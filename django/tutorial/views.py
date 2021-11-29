from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)

import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import psutil
import paho.mqtt.client as mqtt

# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)

class FibView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        order = request.data["order"]
        host = f"{'localhost'}:{8080}"

        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            grpc_request = fib_pb2.FibRequest()
            grpc_request.order = order

            grpc_response = stub.Compute(grpc_request)
        
        client = mqtt.Client()
        client.connect(host="localhost", port=1883)
        client.loop_start()
        client.publish(topic="log", payload=order)
    
        return Response(data={"value": grpc_response.value}, status=200)

class LogView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        host = f"{'localhost'}:{8081}"
        
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LoggerStub(channel)

            grpc_request = log_pb2.LogRequest()
            grpc_request.order = -1

            grpc_response = stub.Log(grpc_request)

        return Response(data={"history": str(grpc_response.value)}, status=200)
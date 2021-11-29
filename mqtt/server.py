import time
import argparse

import psutil
import paho.mqtt.client as mqtt

import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc
import threading

class LoggerServicer(log_pb2_grpc.LoggerServicer):

    def __init__(self):
        self.history = []
        

    def Log(self, request, context):
        n = request.order
        
        if n >= 0:    
            self.history.append(n)
            
        response = log_pb2.LogResponse()
        for i in self.history:
            response.value.append(i)
    
        return response

class MQTT():
    def __init__(self):
        self.grpc_ip = "localhost"
        self.grpc_port = 8081
        self.mqtt_ip = "localhost"
        self.mqtt_port = 1883
    
    @staticmethod
    def on_message(client, obj, msg):
        host = f"{'localhost'}:{8081}"
        
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LoggerStub(channel)

            request = log_pb2.LogRequest()
            request.order = int(msg.payload)

            response = stub.Log(request)
            print(response.value)

        print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")

    def main(self):
        # Establish connection to mqtt broker
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(host=self.mqtt_ip, port=self.mqtt_port)
        client.subscribe('log', 0)

        try:
            client.loop_forever()
        except KeyboardInterrupt as e:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8081, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LoggerServicer()
    log_pb2_grpc.add_LoggerServicer_to_server(servicer, server)

    mqtt_sub = MQTT()
    mqtt_main = threading.Thread(target=mqtt_sub.main)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        mqtt_main.start()
        print(f"Run MQTT Subscriber to {'localhost'}:{1883}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
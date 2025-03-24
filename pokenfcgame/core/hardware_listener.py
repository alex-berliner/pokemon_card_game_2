#!/usr/bin/env python3

import sys
sys.path.append('../build/proto')
import time
import pokemon_interface_pb2_grpc
import pokemon_interface_pb2
import grpc
from threading import Thread
from queue import Queue
from concurrent import futures

# instantiated by showdown interface service to listen for messages from hardware
class PokemonUserEvents(pokemon_interface_pb2_grpc.PokemonUserEventsServicer):
    def __init__(self, queue):
        self.queue = queue

    # # rpc SwitchPokemon (PokemonMessage) returns (PokemonMessage) {}
    # def SwitchPokemon(self, request, context):
    #     print("######################SwitchPokemon########################")
    #     print(f"sending {request} {type(request)}")
    #     self.queue.put(request)
    #     # print(f"q {round(time.time() * 1000)} {request.player_id} inserted")
    #     # TODO: this is what's sent to the client. remove it later.
    #     return pokemon_interface_pb2.PokemonMessage()

    # # rpc SendAttack (AttackMessage) returns (AttackMessage) {}
    # def SendAttack(self, request, context):
    #     print("######################SendAttack########################")
    #     self.queue.put(request)
    #     print(f"sending {request}")
    #     # print(f"q {round(time.time() * 1000)} {request.player_id} inserted")
    #     # TODO: this is what's sent to the client. remove it later.
    #     return pokemon_interface_pb2.AttackMessage()

    # # rpc SendHackedUp (CardEvent) returns (CardEvent) {}
    # def SendCardEvent(self, request, context):
    #     print("######################SendCardEvent########################")
    #     self.queue.put(request)
    #     print(f"sending {request}")
    #     # print(f"q {round(time.time() * 1000)} {request.player_id} inserted")
    #     # TODO: this is what's sent to the client. remove it later.
    #     return pokemon_interface_pb2.CardEventMessage()

    # rpc SendHackedUpMessage (HackedUpMessage) returns (HackedUpMessage) {}
    def SendHackedUpMessage(self, request, context):
        # print("######################SendHackedUp########################")
        self.queue.put(request)
        # print(f"sending {request}")
        # print(f"q {round(time.time() * 1000)} {request.player_id} inserted")
        # TODO: this is what's sent to the client. remove it later.
        return pokemon_interface_pb2.HackedUpMessage()

class HardwareListener:
    def serve(self, queue):
        port = "50051"
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pokemon_interface_pb2_grpc.add_PokemonUserEventsServicer_to_server(PokemonUserEvents(queue), server)
        server.add_insecure_port("[::]:" + port)
        server.start()
        server.wait_for_termination()

    def switch_player(self, active):
        self.active_player = active

    def __init__(self, player_count=2):
        self.active_player = 0
        # Create a thread-safe queue
        self.queue = Queue()
        self.listener_thread = Thread(target=self.serve, args=(self.queue,))
        self.listener_thread.start()

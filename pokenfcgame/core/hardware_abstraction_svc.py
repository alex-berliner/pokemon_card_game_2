#!/usr/bin/env python3

import sys
sys.path.append('../build/proto')
import pokemon_interface_pb2
import pokemon_interface_pb2_grpc
import time
import grpc
from threading import Thread
from queue import Queue
from concurrent import futures
import nfctransport

def poke_proto_read(nt, uid):
    packet = nt.pn532_mifare1k_read_multi(uid)
    print(f"packet: {packet}")
    protokemon = pokemon_interface_pb2.HackedUpMessage() # Init a new (empty) value
    print(f"making new protokemon: {protokemon}")
    # print(''.join('{:02x}'.format(x) for x in packets))
    retval = protokemon.ParseFromString(memoryview(packet)) # Decode a Protobuf message from a string
    print(retval)
    # print(protokemon.pokemon_name)
    return protokemon

def nfctransport_func():
    try:
        nt = nfctransport.NFCTransport()
    except Exception as e:
        print("transport init failed", e)
        return
    while True:
        uid = nt.wait_for_card()
        try:
            pokeproto = poke_proto_read(nt, uid)
        except:
            continue
        # pokeproto.pokemon_name = ">?d"
        print(f"pokeproto: {pokeproto}")
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = pokemon_interface_pb2_grpc.PokemonUserEventsStub(channel)
            response = stub.SendHackedUpMessage(pokeproto)

def keybinput_func():
    moves = {"red":0, "yellow":1, "blue":2, "grey":3}
    while True:
        x = input().lower()
        protokemon = pokemon_interface_pb2.HackedUpMessage()
        if x in moves:
            protokemon.attack = moves[x]
        else:
            protokemon.pokemon_name = x
        print(protokemon)
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = pokemon_interface_pb2_grpc.PokemonUserEventsStub(channel)
            response = stub.SendHackedUpMessage(protokemon)


def main():
    # Create producer and consumer threads
    nfctransport_thread = Thread(target=nfctransport_func, args=())
    keybinput_thread = Thread(target=keybinput_func, args=())

    # Start the threads
    keybinput_thread.start()
    nfctransport_thread.start()

    # Wait for both threads to finish
    keybinput_thread.join()
    nfctransport_thread.join()

if __name__ == "__main__":
    main()

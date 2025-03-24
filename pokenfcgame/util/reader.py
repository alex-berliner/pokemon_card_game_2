#!/usr/bin/env python3

import sys
sys.path.append('build/proto')
import pokemon_interface_pb2
sys.path.append('core')
from nfctransport import *
from pokemon_list import *

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C
import board
import busio
import time
# import mifare1k
import zlib
import struct
import math
BLOCK_COUNT = 720 // 16
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
good_blocks = [i+3 for i in range(1, 60) if i % 4 != 0]
MIFARE_FIRST_BLOCK = 4

# detect cards fast
# read and write protobufs
def pack_message(message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    return packed_len + s

def get_message_length(msg):
    # includes +4 for header
    return 4 + struct.unpack('>L', msg[0:4])[0]

# def make_attack_message(aid):
#     x = pokemon_interface_pb2.AttackMessage()
#     x.attack_id = aid
#     return x

# def make_pokemon_message(name):
#     x = pokemon_interface_pb2.PokemonMessage()
#     # don't set pokemon id, to be set by server
#     x.pokemon_name = name

def make_attack_message2(aid):
    x = pokemon_interface_pb2.HackedUpMessage()
    # don't set pokemon id, to be set by server
    # x.pokemon_name = name
    x.attack = aid

    return x


def write_16(reader, block, uid, data):
    if block < 4 or block > 62:
        return False
    # pn532.mifare_classic_write_block(4, data)
    authenticated = reader.mifare_classic_authenticate_block(uid, block, MIFARE_CMD_AUTH_B, key)
    if not authenticated:
        print("e")
        raise IOError("Authentication failed")

    reader.mifare_classic_write_block(block, data)
    # authenticated = reader.mifare_classic_authenticate_block(uid, 0, MIFARE_CMD_AUTH_B, key)
    # if not authenticated:
    #     print("e")
    #     raise IOError("Authentication failed")
    # authenticated = reader.mifare_classic_authenticate_block(uid, block, MIFARE_CMD_AUTH_B, key)
    # if not authenticated:
    #     print("e")
    #     raise IOError("Authentication failed")
    read_data = reader.mifare_classic_read_block(block)
    # print(f"{block} {read_data} == {data}")
    return read_data == data

def write(reader, uid, data):
    data += bytearray(b'\x00' * ((16 - len(data)) % 16))
    if len(data) > 720:
        print("Data too large:", len(data))
        return False

    blocks_to_write = math.ceil(len(data)/16)
    # print(blocks_to_write)

    for i in range(blocks_to_write):
        byte_offset = i * 16
        block_data = data[byte_offset:byte_offset + 16]
        success = write_16(reader, good_blocks[i], uid, block_data)
        # print(f"Writing block {good_blocks[i]}: {block_data}")
        if not success:
            return False

    return True

def main():
    rtx = NFCTransport()
    rtx.transport_init()
    # i2c = busio.I2C(board.SCL, board.SDA)
    # pn532 = PN532_I2C(i2c, debug=False)
    # pn532.SAM_configuration()
    print(rtx.good_blocks)
    uid = rtx.wait_for_card()
    d = rtx.pn532_mifare1k_read_multi(uid)
    print(d)
    protokemon = pokemon_interface_pb2.HackedUpMessage() # Init a new (empty) value
    retval = protokemon.ParseFromString(memoryview(d)) #
    print(retval)

    # for i in range(4):
    #     for j in range(1):
    #         while True:
    #             uid = pn532.read_passive_target(timeout=0.5)
    #             if uid is not None:
    #                 # print(f"{round(time.time() * 1000)} UID: {uid}")
    #                 break
    #         # r = pack_message(make_attack_message2(i))
    #         # print(write(pn532, uid, r))
    #         # print(f"wrote aid: {i} {r}")
    #         print(pn532_mifare1k_pokemon_read(pn532, uid))
    #         time.sleep(2)

if __name__ == "__main__":
    main()

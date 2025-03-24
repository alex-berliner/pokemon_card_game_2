#!/usr/bin/env python3

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C
import board
import busio
import time
import sys
sys.path.append('../build/proto')
import pokemon_interface_pb2
import struct
import math

class NFCTransport:
    def __init__(self):
        self.BLOCK_COUNT = 720 // 16
        # self.key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
        self.good_blocks = [i+3 for i in range(1, 60) if i % 4 != 0]
        self.MIFARE_FIRST_BLOCK = 4
        self.transport_init()

    def transport_init(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(self.i2c, debug=False)
        self.pn532.SAM_configuration()

    # detect cards fast
    # read and write protobufs
    def pack_message(self, message):
        s = message.SerializeToString()
        packed_len = struct.pack('>L', len(s))
        return packed_len + s

    def get_message_length(self, msg):
        # includes +4 for header
        return 4 + struct.unpack('>L', msg[0:4])[0]

    def read_16(self, block, uid):
        authenticated = self.pn532.mifare_classic_authenticate_block(uid, block, MIFARE_CMD_AUTH_B, self.key)
        if not authenticated:
            print("e")
            raise IOError("Authentication failed")
        readres = self.pn532.mifare_classic_read_block(block)
        # print(f"Reading block {good_blocks[block]}: {readres}")
        if not readres:
            raise IOError("Read failed")
        return readres

    # def read(self, uid, blocks):
    #     results = []
    #     # for block in good_blocks:
    #     for i in range(blocks):
    #         block = good_blocks[i]
    #         # print(block)
    #         data = self.read_16(block, uid)
    #         if data is None:
    #             return None
    #         results.append(data)

    #     return bytearray().join(results)

    def wait_for_card(self):
        while True:
            uid = self.pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                # print(f"{round(time.time() * 1000)} UID: {uid}")
                return uid
        # TODO: probably improve this somehow to reach here
        return -1

    # reads and collates a packet that had a 4 byte length header
    def pn532_mifare1k_read_multi(self, uid):
        # def read_16(pn532, uid, block):
        packets = self.read_16(self.MIFARE_FIRST_BLOCK, uid)
        # print(packets[0])
        message_length = self.get_message_length(packets)
        # print(message_length)
        packets_remaining = math.ceil(message_length / 16) - 1
        # print(packets_remaining)
        for i in range(1, packets_remaining+1):
            packets += self.read_16(good_blocks[i], uid)
        # print(packets)
        return packets[4:message_length]

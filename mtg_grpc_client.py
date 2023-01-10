from __future__ import print_function

import logging

import grpc
from grpc_stubs import card_pb2, card_pb2_grpc

def get_cards(stub: card_pb2_grpc.CardServiceStub):
    cards = stub.GetCardStock(card_pb2.Card_Request(name="Demonic Tutor"))
    for card in cards:
        print(card)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = card_pb2_grpc.CardServiceStub(channel)
        print("------- Test gRPC Server -------")
        get_cards(stub)

if __name__ == '__main__':
    logging.basicConfig()
    run()
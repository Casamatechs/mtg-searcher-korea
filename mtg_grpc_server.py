from concurrent import futures
import logging

import grpc
from grpc_stubs import card_pb2, card_pb2_grpc
from scrappers import kindle, openbinder

class CardServicer(card_pb2_grpc.CardServiceServicer):
    
    def __init__(self) -> None:
        self.kindle = kindle.Kindle()
        self.openbinder = openbinder.Openbinder()

    def GetCardStock(self, request: card_pb2.Card_Request, context):
        yield card_pb2.Card_Response(cards=self.kindle.server_call(request.name))
        for cards_set in self.openbinder.server_call(request.name):
            yield card_pb2.Card_Response(cards=cards_set)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    card_pb2_grpc.add_CardServiceServicer_to_server(
        CardServicer(), server
    )
    server.add_insecure_port('[::]:{}'.format(50051))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
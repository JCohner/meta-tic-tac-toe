# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from remote_calls import game_pb2 as remote__calls_dot_game__pb2


class PiecePlacerStub(object):
    """Piece Placer Service Definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ChooseSquare = channel.unary_unary(
                '/PiecePlacer/ChooseSquare',
                request_serializer=remote__calls_dot_game__pb2.PlayerChoice.SerializeToString,
                response_deserializer=remote__calls_dot_game__pb2.Reply.FromString,
                )


class PiecePlacerServicer(object):
    """Piece Placer Service Definition
    """

    def ChooseSquare(self, request, context):
        """Lets player choose square to place piece
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PiecePlacerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ChooseSquare': grpc.unary_unary_rpc_method_handler(
                    servicer.ChooseSquare,
                    request_deserializer=remote__calls_dot_game__pb2.PlayerChoice.FromString,
                    response_serializer=remote__calls_dot_game__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PiecePlacer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PiecePlacer(object):
    """Piece Placer Service Definition
    """

    @staticmethod
    def ChooseSquare(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PiecePlacer/ChooseSquare',
            remote__calls_dot_game__pb2.PlayerChoice.SerializeToString,
            remote__calls_dot_game__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

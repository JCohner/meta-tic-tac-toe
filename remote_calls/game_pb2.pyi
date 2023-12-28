from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Piece(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    O: _ClassVar[Piece]
    X: _ClassVar[Piece]
O: Piece
X: Piece

class PlayerChoice(_message.Message):
    __slots__ = ("square", "piece")
    SQUARE_FIELD_NUMBER: _ClassVar[int]
    PIECE_FIELD_NUMBER: _ClassVar[int]
    square: str
    piece: Piece
    def __init__(self, square: _Optional[str] = ..., piece: _Optional[_Union[Piece, str]] = ...) -> None: ...

class Reply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

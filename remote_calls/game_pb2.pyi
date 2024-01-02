from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlayerChoice(_message.Message):
    __slots__ = ("square", "piece")
    SQUARE_FIELD_NUMBER: _ClassVar[int]
    PIECE_FIELD_NUMBER: _ClassVar[int]
    square: str
    piece: int
    def __init__(self, square: _Optional[str] = ..., piece: _Optional[int] = ...) -> None: ...

class Reply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

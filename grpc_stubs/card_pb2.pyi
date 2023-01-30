from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Card(_message.Message):
    __slots__ = ["cond", "foil", "imgUrl", "lang", "name", "price", "set", "stock", "store"]
    COND_FIELD_NUMBER: _ClassVar[int]
    FOIL_FIELD_NUMBER: _ClassVar[int]
    IMGURL_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    cond: str
    foil: bool
    imgUrl: str
    lang: str
    name: str
    price: int
    set: str
    stock: int
    store: str
    def __init__(self, name: _Optional[str] = ..., lang: _Optional[str] = ..., cond: _Optional[str] = ..., store: _Optional[str] = ..., price: _Optional[int] = ..., stock: _Optional[int] = ..., foil: bool = ..., set: _Optional[str] = ..., imgUrl: _Optional[str] = ...) -> None: ...

class Card_Request(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Card_Response(_message.Message):
    __slots__ = ["cards"]
    CARDS_FIELD_NUMBER: _ClassVar[int]
    cards: _containers.RepeatedCompositeFieldContainer[Card]
    def __init__(self, cards: _Optional[_Iterable[_Union[Card, _Mapping]]] = ...) -> None: ...

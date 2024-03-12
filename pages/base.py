from requests import get, post, Session, Request, Response
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")
class BaseScraper(Generic[T]):
    """
    Clase padre para todos los scrapers
    para pasar metadatos adicionales se debe usar self.extra
    """

    def __init__(self, session:Optional[Session]=None, default_url:Optional[str]=None, extra=None):
        super().__init__()
        self.session:Optional[Session] = session
        self.default_url:Optional[str] = default_url
        self.extra:Any = extra
        self.extra_file:Optional[str] = None
        self.extra_url:Optional[str] = None
        self.extra_request:Optional[Request]|Any = None
        self.extra_response:Optional[Response]|Any = None

    def parse_file(self, file:str) -> Optional[T]:
        try:
            self.extra_file = file
            with open(file, "rb") as f:
                data = f.read()
            return self.parse_bytes(data)
        finally:
            self.extra_file = None

    def parse_post(self, url:str|Any, data:bytes, *args, **kws) -> Optional[T]:
        try:
            if url is None and self.default_url is not None:
                url = self.default_url
            self.extra_url = url
            if self.session:
                res = self.session.post(url, data=data, *args, **kws)
            else:
                res = post(url, data=data, *args, **kws)
            #type:ignore
            self.extra_request = res.request
            self.extra_response = res
            if res.status_code//100 not in [2,3]:
                # No es 2XX o 3XX
                return None
            return self.parse_bytes(res.content)
        except Exception as err:
            #TODO:Log
            raise Exception("Unexpected exception on HTTP request", err)
        finally:
            self.extra_url = None
            self.extra_request = None
            self.extra_response = None

    def parse_get(self, url:str|Any, *args, **kws) -> Optional[T]:
        try:
            if url is None and self.default_url is not None:
                url = self.default_url
            
            if self.session:
                res = self.session.get(url, *args, **kws)
            else:
                res = get(url, *args, **kws)
            if res.status_code//100 not in [2,3]:
                # No es 2XX, 3XX (Se permite redireccionamientos)
                return None
            return self.parse_bytes(res.content)
        except Exception as err:
            #TODO:Log
            raise Exception("Unexpected exception on HTTP request", err)

    def parse_text(self, txt: str) -> Optional[T]:
        return self.parse_bytes(txt.encode()) #UTF-8
    
    def parse_bytes(self, bs: bytes) -> Optional[T]:
        "Metodo abstracto, debe ser reescrito en cada clase hija"
        return None

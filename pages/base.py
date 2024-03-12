from requests import get, post, Session, Request, Response
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")
class BaseScraper(Generic[T]):
    """
    Clase padre para todos los scrapers
    para pasar metadatos adicionales se debe usar self.extra
    """

    def __init__(self) -> None:
        super().__init__()
        self.session:Session = None
        self.extra:Any = None
        self.extra_file:str = None
        self.extra_url:str = None
        self.extra_request:Request = None
        self.extra_response:Response = None

    def parse_file(self, file:str) -> Optional[T]:
        try:
            self.extra_file = file
            with open(file, "rb") as f:
                data = f.read()
            return self.parse_bytes(data)
        finally:
            self.extra_file = None

    def parse_post(self, url:str, data:bytes, *args, **kws) -> Optional[T]:
        try:
            self.extra_url = url
            if self.session:
                res = self.session.post(url, data=data, *args, **kws)
            else:
                res = post(url, data=data, *args, **kws)
            self.extra_request = res.request
            self.extra_response = res
            if res.content//100 not in [2,3]:
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

    def parse_get(self, url:str, *args, **kws) -> Optional[T]:
        try:
            if self.session:
                res = self.session.get(url, *args, **kws)
            else:
                res = get(url, *args, **kws)
            if res.content//100 not in [2,3]:
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

"""
Parser para la pagina: index.php
Devuelve un objeto que contiene: login erroneo, y proximo Token
"""

from dataclasses import dataclass

from .base import BaseScraper

@dataclass
class IndexResult:
    wrong_login: bool
    session_id: str

class IndexScraper(BaseScraper[IndexResult]):
    def parse_bytes(self, bs: bytes) -> IndexResult | None:
        res = IndexResult(False, None)

        #Si encontramos, entonces hubo problemas al logearse
        badlogin = b"User does not exist or incorrect password."
        res.wrong_login = badlogin in bs

        #Buscamos el session_id
        for line in bs.splitlines():
            if b"passHASH = js_myhash(" in  line:
                splt = line.split(b'\'')
                if len(splt) >= 2:
                    res.session_id = splt[1].decode("utf-8")
                break

        return res
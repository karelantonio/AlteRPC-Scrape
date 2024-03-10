"""
Parser de la pagina de aclaraciones
Devuelve una lista con cada aclaracion
"""
from bs4 import BeautifulSoup, element
from dataclasses import dataclass
from typing import List

from .base import BaseScraper

@dataclass
class Clarification:
    question:str
    response:str

class ClarificationScraper(BaseScraper[List[Clarification]]):
    def __init__(self) -> None:
        super().__init__()

    def parse_bytes(self, data: bytes) -> List[Clarification] | None:
        bs = BeautifulSoup(data, "html.parser")
        res : List[Clarification] = []
        all : List[element.Tag] = bs.find_all("textarea")
        for i in range( len(all)//2 ):
            t1, t2 = all[2*i], all[2*i+1]
            res.append(Clarification(
                t1.getText(strip=True),
                t2.getText(strip=True)
            ))
        return res

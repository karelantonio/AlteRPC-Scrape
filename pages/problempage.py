"""
Scraper de la lista de problemas
devuelve un objeto con la lista de nombres de los problemas
y la URL para descargar el archivo que contiene la descripcion de cada
problema (el pdf del problema A)
"""
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List

from .base import BaseScraper

@dataclass
class Problems:
    names: List[str]
    basenames: List[str]
    fullnames: List[str]
    desc_file: str

class ProblemScraper(BaseScraper[Problems]):
    def parse_bytes(self, data: bytes) -> Problems | None:
        names = []
        basenames = []
        fullnames = []
        desc_file = None
        
        bs = BeautifulSoup(data, "html.parser")
        tables = bs.find_all("table")
        if len(tables) < 3:
            return Problems(names, basenames, fullnames, desc_file)
        table : Tag = tables[2]
        for tr in list(table.find_all("tr"))[1:]:
            tg : Tag = tr
            childs = list(tg.find_all("td"))
            if len(childs) < 4:
                continue
            name = childs[0].getText(strip=True)
            basename = childs[1].getText(strip=True)
            fullname = childs[2].getText(strip=True)
            
            names.append(name)
            basenames.append(basename)
            fullnames.append(fullname)
            a = tg.find_all("a")
            if a and len(a)>0:
                a = a[0]
                desc_file = a.attrs["href"]
        return Problems(names, basenames, fullnames, desc_file)

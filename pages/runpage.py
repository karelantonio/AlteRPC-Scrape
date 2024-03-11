"""
Scraper para la pagina de run.php
Devuelve una lista de los ultimos runs asi como el token para el proximo run
"""

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List

from .base import BaseScraper

@dataclass
class Submission:
    run_id:int
    time:int
    problem:str
    language:str
    answer:str
    download_url:str

class RunScraper(BaseScraper[List[Submission]]):
    def parse_bytes(self, data: bytes) -> List[Submission] | None:
        bs = BeautifulSoup(data, "html.parser")
        tables:List[Tag] = list(bs.find_all("table"))
        if len(tables) < 2:
            return []
        table = tables[-2]
        rows:List[Tag] = list(table.find_all("tr"))

        res = []

        for row in rows[1:]:
            childs:List[Tag] = row.find_all("td")
            if len(childs) != 6:
                continue
            pid = childs[0].getText(strip=True)
            time = childs[1].getText(strip=True)
            problem = childs[2].getText(strip=True)
            language = childs[3].getText(strip=True)
            answer = childs[4].getText(strip=True)
            file = childs[5].find("a").attrs["href"] or ""
            res.append(Submission(
                int(pid), int(time), problem, language, answer, file
            ))
        return res

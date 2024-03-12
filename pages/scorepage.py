"""
Scraper de la pagina score.php
Devuelve el ranking
"""

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List, Optional

from .base import BaseScraper

@dataclass
class User:
    num:int
    name:str
    country:Optional[str]
    university:str
    problems:List[int]
    total:str

class ScoreScraper(BaseScraper[List[User]]):
    def parse_bytes(self, data: bytes) -> List[User] | None:
        bs = BeautifulSoup(data, "html.parser")
        table:Tag = bs.find("table", id="myscoretable")
        if table is None:
            return []
        good_rows:List[Tag] = list(table.find_all("tr", attrs={"class":"sitegroup1"}))
        res : List[User] = []

        for row in good_rows:
            tds:List[Tag] = list(row.find_all("td"))
            if len(tds) < 4:
                continue
            pos = tds[0].getText(strip=True)
            name = tds[1].getText(strip=True)
            univ = tds[2].getText(strip=True)
            total = tds[-1].getText(strip=True)
            ctry_img = tds[1].find("img")
            country = None if not ctry_img else ctry_img.attrs["alt"]

            problems = []
            for idx, tag in enumerate(tds[3:-1], start=1):
                if tag.find("img"):
                    problems.append(idx)

            res.append(User(
                int(pos), name, country, univ, problems, total
            ))

        return res
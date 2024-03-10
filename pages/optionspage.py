"""
Scraper de la pagina de options.php
Devuelve cada una de las configuraciones existentes
"""
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag

from .base import BaseScraper

@dataclass
class Options:
    username:str
    fullname:str
    description:str
    country:str
    country_code:str


class OptionsScraper(BaseScraper[Options]):
    def parse_bytes(self, data: bytes) -> Options | None:
        bs = BeautifulSoup(data, "html.parser")
        #Username
        usertag : Tag = bs.find("input", attrs=dict(name="username") )
        username = usertag.attrs["value"] if usertag is not None else None
        #FullName
        fnametag : Tag = bs.find("input", attrs=dict(name="userfull") )
        fullname = fnametag.attrs["value"] if fnametag is not None else None
        #Description
        desctag : Tag = bs.find("input", attrs=dict(name="userdesc") )
        description = desctag.attrs["value"] if desctag is not None else None
        #Country
        ctry : Tag = bs.find("select")
        if ctry and "selected" in ctry.attrs:
            country_code = ctry.attrs["selected"]
            ctry_name = bs.find("option", value=country_code.lower())
            country = ctry_name.getText(strip=True) if ctry_name is not None else country_code
        else:
            country_code = "Unknown"
            country = "Unknown"
        
        return Options(
            username,
            fullname,
            description,
            country,
            country_code
        )

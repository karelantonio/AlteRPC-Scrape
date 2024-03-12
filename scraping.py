"""
Clase que deberia usarse para hacer scraping
Provee una API sencilla
"""

from hashlib import sha256
from os.path import join
from requests import Session
from typing import List, Optional

try:
    from .pages.indexpage import IndexScraper
    from .pages.problempage import ProblemScraper, ProblemList, Problem
    from .pages.runpage import RunScraper, Submission
    from .pages.scorepage import ScoreScraper, User
    from .pages.clarificationpage import ClarificationScraper, Clarification
    from .pages.optionspage import OptionsScraper, Options
except ImportError:
    #ImportError: attempted relative import with no known parent package
    from pages.indexpage import IndexScraper
    from pages.problempage import ProblemScraper, ProblemList, Problem
    from pages.runpage import RunScraper, Submission
    from pages.scorepage import ScoreScraper, User
    from pages.clarificationpage import ClarificationScraper, Clarification
    from pages.optionspage import OptionsScraper, Options
    pass


class AlteRPCClient:
    """
    Cliente para utilizar el juez del RPC via su web
    """
    def __init__(self, base:str, session:Optional[Session]=None):
        """
        Constructor, necesita la ruta base para ser utilizado (P.Ej: https://test.web/somecontest/2024/13)
        """
        self.base = base
        self.urls = {
            "index.php":join(base, "index.php"),
            "problem.php":join(base, "team/problem.php"),
            "run.php":join(base, "team/run.php"),
            "score.php":join(base, "score/index.php"),
            "clar.php":join(base, "team/clar.php"),
            "option.php":join(base, "team/options.php")
        }
        self.session = session or Session()
        self._index = IndexScraper( session=self.session, default_url=self.urls["index.php"] )
        self._problem = ProblemScraper( session=self.session, default_url=self.urls["problem.php"] )
        self._run = RunScraper( session=self.session, default_url=self.urls["run.php"] )
        self._score = ScoreScraper( session=self.session, default_url=self.urls["score.php"] )
        self._clar = ClarificationScraper( session=self.session, default_url=self.urls["clar.php"] )
        self._opts = OptionsScraper( session=self.session, default_url=self.urls["option.php"] )

    def login(self, username:str, passw:str) -> bool:
        res = self._index.parse_get(None)
        if res is None or res.session_id is None:
            return False
        passHash = sha256( (sha256(passw.encode("utf-8")).hexdigest() + res.session_id).encode("utf-8") ).hexdigest()
        res2 = self._index.parse_get(None, params={
            "name":username,
            "password":passHash
        })
        if res2 is not None and res2.wrong_login:
            return False
        else:
            return True
        
    def needs_relogin(self) -> bool:
        res = self.session.get(self.urls["clar.php"])
        return res.status_code != 200 or b"expired" in res.content

    def logout(self) -> None:
        self._index.parse_get(None)

    def problems(self) -> Optional[ProblemList]:
        return self._problem.parse_get(None)
    
    def runs(self) -> Optional[List[Submission]]:
        return self._run.parse_get(None)
    
    def score(self) -> Optional[List[User]]:
        return self._score.parse_get(None)

    def clarifications(self) -> Optional[List[Clarification]]:
        return self._clar.parse_get(None)
    
    def options(self) -> Optional[Options]:
        return self._opts.parse_get(None)

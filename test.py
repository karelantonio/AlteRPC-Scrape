"""
Modulo de testing
Datos para testing en el directorio: test_data
"""
from unittest import TestCase

import pages.clarificationpage
import pages.indexpage
import pages.optionspage
import pages.problempage
import pages.runpage
import pages.scorepage
#import scraping

#TODO:Implementar todo esto:

class ClarificationTest(TestCase):
    pass

class IndexTest(TestCase):
    def test_get_session_id(self):
        scrp = pages.indexpage.IndexScrapper()
        res = scrp.parse_file("test_data/login_page.html")
        self.assertEqual(res.session_id, "dsjrnu884u621c0de2h4en0raq")

        res = scrp.parse_file("test_data/login_page_wrong.html")
        self.assertEqual(res.session_id, "anotherSessionID")

    def test_get_badlogin(self):
        scrp = pages.indexpage.IndexScrapper()
        res = scrp.parse_file("test_data/login_page.html")
        self.assertFalse(res.wrong_login)

        res = scrp.parse_file("test_data/login_page_wrong.html")
        self.assertTrue(res.wrong_login)


class OptionsTest(TestCase):
    pass

class ProblemTest(TestCase):
    pass

class RunTest(TestCase):
    pass

class ScoreTest(TestCase):
    pass

if __name__=="__main__":
    from unittest import main
    main()

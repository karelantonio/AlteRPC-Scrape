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
    def test_get_first_clarification_right(self):
        fst_q = "En el caso 1 la respuesta no debería ser 20?"
        fst_a = "La respuesta correcta es 20."

        scrp = pages.clarificationpage.ClarificationScraper()
        res = scrp.parse_file("test_data/clarifications_page.html")
        self.assertIsNotNone( res )
        self.assertGreaterEqual( len(res), 1 )
        res = res[0]
        self.assertEqual( res.question[:len(fst_q)] , fst_q )
        self.assertEqual( res.response, fst_a )

    def test_get_all(self):
        scrp = pages.clarificationpage.ClarificationScraper()
        res = scrp.parse_file("test_data/clarifications_page.html")
        self.assertIsNotNone( res )
        self.assertEqual( len(res), 4 )

    def test_all_matches(self):
        scrp = pages.clarificationpage.ClarificationScraper()
        res = scrp.parse_file("test_data/clarifications_page.html")
        self.assertIsNotNone( res )
        clarifications = [
            ("En el caso 1 la respuesta no debería ser 20?", "La respuesta correcta es 20."),
            ("En el primer caso de prueba, si Panda comienza en la posición indicada", "La respuesta correcta es 20."),
            ("La salida del primer caso de ejemplo está mal", "La respuesta correcta es 20."),
            ("¿Donde está la descripción de este problema?", "En la RPC siempre el problemset completo se encuentra en el problema A.")
        ]
        self.assertEqual( len(res), len(clarifications) )
        for first, second in zip(res, clarifications):
            self.assertTrue( first.question.startswith(second[0]) , first.question)
            self.assertTrue( first.response.startswith(second[1]) , first.response)
        #Todo OK


class IndexTest(TestCase):
    def test_get_session_id(self):
        scrp = pages.indexpage.IndexScraper()
        res = scrp.parse_file("test_data/login_page.html")
        self.assertEqual(res.session_id, "dsjrnu884u621c0de2h4en0raq")

        res = scrp.parse_file("test_data/login_page_wrong.html")
        self.assertEqual(res.session_id, "anotherSessionID")

    def test_get_badlogin(self):
        scrp = pages.indexpage.IndexScraper()
        res = scrp.parse_file("test_data/login_page.html")
        self.assertFalse(res.wrong_login)

        res = scrp.parse_file("test_data/login_page_wrong.html")
        self.assertTrue(res.wrong_login)


class OptionsTest(TestCase):
    def test_options(self):
        scrp = pages.optionspage.OptionsScraper()
        res = scrp.parse_file("test_data/options_page.html")

        self.assertEqual(res.username, "exacerbados")
        self.assertEqual(res.fullname, "Exacerbados")
        self.assertEqual(res.description, "IPVCE José Martí")
        self.assertEqual(res.country_code, "CU")
        self.assertEqual(res.country, "Cuba")



class ProblemTest(TestCase):
    pass

class RunTest(TestCase):
    pass

class ScoreTest(TestCase):
    pass

if __name__=="__main__":
    from unittest import main
    main()

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
    def test_fetch_problem_list(self):
        scrp = pages.problempage.ProblemScraper()
        res = scrp.parse_file("test_data/problem_page.html")
        self.assertEqual(res.desc_file, "../filedownload.php?oid=-1&filename=LzhTMjI2bDFFZXhTUFAzWmxtYWc0TDg1SmplVE5SSW91SklSbHFleGVUSWJGYzVjZ3VCN2VDWTFxZThhYXYxQ0lPK0tDUW5RcDUwa1JCZkMxVnhJU2dtV0ZpcjJXMFpUQVQxSDkvU2duUmhMSzVyK3VDMU1Lbm9PYk1McE0wS1pyNXE2bGtNdFcrWW4xdHoyUm9GNnVxT21heHBLTHI4QVp3ejVSdlFmNkZGRFRiL3RRSDJVN2FoVTcweHBYQ1F3&check=eec95c894c74001f2fb6afd588ce8abc7512e19405ea9ced36064e83846d0ceb")
        self.assertEqual(res.fullnames[0], "Easy-to-Solve Expressions")
        self.assertEqual(res.basenames[3], "Fishing")
        self.assertEqual(len(res.names), 13)
        self.assertEqual(len(res.basenames), 13)
        self.assertEqual(len(res.fullnames), 13)



class RunTest(TestCase):
    def test_run_fetch_correct_size_of_elements(self):
        scrp = pages.runpage.RunScraper()
        res = scrp.parse_file("test_data/runs_page.html")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 21)

    def test_matches_first_element(self):
        scrp = pages.runpage.RunScraper()
        res = scrp.parse_file("test_data/runs_page.html")
        self.assertIsNotNone(res)
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual( res[0].run_id, 450971511 )
        self.assertEqual( res[0].time, 18 )
        self.assertEqual( res[0].problem, "A" )
        self.assertEqual( res[0].language, "C++11" )
        self.assertEqual( res[0].answer, "NO - Presentation error" )
        self.assertEqual( res[0].download_url, "../filedownload.php?oid=249408&filename=cDdIRWZrOGxEZ3A1dXByOHdOK0V1ZHNYY0s0STdLOElhSnRWNUh4dlMrbTlFWms2aWJCRXhhek5VSXArZWNZeS9VeW5IMTNFbVRlWU15d0xwOWViR3pwY1JxVXJPVEV3dXovYXFMV3l4U3c9&check=d0aaefd0080ff4f3da0c939993097846d989908e213c82e6bf1c4401026c1920" )

    def test_matches_last_element(self):
        scrp = pages.runpage.RunScraper()
        res = scrp.parse_file("test_data/runs_page.html")
        self.assertIsNotNone(res)
        self.assertEqual( len(res), 21 )
        self.assertEqual( res[20].run_id, 619084361 )
        self.assertEqual( res[20].time, 298 )
        self.assertEqual( res[20].problem, "F" )
        self.assertEqual( res[20].language, "C++11" )
        self.assertEqual( res[20].answer, "NO - Wrong answer" )
        self.assertEqual( res[20].download_url, "../filedownload.php?oid=252382&filename=cFplMmVKMXBJVkp6aStTMFpuV1lGMnRLZS82eFR4KzZTUWdML1RvS3EwOHowNXZkdWVobGFIekZ1WHZiTEFZM05Dam84ejM1VWw3cDcxM3ZOcmNVby9NdytybVdtMER4cmNBSVVzUnROVE09&check=9fb8f4a01acfd444fb370d1912c73cf697d7b674326392632ac1f601b4aabbf4" )


class ScoreTest(TestCase):
    pass

if __name__=="__main__":
    from unittest import main
    main()

from unittest import TestCase

import main as mn


class Test(TestCase):
    def test_1(self):
        line = 'Alphard. 1974. Name of the brightest star in Hydra. Pascal-like, not implemented.'
        lang = mn.parse_line_into_lang(line)
        self.assertEqual('Alphard', lang.name)
        self.assertEqual('1974', lang.year)
        desc = 'Name of the brightest star in Hydra. Pascal-like, not implemented.'
        self.assertEqual(desc, lang.desc)

    def test_2(self):
        line = 'AQL, Aerospike Query Language. 2012. Simple language but more evolved than SQL for the Aerospike DBM.'
        lang = mn.parse_line_into_lang(line)
        self.assertEqual('AQL', lang.name)
        self.assertEqual('AQL, Aerospike Query Language', lang.full_name)
        self.assertEqual('2012', lang.year)
        desc = 'Simple language but more evolved than SQL for the Aerospike DBM.'
        self.assertEqual(desc, lang.desc)

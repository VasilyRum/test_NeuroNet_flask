import unittest
from blueprint import make_request


class BlueprintFunctionTest(unittest.TestCase):
    def test_make_request(self):
        self.assertEqual(make_request('12ksasnnas'),
                         'Something goes wrong, try another one')
        self.assertEqual(make_request('Арзамас'),
                         'Entered address is 474.19km away from MKAD')
        self.assertEqual(make_request('Москва'),
                         'Entered address is in MKAD-area')
        self.assertEqual(make_request('Kansas'),
                         'Something goes wrong, try another one')
        self.assertEqual(make_request('       '),
                         'Something goes wrong, try another one')
        self.assertEqual(make_request(123),
                         'Something goes wrong, try another one')
        self.assertEqual(make_request([123]),
                         'Something goes wrong, try another one')


if __name__ == "__main__":
    unittest.main()

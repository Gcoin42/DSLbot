import unittest
from douban import fetch_douban
from lianjia import fetch_lianjia
from interpreter import parse_range

class TestDouban(unittest.TestCase):
    def test_fetch_douban(self):
        df = fetch_douban()
        self.assertFalse(df.empty)
        self.assertIn('Title', df.columns)

class TestLianjia(unittest.TestCase):
    def test_fetch_lianjia(self):
        url = "https://bj.fang.lianjia.com/loupan/"
        data, success = fetch_lianjia(url)
        self.assertTrue(success)
        self.assertGreater(len(data), 0)

class TestParseRange(unittest.TestCase):
    def test_parse_range(self):
        start, end = parse_range("1-10")
        self.assertEqual(start, 1)
        self.assertEqual(end, 10)
        start, end = parse_range("invalid")
        self.assertIsNone(start)
        self.assertIsNone(end)

if __name__ == '__main__':
    unittest.main()
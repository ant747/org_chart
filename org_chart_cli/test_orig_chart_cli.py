import unittest
import org_chart_cli as cli

class TectCli(unittest.TestCase):

    def test_add_seq_len(self):
        self.assertNotEqual (cli.check_seq_len(['a']), '')
        self.assertNotEqual (cli.check_seq_len(['1',]), '')
        self.assertEqual    (cli.check_seq_len(['a','b']), '')
        self.assertEqual    (cli.check_seq_len(['r','1','.']), '')

    def test_add_seq_empty(self):
        self.assertNotEqual (cli.check_seq_empty_elements(['a','']), '')
        self.assertNotEqual (cli.check_seq_empty_elements(['','.']), '')
        self.assertEqual    (cli.check_seq_empty_elements(['a','.']), '')
        self.assertEqual    (cli.check_seq_empty_elements(['1','2']), '')

    def test_add_seq_no_letters(self):
        self.assertNotEqual (cli.check_seq_letter(['a','1']), '')
        self.assertNotEqual (cli.check_seq_letter(['e','.']), '')
        self.assertEqual    (cli.check_seq_letter(['a','j','H']), '')
        self.assertEqual    (cli.check_seq_letter(['F','g']), '')

if __name__ == '__main__':
    unittest.main()
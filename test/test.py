import unittest
from cleaner import rm_empty_files, rm_temp_files, scan_files
from make_mess import make_mess


class BasicTest(unittest.TestCase):
    def setUp(self):
        make_mess()
        self.x_files_list = scan_files("X")
        self.y_files_list = scan_files("Y1")

    def tearDown(self):
        make_mess()
        self.x_files_list = scan_files("X")
        self.y_files_list = scan_files("Y1")

    def test_list(self):
        assert "X/15875" in self.x_files_list
        assert "X/27726.tmp" in self.x_files_list
        assert "X/20065" in self.x_files_list
        assert "Y1/20065" not in self.y_files_list
        assert "Y1/6142" in self.y_files_list
        assert "X/6142" not in self.x_files_list

    def test_rm_empty(self):
        modified_files_list = rm_empty_files(self.x_files_list, True)
        assert "X/15875" not in modified_files_list
        assert "X/24552" not in modified_files_list
        assert "X/27148" not in modified_files_list
        assert "X/29191" not in modified_files_list

    def test_rm_temp(self):
        modified_files_list = rm_temp_files(self.x_files_list, "*.tmp", True)
        assert "X/14806.tmp" not in modified_files_list
        assert "X/27726.tmp" not in modified_files_list
        assert "X/20502.tmp" not in modified_files_list

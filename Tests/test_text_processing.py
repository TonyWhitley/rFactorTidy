"""
docstring
"""
import unittest
# pylint: disable=protected-access,line-too-long
from rFactorTidy import TraceReader, TRACE_FILE, PARSED_FILE, NO_SIMILAR_FILE,\
    DUPLICATES_FILE

SINGLE_LINE = ["   9.61s setup.cpp    1746: Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n"]
PARSED_LINE = ["Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n"]
DUPLICATE_LINES = [
    "   9.61s setup.cpp    1746: Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n",
    "   9.61s setup.cpp    1746: Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n",
    "   9.61s setup.cpp    1746: Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n"
    ]
NEAR_DUPLICATE_LINE1 = r"Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_83.VEH"
NEAR_DUPLICATE_LINE2 = r"Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_4.VEH"
LESS_DUPLICATE_LINE1 = r"Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2017\1.6\USF2000_5.VEH"
DUPLICATE_MODS = [
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_9.VEH",
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_91.VEH",
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_92.VEH",
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\Tatuus_PM-18_2018\1.03\01PM_LAUNCE3E4CE63.VEH",
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\Tatuus_PM-18_2018\1.03\02JUNCOS97731899.VEH",
    r"   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\Tatuus_PM-18_2018\1.03\10RP_MOTORA589144B.VEH"
    ]

DUPLICATE_MODS_RESULT = [
    r"Vehicles\USF2000_2016\1.5"+"\n",
    r"Vehicles\Tatuus_PM-18_2018\1.03"+"\n"
    ]

class TestTextProcessing(unittest.TestCase):
    """
    docstring
    """
    def setUp(self):
        """
        docstring
        """
        self.tr_o = TraceReader()

    def test_single_line(self):
        """
        docstring
        """
        self.tr_o._ut_load_text(SINGLE_LINE)
        self.tr_o.parse()
        _parsed = self.tr_o.get_parsed_text()
        self.assertEqual(_parsed, PARSED_LINE, \
            _parsed)

    def test_duplicate_lines(self):
        """
        docstring
        """
        self.tr_o._ut_load_text(DUPLICATE_LINES)
        self.tr_o.parse()
        _parsed = self.tr_o.get_parsed_text()
        self.assertEqual(_parsed, PARSED_LINE, \
            _parsed)

    def test_similar_lines(self):
        """
        docstring
        """
        #self.tr_o._ut_load_text(NEAR_DUPLICATE_LINES)
        #self.tr_o.parse()
        _same, _diff = self.tr_o._near_duplicate(NEAR_DUPLICATE_LINE1, NEAR_DUPLICATE_LINE2)
        self.assertGreater(_same, 24)
        self.assertLess(_diff, 3)

    def test_less_similar_lines(self):
        """
        docstring
        """
        _same, _diff = self.tr_o._near_duplicate(NEAR_DUPLICATE_LINE1, LESS_DUPLICATE_LINE1)
        self.assertLess(_same, 24)
        self.assertGreater(_diff, 2)

    def test_find_duplicate_mods(self):
        """
        docstring
        """
        self.tr_o._ut_load_text(DUPLICATE_MODS)
        self.tr_o.parse()
        _duplicates = self.tr_o.get_duplicate_mods()
        self.assertEqual(_duplicates, DUPLICATE_MODS_RESULT, _duplicates)

class TestFileHandling(unittest.TestCase):
    """
    docstring
    """
    def setUp(self):
        """
        docstring
        """
        self.tr_o = TraceReader()

    def test_read_no_such_file(self):
        """
        docstring
        """
        _res = self.tr_o.read_file("no such file")
        self.assertFalse(_res)

    def test_read_trace_file(self):
        """
        docstring
        """
        _res = self.tr_o.read_file(TRACE_FILE)
        self.assertTrue(_res)

    def test_write_no_such_file(self):
        """
        docstring
        """
        _res = self.tr_o.write_file("/no/such/path/file")
        self.assertFalse(_res)

class TestRealFiles(unittest.TestCase):
    """
    docstring
    """
    def setUp(self):
        """
        docstring
        """
        self.tr_o = TraceReader()

    def test_write_parsed_file(self):
        """
        docstring
        """
        _res = self.tr_o.read_file(TRACE_FILE)
        self.assertTrue(_res)
        self.tr_o.parse()
        _res = self.tr_o.write_file(PARSED_FILE)
        self.assertTrue(_res)

    def test_write_no_similar_file(self):
        """
        docstring
        """
        _res = self.tr_o.read_file(TRACE_FILE)
        self.assertTrue(_res)
        self.tr_o.parse()
        self.tr_o.remove_similar()
        _res = self.tr_o.write_file(NO_SIMILAR_FILE)
        self.assertTrue(_res)

    def test_write_duplicate_mods(self):
        """
        docstring
        """
        _res = self.tr_o.read_file(TRACE_FILE)
        self.assertTrue(_res)
        self.tr_o.parse()
        _res = self.tr_o.write_duplicates(DUPLICATES_FILE)
        self.assertTrue(_res)

if __name__ == '__main__':
    unittest.main()

# pylint: disable=invalid-name # (rFactorTidy)
r""" # pylint: disable=line-too-long
A program to read ...\rFactor 2\UserData\Log\trace.txt, de-dupe and parse the
errors/warnings.
Output a de-duped copy of the trace file
Output a list of mods which are duplicates of newer ones

(Later offer to clean up the rFactor installation)

Types of messages parsed:
Error opening shaders MAS file brianza1966.mas
    tbd. just a warning?

WARNING: Unable to find track-specific gdb file for: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\Aquitania\1.1\_OUTPUT.scn
    tbd. just a warning?

Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_12.VEH
    Old version of mod, could be deleted

Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long
    tbd. just a warning?

Could not find M6_GTLM_CAM.CAM
Couldn't find cam file or load cam file  for vehicle C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\STK BMW M6 GT3\1.20\M6_GT3_16025IM.VEH
Could not find special spinner GEN file M6_GTLM_SPIN.GEN, defaulting to normal GEN file M6_GTLM.GEN
Could not find file "flag_yellow_race.wav" from commentary script
    Could not find group: tbd. just a warning?

Not using vehicle C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\STK BMW M6 GT3\1.20\M6_GT3_16025IM.VEH because one or more important references could not be found
    tbd. just a warning?

Couldn't figure out line in TrackConfigs file "C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\F1RFT_2013_Frenky_1.61\1.61\TRACKCONFIGSBASE.INI":
Erroneous line->"Nürburgring Grand Prix"
    tbd. just a warning?

ATTENTION: Skipping vehicle because the filename CLASSIC_BLACKYELLOW_B.VEH exceeds the maximum length by 2 character(s)
Livery file CLASSIC_BLACKYELLOW excluded from list on account of being too long

Collidable instance "TREES3DT_01" is dependent on track detail level
    tbd. just a warning?

CUBE error loading animation file HOLDLEFT.ANM: Error locating animation file HOLDLEFT.ANM
    tbd. just a warning?

Unable to adjust texture for material: wcwindshieldin_001, tex0=HG4_1967Endur_14windshieldin.DDS, tex1=Misc\HG4_1967Endur_14windshieldin.DDS, tex2=HG4_1967Endur_14windshieldin.DDS

"""

r""" # pylint: disable=line-too-long
De-dupe turns
   8.67s setup.cpp    4052: WARNING: Unable to find track-specific gdb file for: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\Sportsland_Sugo\1.05\_OUTPUT.scn
   8.84s setup.cpp    4052: WARNING: Unable to find track-specific gdb file for: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\exm_spa\1.1\_OUTPUT.scn
   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_12.VEH
   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_19.VEH
   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_16.VEH
   9.20s setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_17A.VEH
into
setup.cpp    4052: WARNING: Unable to find track-specific gdb file for: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\Sportsland_Sugo\1.05\_OUTPUT.scn
setup.cpp    4052: WARNING: Unable to find track-specific gdb file for: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\exm_spa\1.1\_OUTPUT.scn
setup.cpp    2358: Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5

"""
from typing import List, Tuple #, Set, Dict, Optional   # pylint: disable=wrong-import-position
from os.path import split   # pylint: disable=wrong-import-position

TRACE_FILE = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\Log\trace.txt"
PARSED_FILE = r"c:\temp\parsed_trace.txt"
NO_SIMILAR_FILE = r"c:\temp\parsed_no_similar_trace.txt"
DUPLICATES_FILE = r"c:\temp\duplicate_mods.txt"

class TraceReader:
    """
    Read and parse an rFactor 2 trace file
    """
    # pylint: enable=invalid-name
    __in_text: List[str] = list()
    __out_text: List[str] = list()
    """
    Unit test methods
    """
    def _ut_load_text(self, text: List[str]) -> None:
        """
        Load a list of test strings
        """
        self.__in_text = text

    def read_file(self, filepath: str) -> bool:
        """
        Return false if read fails
        """
        try:
            with open(filepath, 'r') as _fp:
                self.__in_text = _fp.readlines()
                return True
        except FileNotFoundError:
            print(F'"{filepath}" not found')
        return False

    def write_file(self, filepath: str) -> bool:
        """
        Return false if write fails
        """
        return self.__write_file(filepath, self.__out_text)

    def write_duplicates(self, filepath: str) -> bool:
        """
        Return false if write fails
        """
        return self.__write_file(filepath, self.get_duplicate_mods())

    def __write_file(self, filepath: str, text: List[str]) -> bool: # pylint: disable=no-self-use
        """
        Return false if write fails
        """
        try:
            with open(filepath, 'w') as _fp:
                _fp.writelines(text)
                return True
        except FileNotFoundError:
            print(F'"{filepath}" could not be written')
        return False

    def parse(self) -> None:
        """
        Parse all the lines in __in_text and then remove duplicate lines
        """
        self.__out_text = list()
        for line in self.__in_text:
            _out_line = self.__parse_line(line)
            self.__out_text.append(_out_line)
        # de-dupe the list
        self.__out_text = list(dict.fromkeys(self.__out_text))

    def remove_similar(self) -> None:
        """
        Remove lines that are most similar to the previous one, e.g.
        Livery file ESP2_ORECA03_161034 excluded from list on account of being too long
        Livery file ESP2_ORECA03_111040 excluded from list on account of being too long
        Livery file ESP2_ORECA03_121010 excluded from list on account of being too long
        """
        _not_similar = list()
        for i in range(len(self.__out_text)-1):
            _same, _diff = self._near_duplicate(self.__out_text[i], \
                self.__out_text[i+1])
            if _diff > 3:
                _not_similar.append(self.__out_text[i])
        _not_similar.append(self.__out_text[-1])
        self.__out_text = _not_similar

    def __parse_line(self, line: str) -> str:   # pylint: disable=no-self-use
        """ # pylint: disable=line-too-long
        Split at the first : to lose the timestamp/filename/line number, e.g.
           9.61s setup.cpp    1746: Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n
        becomes
        Livery file 15019BP_HURACAN_GT3 excluded from list on account of being too long\n
        """
        try:
            _res = line.split(':', 1)[1].strip() + '\n'
        except IndexError:  # the line didn't split
            _res = line
        return _res

    def _near_duplicate(self, line1: str, line2: str) -> Tuple[int, int]:   # pylint: disable=no-self-use
        """
        Return tokens same and different in the two lines
        """
        _delims = './\\=_-'
        for _d in _delims:
            line1 = line1.replace(_d, ' ')
            line2 = line2.replace(_d, ' ')
        _line1 = line1.split()
        _line2 = line2.split()
        _same = 0
        _diff = 0
        for i, _w in enumerate(_line1):
            if i < len(_line2):
                if _w == _line2[i]:
                    _same += 1
                else:
                    _diff += 1
            else:
                _diff += 1
        return _same, _diff

    def get_duplicate_mods(self) -> List[str]:
        r""" # pylint: disable=line-too-long
        Find all
        Duplicate vehfile detected & deleted from VehMan lists: C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.5\USF2000_12.VEH
        Tracks too? (None in the filter files I have)
        """
        _duplicates = list()
        for _line in self.__out_text:
            if _line.startswith('Duplicate vehfile detected & deleted from VehMan lists:'):
                _mod = _line.split(r'Installed')[1]    # Vehicles\USF2000_2016\1.5\USF2000_12.VEH
                _duplicates.append(split(_mod)[0][1:]+'\n') # Vehicles\USF2000_2016\1.5
        # de-dupe the list
        _duplicates = list(dict.fromkeys(_duplicates))
        return _duplicates

    def get_parsed_text(self) -> List[str]:
        """
        docstring
        """
        return self.__out_text

def main():
    """
    docstring
    """
    tr_o = TraceReader()
    _res = tr_o.read_file(TRACE_FILE)
    assert(_res)
    tr_o.parse()
    _res = tr_o.write_file(PARSED_FILE)
    assert(_res)
    tr_o.remove_similar()
    _res = tr_o.write_file(NO_SIMILAR_FILE)
    assert(_res)

    _res = tr_o.write_duplicates(DUPLICATES_FILE)
    assert(_res)

if __name__ == '__main__':
    main()

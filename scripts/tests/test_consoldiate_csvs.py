import unittest
import os
import filecmp

class TestConsolidateCsvs(unittest.TestCase):

    def setUp(self):
        # Run check file structure
        # pwd = ~/ilastik/scripts/tests
        # ../
        projectname = "testDir"
        userdir = "../../"
        uwid = "test_user"
        workingdir = userdir + "/" + uwid + "/"
        call = "../check_file_structure.sh " + projectname + " " + userdir + " " + uwid
        os.system(call)
        # /some_dir/test_user/out/testDir/
        self.outputDir = workingdir + "/out/" + projectname
        self.outputCSVPath = self.outputDir + "/out.csv"
        self.expected = "./expected_out.csv"


    def tearDown(self):
        # Remove output file made
        # os.remove(self.outputCSVPath)
        return

    # Check that for a given output directory with a known amount of csvs, consoldiate gets all the
    # desired output (all measurements and one header)
    # Inputs: (assumes that /out dir has segmentation already)
        # 210616_1%_DMSO_day_0_b7_seg.tif
        # 210616_1%_DMSO_day_0_c7_seg.tif
        # 210616_1%_DMSO_day_0_d7_seg.tif
    # Expected Output:
        # ./expected_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_something(self):
        call = "python3 ../consolidate_csvs.py " + self.outputDir + " " + self.outputCSVPath
        os.system(call)
        os.system("cat " + self.outputCSVPath)
        self.assertTrue(filecmp.cmp(self.expected, self.outputCSVPath))


if __name__ == '__main__':
    unittest.main()

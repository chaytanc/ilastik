import unittest
import os
import filecmp
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('../')
import consolidate_csvs as cc
import subprocess

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
        # Delete existing output before creating new
        os.remove(self.outputCSVPath)


    # def tearDown(self):

    # Check that for a given output directory with a known amount of csvs, consoldiate gets all the
    # desired output (all measurements and one header)
    # Inputs: (assumes that /out dir has segmentation already)
        # 210616_1%_DMSO_day_0_b7_table.csv
        # 210616_1%_DMSO_day_0_c7_table.csv
        # 210616_1%_DMSO_day_0_d7_table.csv
    # Expected Output:
        # ./expected_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_something(self):
        cc.main(self.outputDir, self.outputCSVPath)
        # call = "python3 ../consolidate_csvs.py " + self.outputDir + " " + self.outputCSVPath
        # os.system(call)
        print("Actual: \n")
        os.system("cat " + self.outputCSVPath)
        print("Expected: \n")
        os.system("cat " + self.expected)
        # Sort the rows because I'm not sure what order the rows should be in
        #XXX working here to do process substitution
        # subprocess.run(["diff", "<(sort {})", "<(sort {})"].format(self.expected, self.outputCSVPath))
        # subprocess.run(["diff", "<(sort {})".format(self.expected), "<(sort {})".format(self.outputCSVPath)])
        exit = os.system("./compare_output.sh {} {}".format(self.expected, self.outputCSVPath))
        # self.assertTrue(filecmp.cmp(self.expected, self.outputCSVPath))
        self.assertEqual(exit, 0)


if __name__ == '__main__':
    unittest.main()

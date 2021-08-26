import math
import unittest
import os
import sys

import pandas as pd

sys.path.append('../')
import format_data as fd

class TestFormatData(unittest.TestCase):

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
        self.outputCSV = self.outputDir + "/out.csv"
        self.output_path = self.outputDir + "/formatted_out.csv"
        self.expected = "./expected_formatted.csv"
        # Delete existing output before creating new
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


    # Check that for a given consolidated csv of data, we get the expected xlsx file back
    # Inputs: (assumes that /out dir has segmentation already)
        # expected_out.csv
            # 210616_1%_DMSO_day_0_b7_table.csv
            # 210616_1%_DMSO_day_0_c7_table.csv
            # 210616_1%_DMSO_day_0_d7_table.csv
    # Expected Output:
        # ./expected_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_something(self):
        fd.main(self.outputCSV, self.output_path)
        print("Actual: \n")
        os.system("cat " + self.output_path)
        print("Expected: \n")
        os.system("cat " + self.expected)
        # Sort the rows because I'm not sure what order the rows should be in
        # exit = os.system("./compare_output.sh {} {}".format(self.expected, self.output_path))
        # self.assertEqual(exit, 0)
        same_cols = self.compare_csv_cols(self.output_path, self.expected)
        self.assertTrue(same_cols)

    def compare_csv_cols(self, output, expected):
        exp = pd.read_csv(expected)
        out = pd.read_csv(output)
        same_cols = True
        for col in exp.columns:
            this_col = exp[col]
            other_col = out[col]
            for i, item in enumerate(this_col):
                other_item = other_col.iloc[i]
                if item != other_item:
                    if str(item).isnumeric() and not (math.isclose(float(item), float(other_item), abs_tol=0.2)):
                        same_cols = False
        return same_cols

    #XXX write a test which compares manual imagej results for a given test/validation set with actual


if __name__ == '__main__':
    unittest.main()

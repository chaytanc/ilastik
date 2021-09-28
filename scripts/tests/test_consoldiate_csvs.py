import math
import unittest
import os
import sys

import pandas as pd

sys.path.append('../')
import consolidate_csvs as cc

class TestConsolidateCsvs(unittest.TestCase):

    def setUp(self):
        # Run check file structure
        # pwd = ~/ilastik/scripts/tests
        # ../
        projectname = "testDir"
        userdir = "../../"
        uwid = "test_user"
        workingdir = userdir + "/" + uwid + "/"
        call = "../bootstrap/check_file_structure.sh " + projectname + " " + userdir + " " + uwid
        os.system(call)
        # /some_dir/test_user/out/testDir/
        self.outputDir = workingdir + "/out/" + projectname
        self.outputMultiDir = workingdir + "/out/testMulti"
        self.outputCSVPath = self.outputDir + "/out.csv"
        self.outputMultiCSVPath = self.outputMultiDir + "/actual_out.csv"
        self.expected = "./data/expected_out.csv"
        self.expectedMulti = "./data/expected_multi_out.csv"
        # Delete existing output before creating new
        if os.path.exists(self.outputCSVPath):
            os.remove(self.outputCSVPath)
        # Delete existing output before creating new
        if os.path.exists(self.outputMultiCSVPath):
            os.remove(self.outputMultiCSVPath)



    # Check that for a given output directory with a known amount of csvs, consoldiate gets all the
    # desired output (all measurements and one header)
    # Inputs: (assumes that /out dir has segmentation already)
        # 210616_DMSO_1%_b7_table.csv
        # 210616_1%_DMSO_day_0_c7_table.csv
        # 210616_1%_DMSO_day_0_d7_table.csv
    # Expected Output:
        # ./actual_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_output(self):
        cc.main(self.outputDir, self.outputCSVPath)

        # Sorts the rows because I'm not sure what order the rows should be in
        # exit = os.system("./compare_output.sh {} {}".format(self.expected, self.outputCSVPath))
        # self.assertEqual(exit, 0)
        self.sort_files(self.outputCSVPath, self.expected)
        same_cols = self.compare_csv_cols(self.outputCSVPath, self.expected)
        print("Actual: \n")
        os.system("cat " + self.outputCSVPath)
        print("Expected: \n")
        os.system("cat " + self.expected)
        print("end \n")
        self.assertTrue(same_cols)

    # Inputs: (assumes that /out dir has segmentation already)
        # 210616_DMSO_1%_b7_table.csv
        # 210616_1%_DMSO_day_0_c7_table.csv
        # 210616_1%_DMSO_day_0_d7_table.csv
    # Expected Output:
    # .../out/testMulti/actual_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_multi_output(self):
        cc.main(self.outputMultiDir, self.outputMultiCSVPath)

        # Sorts the rows because I'm not sure what order the rows should be in
        self.sort_files(self.outputMultiCSVPath, self.expectedMulti)
        same_cols = self.compare_csv_cols(self.outputMultiCSVPath, self.expectedMulti)
        print("Actual: \n")
        os.system("cat " + self.outputMultiCSVPath)
        print("Expected: \n")
        os.system("cat " + self.expectedMulti)
        print("end \n")
        self.assertTrue(same_cols)


    # Allows for numerical differences of +/- 0.01 in output due to different rounding mechanisms
    # of mathematical operations in Python
    def compare_csv_cols(self, output, expected):
        exp = pd.read_csv(expected)
        out = pd.read_csv(output)
        same_cols = True
        # Loop through all columns of each dataset
        for col in exp.columns:
            this_col = exp[col]
            other_col = out[col]
            # Check that they have the same number of values
            if len(this_col.values) != len(other_col.values):
                print("\n ERROR: Unequal number of values in column ", col, "\n expected: ", this_col.values,
                      " \n actual: ", other_col.values)
                return False

            # Compare each item in the column to the corresponding item in the other column
            for i, item in enumerate(this_col):
                # getting row this way causes row order agnostic behavior??
                other_item = other_col.iloc[i]
                # Check if numeric values are close enough
                if item != other_item:
                    same_cols = False
                    try:
                        if math.isclose(float(item), float(other_item), abs_tol=0.02):
                            print("\nClose enough... ", item, " and ", other_item)
                            same_cols = True
                    except ValueError as e:
                        print("\nConsidering ", item, " and ", other_item, " not equal")

                # Stop at first unequal columns that are still unequal after checking if numbers are close
                if not same_cols:
                    return False
        return same_cols


    # NOTE: modifies files passed in with the sorted lines version
    def sort_files(self, *files):
        for file in files:
            with open(file, "r") as f:
                lines = f.readlines()
                new_lines = sorted(lines, reverse=True)
            f.close()
            with open(file, "w") as f:
                f.seek(0)
                # f.truncate()
                # Overwrites
                for i in range(len(new_lines)):
                    f.write(new_lines[i])

                #XXX why is this necessary?? why wouldn't lines always be the same length as new lines
                # if len(lines) > len(new_lines):
                #     for i in range(len(new_lines), len(lines)):
                #         f.write(lines[i])


if __name__ == '__main__':
    unittest.main()

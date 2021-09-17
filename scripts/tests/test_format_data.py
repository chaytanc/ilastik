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
        projectname = "testDir"
        userdir = "../../"
        uwid = "test_user"
        workingdir = userdir + "/" + uwid + "/"
        call = "../check_file_structure.sh " + projectname + " " + userdir + " " + uwid
        os.system(call)
        # where to find the input for this test (the consolidated csv file)
        # /some_dir/test_user/out/testDir/
        self.outputDir = workingdir + "/out/" + projectname
        #self.outputCSV = self.outputDir + "/out.csv"
        # Uses hardcoded expected consolidated csv instead of relying on consoldiate_csvs to work
        self.outputCSV = "./expected_out.csv"
        self.output_standardCSV = "./expected_standard_out.csv"
        # where to put the actual output from running this test which we will compare with expected
        self.output_path = self.outputDir + "/actual_formatted_out.csv"
        # where to find the hard coded expected output of this test
        self.expected = "./expected_formatted.csv"
        self.expected_standard = "./expected_standard_formatted.csv"
        # This file scrambles 3uM concentration and 1% concentration for b7 and c7
        self.failed_expected_standard = "./failed_expected_standard_formatted.csv"
        # Delete existing output before creating new
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


    def tearDown(self):
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
    def test_ramila_format(self):
        fd.main(self.outputCSV, self.output_path, ramila_data=True)
        print("Actual: \n")
        os.system("cat " + self.output_path)
        print("Expected: \n")
        os.system("cat " + self.expected)
        same_cols = self.compare_csv_cols(self.output_path, self.expected)
        self.assertTrue(same_cols)


    # Check that for a given consolidated csv of data, we get the expected xlsx file back
    # FORMAT:
    # "day" {day number}/{date}_{treatment}_{concentration}_{id}_{optional_id}"_table.csv"
    # Inputs: (assumes that /out dir has segmentation already)
    # expected_out.csv
    # day_0/210616_ROCK_3uM_b7.csv
    # day_0/210616_DMSO_1%_c7_01_table.csv
    # day_0/210616_ROCK_100_d7_table.csv
    # Expected Output:
    # ./expected_standard_out.csv (not sure if order of processing is same, but went alphabetical)
    def test_standard_format(self):
        # Uses standard format
        fd.main(self.output_standardCSV, self.output_path, False)
        # Print output comparison
        print("Actual: \n")
        os.system("cat " + self.output_path)
        print("Expected: \n")
        os.system("cat " + self.expected_standard)
        # Compare
        same_cols = self.compare_csv_cols(self.output_path, self.expected_standard)
        self.assertTrue(same_cols)


    def test_failed_standard_format(self):
        fd.main(self.output_standardCSV, self.output_path, False)
        # Print output comparison
        print("Actual: \n")
        os.system("cat " + self.output_path)
        print("Expected: \n")
        os.system("cat " + self.failed_expected_standard)
        # Comparison should fail because failed_expected_standard has scrambled output
        same_cols = self.compare_csv_cols(self.output_path, self.failed_expected_standard)
        self.assertFalse(same_cols)


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

    #XXX write an accuracy test which compares manual imagej results for a given test/validation set with actual


if __name__ == '__main__':
    unittest.main()

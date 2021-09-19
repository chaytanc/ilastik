import math
import unittest
import os
import sys
sys.path.append('../')
import cleanup as cu


class TestFormatData(unittest.TestCase):

    def setUp(self):
        # Run check file structure
        projectname = "testDir"
        userdir = "../../"
        uwid = "test_user"
        workingdir = userdir + "/" + uwid + "/"
        call = "../bootstrap/check_file_structure.sh " + projectname + " " + userdir + " " + uwid
        os.system(call)
        # /some_dir/test_user/out/testDir/
        self.outputDir = workingdir + "/out/" + projectname
        self.output_csv = self.outputDir + "/out.csv"
        self.output_path = self.outputDir + "/formatted_out.csv"
        self.expected = "./expected_formatted.csv"
        call = "cp " + self.outputDir + "/../test_data/* " + self.outputDir + "/day_0/"
        os.system(call)


    # Check that cleanup.py recursively removes all csv and tifs that aren't the output and
    # are underneath the given output directory
    # Inputs: (assumes that /out/ dir has segmentation already)
        # expected_out.csv
            # 210616_1%_DMSO_day_0_b7_table.csv
            # 210616_1%_DMSO_day_0_c7_table.csv
            # 210616_1%_DMSO_day_0_d7_table.csv
    # Expected Output:
        # No .csv or tif files in any day X folders
    #XXX should also probably chekc that no files we want to keep in higher folders are deleted on accident
    def test_cleanup(self):
        cu.main(self.outputDir)
        # Look through files of outputDir and if any are csvs or tifs in day X folders that are also not an output file
        # then we have not removed all the desired files
        for root, foundSubdirs, files in os.walk(self.outputDir):
            for file in files:
                path = os.path.join(root, file)
                basedir = os.path.dirname(path)
                if "Day" in basedir or "day" in basedir:
                    # Check if the file is a csv or tif and isn't an output file
                    if (file.endswith(".csv") or file.endswith(".tif")) and file != self.output_csv and \
                            file != self.output_path:
                        print("Found ", file, ": test failed")
                        raise AssertionError("Not all csvs and tifs were removed from day X folders")


if __name__ == '__main__':
    unittest.main()

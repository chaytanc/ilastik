'''
This script will replace the first --project=... occurrence with --project={pixel_model} and the second with
the object model.
PARAMETERS:
    file_path: the location of the file which calls Ilastik headlessly whose lines you want to replace
    pixel_model: local path(s) to the pixel segmentation model which you want to use
    obj_model: local path(s) to the object detection model which you want to use

EFFECTS:
    Modifies the file at file_path by replacing the first --project line to use the pixel_model and the second
    --project line to use the obj_model specified.
'''
import argparse
import re

global ARGS
ARGS = None

# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("pixel_model")
    parser.add_argument("obj_model")
    return parser.parse_args()


# Tries to find scripts dir around where the model files were transferred to and if it does, looks for start.sh
# If start.sh is found, replaces --project "previous_pixel.ilp" lines to use --project "current_pixel.ilp" and
# --project "previous_object.ilp"
def replace_models(file_path, pixel_model, obj_model):
    # find auto_ilastik.sh --project matches
    pattern = re.compile(r'--project.*')
    new_file = ""
    with open(file_path, 'r') as f:
        match = 1
        for line in f:
            # Remove line ending before we do replacement
            line = line.strip()
            # replace first --project line match with pixel
            if match == 1:
                result = re.sub(pattern, "--project='" + pixel_model + "'", line)
            # replace second --project line match with object
            elif match == 2:
                result = re.sub(pattern, "--project='" + obj_model + "'", line)
            else:
                result = line
            # Check that a substitution was actually made
            if result is not line:
                # Add a backslash to the replaced line
                result += " \\"
                print("\nReplaced ", line, " with ", result)
                # Increment number of matches found
                match += 1
            # Add the potentially modified line to our new file
            new_file = new_file + result + "\n"
        # close file / save output
        f.close()
    fout = open(file_path, "w")
    fout.write(new_file)
    fout.close()


# A useless main function wrapping replace_models function because of possible functionality extension later
def main(file_path, pixel_model, obj_model):
    replace_models(file_path, pixel_model, obj_model)


if __name__ == "__main__":
    ARGS = parse_args()
    print("args: ", ARGS)
    main(ARGS.file_path, ARGS.pixel_model, ARGS.obj_model)

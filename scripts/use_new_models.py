'''
This script will take in any number of arguments, with at least two. The first is the location on the Hyak where
you want to transfer the files. The second, and potentially third, fourth, etc... arguments are the paths (relative to
your working directory) to the models you would like to transfer to that location on the Hyak. Technically, despite
being named use_new_models.py, you can transfer any type of file to any location on the Hyak. You
could also specify a directory instead of a file. You will need to separately ssh for each different file to
transfer it.
PARAMETERS:
    transferdir: the location on the Hyak where you want to transfer the files.
    uwid: your UW NetID which must have an account on the Hyak
    files*: local path(s) to files you want to transfer

EFFECTS:
#XXX todo
'''
import argparse
import os

global ARGS
ARGS = None

# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("transferdir")
    parser.add_argument("uwid")
    parser.add_argument("files", nargs='+')
    return parser.parse_args()


#XXX todo add support for editing the start.sh file with given models (also add flag that controls whether to do that)
#XXX todo turn in to a bash script because ffs python needs a module in order to


# Tries to find scripts dir around where the model files were transferred to and if it does, looks for start.sh
# If start.sh is found, replaces --project "previous_pixel.ilp" lines to use --project "current_pixel.ilp" and
# --project "previous_object.ilp"
def replace_start_models(hyakdir, pixel_model, obj_model):
    # find start.sh
    # replace --project lines
    # save file / scp over to hyak
    print()

def main(transferdir, uwid, files):
    transfer_path = uwid + "@klone.hyak.uw.edu:" + transferdir
    # exit_val = xxx
    # if exit_val == 0:
    #     print("Success! Transferred files ")


if __name__ == "__main__":
    ARGS = parse_args()
    print("args: ", ARGS)
    main(ARGS.transferdir, ARGS.uwid, ARGS.files)
import os
import sys
import ntpath
from pathlib import Path
import re

import pandas as pd

''' 
This script takes all csvs below the given outputdir and consolidates them into one csv with n+1 rows where
n is the number of csvs consolidated (there is a header row). The consolidated csv file path and filename is 
determined by the second parameter given. This script may be run locally or on the Hyak, but will be run on the
Hyak if run by the start.sh pipeline. It does not consolidate csv files with "out" anywhere in the name.

PARAMETERS: 
    outputdir: the path to the directory which contains csvs output from object detection
    ouputpath: the path of the destination of the consolidated csv file, including filename
    
USAGE: python3 consolidate_csvs.py {outputdir} {outputpath}
    Ex:
    python3 consolidate_csvs.py /gscratch/freedmanlab/uwid/out/testDir/ /gscratch/freedmanlab/uwid/out/testDir/out.csv
    Potentially useful commands: 
        pwd | sed 's/ /\\ /g' | pbcopy
        pbpaste | xargs python3 consolidate_csvs.py

EFFECTS:
This script takes the many individual output csvs from a given folder and
adds them to one csv as rows.  It adds a column called "filename" and a col
called "day". It renames all files in the directory to use underscores
rather than spaces. 
This script ignores the csv file ".*out.*csv"
It appends filename, day columns to each csv processed. For example, an image titled 
"210616_1%_DMSO_day_0_c7_table.csv"
has "210616_1%_DMSO_day_0_c7_table.csv,0" appended to the START of each row so that the first and second column
correspond to filename,day

PRECONDITIONS:
It assumes all the csvs in the directory given have the same column labels (first row of the file).
It assumes the directory containing the csvs is labeled with the day number,
typically as "/other directories/day 1/...csv files".
It assumes the parent directory named with the day has NO other numbers in the name.
It assumes the output of ilastik is stored in CSVS and that the output of formatting the data
is a .xlsx or any file that will not be processed / consolidated by this script.
In other words, it assumes there are no csvs under the directory passed as an argument that are not wanted
in the analysis of ilastik output. (HINT: perhaps store this and other formatting scripts in a directory called "scripts"
somewhere above the root of your cystic images)

OUTPUT:
The output is stored as the file specified by outputpath.
'''


# Removes spaces and puts in underscores for files
def rename_files(csv_dir):
    for filename in os.listdir(csv_dir):
        # print(filename)
        new_name = filename.replace(' ', '_')
        old_file_path = os.path.join(csv_dir, filename)
        new_file_path = os.path.join(csv_dir, new_name)
        os.rename(old_file_path, new_file_path)

    # Returns the path to the renamed file


def rename_file(file):
    print("Renaming ", file, " in consolidate_csvs.py")
    parts = os.path.split(file)
    filename = parts[1]
    csv_dir = parts[0]
    new_name = filename.replace(' ', '_')
    print("New name ", new_name)
    old_file_path = os.path.join(csv_dir, filename)
    new_file_path = os.path.join(csv_dir, new_name)
    os.rename(old_file_path, new_file_path)
    return new_file_path


# gets from sys.argv[0] / first arg passed to command
# Post condition: finds some csv files in the directory passed
def get_csvs(csv_dir):
    files = os.listdir(csv_dir)
    csv_files = [os.path.join(csv_dir, file) for file in files if file.endswith('.csv')]
    # Checks post condition that some csv files were found
    try:
        file1 = csv_files[0]
    except FileNotFoundError:
        raise FileNotFoundError("Could not find any csv files in ", csv_dir)

    return csv_files


# Looks in all directories below csv_dir for csv files and adds them to the
# csv file list if they aren't an out.csv type file
def get_csvs_recursive(csv_dir):
    csv_files = []
    # Excludes strings matching out.*\.csv regex pattern
    excluded_pattern = re.compile(r'.*out.*')
    # csv_files = [csv for csv in Path(csv_dir).rglob('*.csv')]
    for csv in Path(csv_dir).rglob('*.csv'):
        # print("csv stem: ", csv.stem)
        bad_csv = re.match(excluded_pattern, csv.stem)
        if bad_csv:
            print("Not consolidating ", csv.stem)
        else:
            # print("good csv: ", csv.stem)
            csv_files.append(csv)
    try:
        csv_files[0]
    except FileNotFoundError:
        raise FileNotFoundError("Could not find any csv files in " + str(csv_dir))
    return csv_files


# This method of getting the day assumes we are operating on a csv_dir that represents
# where the images are located, not above it
def get_day(csv_dir):
    parent_dir = os.path.basename(csv_dir)
    day = find_number(parent_dir)
    # Check grandparent if we don't find parent number
    if day == "":
        split_path = os.path.split(csv_dir)
        # print("Split path: ", split_path)
        split_again = os.path.split(split_path[0])
        grandparent_dir = split_again[1]
        print("Using grandparent ", grandparent_dir, " to find which day the images were taken")
        day = find_number(grandparent_dir)
    if day == "":
        raise NameError("Neither the parent nor grandparent directory " +
                        "indicated which day the images were taken.")

    return day


# This method of getting the day allows for passing in a root_dir above
# where the actual csv files are located


# USE WHEN PASSING FILES, NOT DIR PATH
def get_day_recursive(csv_file):
    # skip the file
    parent_dir = os.path.split(csv_file)[0]
    day = get_day_recursive_helper(parent_dir, 0)
    return day


# Checks up to 3 directories up for "day_X" folder; gives up after that
def get_day_recursive_helper(csv_dir, height):
    split_path = os.path.split(csv_dir)
    parent_dir = split_path[1]
    day = find_number(parent_dir)
    # Check grandparent if we don't find parent number
    if day == "" and height < 4:
        print("Using ", parent_dir, " to find which day the images were taken")
        day = get_day_recursive_helper(split_path[0], height + 1)
    # Inv: Gets here if height is greater than 4 or we found non "" day
    if day == "":
        raise NameError("Neither the parent nor grandparent directory " +
                        "indicated which day the images were taken.")

    return day


# Checks the given path for a number and returns the first one found
def find_number(path):
    number = ""
    for word in path.split():
        if word.isdigit():
            number = word
    if number == "":
        for word in path.split("_"):
            if word.isdigit():
                number = word
    return number


def consolidate_csvs(csv_files, day):
    output_file = "out_" + day + '.csv'
    fout = open(output_file, "a")

    header = _write_first_file(fout, csv_files, day)

    # Slicing out the first file that we manually wrote
    other_files = csv_files[2:]
    # now the rest, no headers:    
    for csv in other_files:
        with open(csv, "r+") as f:
            # supposed_header = f.readline()
            # skip headers
            f.readline()

            # each line is a row
            for line in f:
                # Only write lines that are not the header
                if line != header:
                    # print("line before \n", line)
                    # need to append filename to the csv output to the front
                    # also appends day column
                    # processed_line = ntpath.basename(csv) + "," + day + "," + line
                    processed_line = _process_line(csv, day, line)
                    print("new line \n", processed_line)
                    fout.write(processed_line)
            f.close()  # not really needed, closes input file

    print("Finished writing to output_file")
    fout.close()  # closes output file


def consolidate_csvs_recursive(csv_files, out_path):
    fout = open(out_path, "a")

    header = _write_first_file(fout, csv_files)

    # Slicing out the first file that we manually wrote
    other_files = csv_files[1:]
    # now the rest, no headers:    
    for csv in other_files:
        new_csv_path = rename_file(csv)
        day = get_day_recursive(new_csv_path)
        with open(new_csv_path, "r+") as f:
            # new_csv unused because it directly modifies file we're reading instead of making a new one
            new_csv, header = _fix_headers(f, header)
            # skip headers
            new_csv.readline()

            # each line is a row
            # for line in f:
            for line in new_csv.readlines():
                # Only write lines that are not the header
                if line != header:
                    # print("line before \n", line)
                    # appends filename and day columns to the csv output to the front
                    processed_line = _process_line(csv, day, line)
                    # print("new line \n", processed_line)
                    fout.write(processed_line)
            f.close()  # not really needed, closes input file

    print("Finished writing to out_path, ", out_path)
    fout.close()  # closes output file


# Whatever the first header contained is the maximum information we can use for the headers going forward
# Precondition: While the header columns may differ, the file must have at least the columns that
# current_header_line has
# Returns: reordered file and reordered header as a tuple
def _fix_headers(file, current_header_line):
    # read file in to pandas df
    csv = pd.read_csv(file)
    # read header into pandas df
    temp = _line_to_csv(current_header_line)
    header_df = pd.read_csv(temp)
    # print("FILE COLS: ", csv.columns)
    # print("HEADER COLS: ", header_df.columns)
    # print("")

    # Compare header differences, take the left join of the header_df and csv headers, reindex dfs accordingly
    new_header, new_csv = _reindex_df_headers(header_df, csv)

    # Write fixed header df to csv
    new_csv.to_csv(file.name, index=False)
    # Read file as IO thing instead of pandas dataframe to return in same format we received it
    nf = open(file.name, "r+")

    # Get new_header as a string
    new_header.to_csv('./temp.csv', index=False)
    # Write to new_header the rearranged header we stored in temp.csv
    with open('./temp.csv', 'r') as new_header:
        new_header = new_header.readline()

    # Cleanup
    os.remove('./temp.csv')

    # noinspection PyRedundantParentheses
    return (nf, new_header)


# Effects: takes the left merge of column headers and then reindexes both dataframes based on that.
#       Should not modify old_header_df, but may modify and rearrange contents of new_header_df.
# Return: reindexed (old_header_df, new_header_df)
def _reindex_df_headers(old_header_df, new_header_df):
    # compare headers
    # if file has more header col(s) than current_header_line, deletes those
    same_cols = old_header_df.columns.intersection(new_header_df.columns)
    # Cols in header_df and not in csv
    diff_cols = old_header_df.columns.difference(new_header_df.columns)
    if len(diff_cols.values) != 0:
        print("FOUND mismatched headers; values in previous header not in current file: ", diff_cols.values)
    cols_df = same_cols.join(diff_cols, how="outer")
    cols_df = cols_df.reindex(old_header_df.columns)
    cols = cols_df[0].values
    # if different order, rearrange file headers to be same order as current_header_line
    old_header_df = old_header_df.reindex(columns=cols)
    # may add column that didn't exist before --> Precondition; don't have that.
    assert(len(old_header_df.columns) <= len(new_header_df.columns))
    new_header_df = new_header_df.reindex(columns=cols)
    return (old_header_df, new_header_df)

def _line_to_csv(line):
    with open("./temp.csv", "w") as f:
        f.write(line)
    f.close()
    return "./temp.csv"


# Modifies fout by adding the header and appending the filename to the
# csv list of headers
# Assumes that all csvs it is consolidating have the same header -- can deal with it if not, but data may be lost
# Returns the header from the first file
def _write_first_file(fout, csv_files):
    # first file, gets the headers
    new_path = rename_file(csv_files[0])
    first_file = open(new_path)
    header = first_file.readline()
    # adding filename and day column to output
    new_header = "filename,day," + header
    print("new_header \n", new_header)
    fout.write(new_header)
    day = get_day_recursive(new_path)
    for line in first_file:
        print("line before \n", line)
        # add filename and day to the file
        # first_filename = ntpath.basename(csv_files[0])
        # line_after = first_filename + line
        line_after = _process_line(new_path, day, line)
        assert (line != line_after)
        print("line after \n", line_after)
        fout.write(line_after)
    return header


# Adds filename and day to the line as two new front columns
# Pass in the csv to get the filename from and the line / row of data we're editing
def _process_line(csv, day, line):
    processed_line = ntpath.basename(csv) + "," + day + "," + line
    return processed_line


# Moves any existing files at the specified output csv or xlsx to a .copy extension and saves
# the new analysis files as out.csv or .xlsx
def move_existing_output_files(*paths_to_check):
    for path in paths_to_check:
        if os.path.exists(path):
            new = path + ".copy"
            os.rename(path, new)


def main(csv_dir, out_path):
    move_existing_output_files(out_path)
    csvs = get_csvs_recursive(csv_dir)
    consolidate_csvs_recursive(csvs, out_path)


if __name__ == "__main__":
    # print("args: ", str(sys.argv))
    csv_dir = sys.argv[1]
    out_path = sys.argv[2]

    main(csv_dir, out_path)

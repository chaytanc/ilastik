import os
import sys
import ntpath

#XXX todo: does this work on windows and will I need it to do so if I run 
# on hyak instead of individual pcs
''' 
USAGE: python3 consolidate_csvs.py {path to dir containing output csvs}
    Ex:
    python3 consolidate_csvs.py ~/Desktop/lab/freedman/cysts/object_det/output
    Useful command: pwd | sed 's/ /\\ /g' | pbcopy

EFFECTS:
This script takes the many individual output csvs from a given folder and
adds them to one csv as rows.  It adds a column called "filename" and a col
called "day". It renames all files in the directory to use underscores
rather than spaces.

PRECONDITIONS:
It assumes all the csvs in the directory given have the same headers.
It assumes the directory containing the csvs is labeled with the day number,
typically as "/other directories/day 1/...csv files".
It assumes the parent directory named with the day has NO other numbers in the name.

OUTPUT:
The output is stored as out_{day}.csv in the directory from which this script was
run.
'''

# Removes spaces and puts in underscores for files
def rename_files(csv_dir):
    for filename in os.listdir(csv_dir):
        #print(filename)
        new_name = filename.replace(' ', '_')
        old_file_path = os.path.join(csv_dir, filename)
        new_file_path = os.path.join(csv_dir, new_name)
        os.rename(old_file_path, new_file_path) 


# gets from sys.argv[0] / first arg passed to command
# Post condition: finds some csv files in the directory passed
def get_csvs(csv_dir):
    files = os.listdir(csv_dir)
    csv_files = [ os.path.join(csv_dir, file) for file in files if file.endswith('.csv') ]
    # Checks post condition that some csv files were found
    try:
        file1 = csv_files[0]
        print("First csv file: " + file1)
    except:
        raise FileNotFoundError("Could not find any csv files in ", csv_dir)

    return csv_files

def get_day(csv_dir):
    parent_dir = os.path.basename(csv_dir)
    print("Parent dir: ", parent_dir)
    day = find_number(parent_dir)
    # Check grandparent if we don't find parent number
    if day == "":
        split_path = os.path.split(csv_dir)
        print("Split path: ", split_path)
        split_again = os.path.split(split_path[0])
        grandparent_dir = split_again[1]
        print("Using grandparent ", grandparent_dir, " to find which day the images were taken")
        #XXX put in an input check whether to continue processing or not
        day = find_number(grandparent_dir)
    if day == "":
        raise NameError("Neither the parent nor grandparent directory " +\
                "indicated which day the images were taken.")

    return day

# Checks the given path for a number and returns the first one found
def find_number(path):
    number = ""
    for word in path.split():
        if word.isdigit():
            number = word
    return number


def consolidate_csvs(csv_files, day):
    output_file = "out_" + day + '.csv'
    fout=open(output_file,"a")

    header = _write_first_file(fout, csv_files, day)
    
    # Slicing out the first file that we manually wrote
    other_files = csv_files[2:]
    # now the rest, no headers:    
    for csv in other_files:
        with open(csv, "r+") as f:
            #supposed_header = f.readline()
            # skip headers
            f.readline()

            # each line is a row
            for line in f:
                # Only write lines that are not the header
                if(line != header):
                    #print("line before \n", line)
                    # need to append filename to the csv output to the front
                    # also appends day column
                    #processed_line = ntpath.basename(csv) + "," + day + "," + line
                    processed_line = _process_line(csv, day, line)
                    print("new line \n", processed_line)
                    fout.write(processed_line)
            f.close() # not really needed, closes input file

    print("Finished writing to output_file") 
    fout.close() # closes output file

# Modifies fout by adding the header and appending the filename to the
# csv list of headers
# Returns the header from the first file
def _write_first_file(fout, csv_files, day):
    # first file, gets the headers
    first_file = open(csv_files[0])
    header = first_file.readline()
    # adding filename and day column to output
    #new_header = "filename," + header
    new_header = "filename,day," + header
    print("new_header \n", new_header)
    fout.write(new_header)
    for line in first_file:
        print("line before \n", line)
        # add filename and day to the file
        #first_filename = ntpath.basename(csv_files[0])
        #line_after = first_filename + line
        line_after = _process_line(csv_files[0], day, line)
        assert(line != line_after)
        print("line after \n", line_after)
        fout.write(line_after)
    return header

# Adds filename and day to the line as two new front columns
# Pass in the csv to get the filename from and the line / row of data we're editing
def _process_line(csv, day, line):
    processed_line = ntpath.basename(csv) + "," + day + "," + line
    return processed_line

if __name__ == "__main__":
    #for i, arg in enumerate(sys.argv):
    print("args: ", str(sys.argv))
    csv_dir = sys.argv[1]
    rename_files(csv_dir)
    csvs = get_csvs(csv_dir)
    day = get_day(csv_dir)
    consolidate_csvs(csvs, day)

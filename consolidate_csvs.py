import os
import sys
import ntpath

#TODO add function to add column of image name to csv

# Removes spaces and puts in underscores for files
def rename_files(csv_dir):
    for filename in os.listdir(csv_dir):
        #print(filename)
        new_name = filename.replace(' ', '_')
        old_file_path = os.path.join(csv_dir, filename)
        new_file_path = os.path.join(csv_dir, new_name)
        os.rename(old_file_path, new_file_path) 

# gets from sys.argv[0] / first arg passed to command
def get_csvs(csv_dir):
    files = os.listdir(csv_dir)
    csv_files = [ os.path.join(csv_dir, file) for file in files if file.endswith('.csv') ]
    return csv_files

def consolidate_csvs(csv_files):
    fout=open("out.csv","a")

    try:
        file1 = csv_files[0]
        print("First csv file: " + file1)
    except:
        print("Could not find any csv files")

    header = _write_first_file(fout, csv_files)
    
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
                    print("line before \n", line)
                    # need to append filename to the csv output to the front
                    filename_line = ntpath.basename(csv) + "," + line
                    print("line after \n", filename_line)
                    fout.write(filename_line)
            f.close() # not really needed, closes input file

    #XXX pass in output csv
    print("Finished writing to out.csv") 
    fout.close() # closes output file

# Modifies fout by adding the header and appending the filename to the
# csv list of headers
# Returns the header from the first file
def _write_first_file(fout, csv_files):
    # first file, gets the headers
    first_file = open(csv_files[0])
    header = first_file.readline()
    # adding filename column to output
    new_header = "filename," + header
    print("new_header \n", new_header)
    fout.write(new_header)
    for line in first_file:
        print("line before \n", line)
        first_filename = ntpath.basename(csv_files[0])
        line_after = first_filename + line
        assert(line != line_after)
        print("line after \n", line_after)
        fout.write(line_after)
    return header

if __name__ == "__main__":
    #for i, arg in enumerate(sys.argv):
    print("args: ", str(sys.argv))
    csv_dir = sys.argv[1]
    rename_files(csv_dir)
    csvs = get_csvs(csv_dir)
    consolidate_csvs(csvs)

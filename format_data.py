import pandas as pd
import sys
import os

'''
#XXX todo
USAGE: python3 format_data.py {input csv}

{input csv} is the consolidated csv with all the data from Ilastik batch 
    processing object detection. It will typically be named out_{day}.csv
    as processed by consolidate_csvs.py.
    
PRECONDITIONS:
    Assumes that row entries in the input csv are unique. There should be 
    no duplicate treatments on the same day.

EFFECTS:
    Formats the data from all the processed csv files is filtered for 
    just the entries detecting "cystanoids" and not other labels
    like background. Then the area and intensity are found for 

OUTPUT:
    modified_{input csv}.csv is a more readable and organized verison
    of the input csv.

'''

#col_headers = ["Treatment", "Well", "Day", "Area", "Diameter", "Mean Intensity"]
#louisa_col_headers = ["Treatment", "Concentration", "ID", "Day", "Area", "Intensity"]

whose_data = "LOUISA"
#whose_data = "RAMILA"

# old_headers =filename	object_id	timestep	labelimage_oid	User Label	Predicted Class	Probability of bkgrd	Probability of cystanoid	Minimum intensity_0	Minimum intensity_1	Minimum intensity_2	Maximum intensity_0	Maximum intensity_1	Maximum intensity_2	Size in pixels	Radii of the object_0	Radii of the object_1	Variance of Intensity_0	Variance of Intensity_1	Variance of Intensity_2	Mean Intensity_0	Mean Intensity_1	Mean Intensity_2	Diameter	Bounding Box Minimum_0	Bounding Box Minimum_1	Bounding Box Maximum_0	Bounding Box Maximum_1	Center of the object_0	Center of the object_1 

# new old headers same as before but with filename day... instead of filename...


def format_data(df):
    # get cystanoid prediction rows
    print("out.csv: ", df)
    cystanoid_rows = df.loc[df["Predicted Class"] == "cystanoid"].reset_index()
    filename_df = cystanoid_rows.loc[:,"filename"]
    #print("filename_df : ", filename_df)
    with_file_cols_df = _parse_filenames(filename_df)
    #print("with file info df: ", with_file_cols_df)
    add_relevant_info(with_file_cols_df, cystanoid_rows)
    #print("improved df: ", improved_df)
    well_dfs = _get_unique_wells(with_file_cols_df)
    get_full_csv(well_dfs)

def format_louisa_data(df):
    # get cystanoid prediction rows
    print("out.csv: ", df)
    cystanoid_rows = df.loc[df["Predicted Class"] == "cystanoid"].reset_index()
    filename_df = cystanoid_rows.loc[:,"filename"]
    #print("filename_df : ", filename_df)
    with_file_cols_df = _parse_louisa_filenames(filename_df)
    add_days_column(with_file_cols_df, cystanoid_rows)
    #print("with file info df: ", with_file_cols_df)
    add_relevant_info_multi(with_file_cols_df, cystanoid_rows)
    output = "./excel_out.xlsx"
    with_file_cols_df.to_excel(output)
    print("Success! saved output to ", output)

# Should make a df that has treatment column, wellname column, and day column
# and merge with other df
# PRESUMED FILENAME FORMAT:
# 210623_control_day_7_f2_table.csv
# date_treatment_"day"_day_well_"table.csv"
# Headers to add --> ["Treatment", "Well", "Day"]
def _parse_filenames(filename_df):

    treatments = []
    wells = []
    days = []

    for filename in filename_df:
        items = filename.split("_")
        if items[2] ==  "DMSO":
            treatments.append(items[1] + items[2])
            wells.append(items[5])
            days.append(items[4])
        else:
            treatments.append(items[1])
            wells.append(items[4])
            days.append(items[3])
    new_df = pd.DataFrame(treatments)
    new_df.columns = ["Treatment"]
    new_df["Well"] = wells 
    new_df["Day"] = days
    return new_df

# PRESUMED FILENAME FORMAT:
# day 14/ROCK_5_uM_09_table.csv
# "day" {day number}/{treatment}_{id}_"table.csv"
# Will consider treatment and id one field just called treatment
# Headers to add --> ["Treatment"]
# need to later add the headers  ["Day X Area", "Day X Intensity"]
# PRECONDITION: filename must at least contain treatment, id, and table.csv.
# concentration, I suppose, is optional
def _parse_louisa_filenames(filename_df):
    treatments = []
    concentrations = []
    ids = []

    for filename in filename_df:
        items = filename.split("_")
        try:
            #print(items, "length: ", len(items))
            if (len(items) < 3):
                raise NameError("The filename " + filename + \
                        " does not contain enough information")
            # if length == 3 then no concentration (ie dmso) add none to concentration
            elif (len(items) == 3):
                concentrations.append(None)
            else:
                concentrations.append(items[1])

            treatments.append(items[0])
            # second to last element is the id
            ids.append(items[-2])
        except NameError as e:
            print("Exception: ", e)
            print("ERROR: Skipping file ", filename, " beceause it does not have "+\
                "enough information")
            continue
    new_df = pd.DataFrame(treatments)
    new_df.columns = ["Treatment"]
    new_df["Concentration"] = concentrations
    new_df["ID"] = ids
    return new_df

def add_days_column(in_prog_df, initial_df):
    in_prog_df["Day"] = initial_df["day"]

# MULTI-INDEXED

def add_relevant_info_multi(in_prog_df, initial_df):
    areas = initial_df.loc[:,'Size in pixels']
    intensities = initial_df.loc[:,'Mean Intensity_0']
    in_prog_df.loc[:,'Area'] = pd.Series(areas, index=in_prog_df.index)
    in_prog_df.loc[:,'Mean Intensity'] = pd.Series(intensities, index=in_prog_df.index)
    # Outer index (treatment, concentration, id should all have same # of unique occurences)
    # inner index -> day
    in_prog_df.set_index(["Treatment", "Concentration", "ID", "Day"], inplace=True)
    in_prog_df.sort_index(inplace=True)
    print("df, multi-indexed: ", in_prog_df)


# Modifies in_prog_df
# adds area, diameter, mean intensity info to the given dataframe
def add_relevant_info(in_prog_df, initial_df):
    print("initial df: ", initial_df)
    areas = initial_df.loc[:,'Size in pixels']

    print("Areas: ", areas)
    diameters = initial_df.loc[:,'Diameter']
    intensities = initial_df.loc[:,'Mean Intensity_0']
    # copy the initial_df so we can add some stuff to it
    in_prog_df.loc[:,'Area'] = pd.Series(areas, index=in_prog_df.index)
    in_prog_df.loc[:,'Diameter'] = pd.Series(diameters, index=in_prog_df.index)
    in_prog_df.loc[:,'Mean Intensity'] = pd.Series(intensities, index=in_prog_df.index)

# returns well_df_dict, a dictionary with keys as unique well names and values of a list of 
# the rows corresponding to those well names
def _get_unique_wells(improved_df):
    
    well_df_dict = {}
    wells = improved_df.loc[:,"Well"]
    for well in wells:
        row = improved_df.loc[improved_df['Well'] == well]
        row["Day"] = pd.to_numeric(row["Day"])
        row = row.sort_values("Day")
        well_df_dict[well] = row
    return well_df_dict

# writes full csv to out.csv, merging all the data from each well into one df
def get_full_csv(well_df_dict):
    # Concatenates all the individual dataframes representing each well's data
    big_df = pd.concat(list(well_df_dict.values()))
    print("final df: ", big_df)
    # write to csv
    big_df.to_csv("modified_out.csv")

#XXX working here to add fold change column based on (last day - first day) / first day
def _calculate_fold_change(improved_df):
    fold_changes = []
    #  for each unique treatment, conc, id, get days and areas
    # fold change is latest day - earliest day / latest day
    # put fold change for all cols of that unique treat, conc, id and multi index

if __name__ == "__main__":
    print("args: ", str(sys.argv))
    csv_file = sys.argv[1]
    df = pd.read_csv(csv_file)
    if whose_data == "LOUISA":
        format_louisa_data(df)
    if whose_data == "RAMILA":
        format_data(df)


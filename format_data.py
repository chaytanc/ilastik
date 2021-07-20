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

col_headers = ["Treatment", "Well", "Day", "Area", "Diameter", "Mean Intensity"]
#new_col_headers = ["Treatment", "Concentration", "ID", "Area Day 0", "Area Day ...", "Mean Intensity Day ...", ]
new_new_col_headers = ["Treatment", "Concentration", "ID", "Day", "Area", "Intensity"]

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
    improved_df = add_relevant_info(with_file_cols_df, cystanoid_rows)
    #print("improved df: ", improved_df)
    well_dfs = _get_unique_wells(improved_df)
    #well_dfs = get_well_dfs(improved_df)
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
    with_file_cols_df.to_excel("./excel_out.xlsx")
    #print("improved df: ", improved_df)


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
        #print("filename ", filename)
        items = filename.split("_")
        if items[2] ==  "DMSO":
            treatments.append(items[1] + items[2])
            wells.append(items[5])
            days.append(items[4])
        else:
            treatments.append(items[1])
            wells.append(items[4])
            days.append(items[3])
    #print("treatments: ", treatments)
    #print("wells ", wells)
    #print("days ", days)
    new_df = pd.DataFrame(treatments)
    new_df.columns = ["Treatment"]
    new_df["Well"] = wells 
    new_df["Day"] = days
    return new_df

#XXX working here to format Louisa output
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
            print(items, "length: ", len(items))
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

# Not "TIDY" attempt

## Makes a new column for each measurement and each separate day it was measured
## ie a column called Area Day 0, Area Day 7...
## Initial df comes from ilastik output, improved_df refers to df constructed after 
## filename parsing but missing measurements
##XXX workign here to format df
##XXX TODO: merge function to get rid of None values everywhere in area, intensity cols
#def add_relevant_info_by_day(improved_df, initial_df):
#
#    _add_measurement_headers(improved_df)
#    
#    # Should have Area Day... by now
#    headers = improved_df.columns
#    for row in initial_df:
#        # get values from initial_df for the given row
#        day = row["Day"]
#        area = row["Size in pixels"]
#        intensity = row["Mean Intensity_0"]
#
#        # match day to correct area column (by splitting
#        # header, getting number and checking if equal to 
#        # day # column)
#        area_col = _get_matching_col_by_day(headers, "Area", day)
#        intensity_col = _get_matching_col_by_day(headers, "Intensity", day)
#        
#        # get treatment for the given row --> don't need to do this, should be 
#        # able to assume that row order stays the same between the improved df and initial_df
#
#        # put area in correct area column in the row
#        # corresponding to the treatment from inital_df / just same row
#        improved_df.at[row.index, area_col] = area
#        improved_df.at[row.index, intensity_col] = intensity
#
## Adds a column per measurement per day
#def _add_measurement_headers(improved_df):
#
#    days = _get_unique_days(improved_df)
#    
#    # for unique day 
#    for day in days:
#        area_header = "Area, Day " + day
#        intensity_header = "Mean Intensity, Day " + day
#        # add empty cols per measurement per day
#        improved_df[area_header] = None
#        improved_df[intensity_header] = None
#    print("improved improved df: ", improved_df)
#    #XXX not necessary return b/c modifying directly???
#    #return improved_df
#
## Measurement type is something like "Area" or "Intensity"
#def _get_matching_col_by_day(columns, measurement_type, day):
#    possible_matches = [header for header in \
#            columns if measurement_type in header]
#    matching_headers = [h for h in possible_matches \
#            if day in h]
#    #XXX could there be multiple matches? shouldn't be
#    assert matching_headers.length == 1
#    return matching_headers[0]
#    
#
## NOTE: this makes the program flexible to the number of days for which the cysts
## are imaged (can do 0,1,3,7,14 like Ramila or 0,7,14 like Louisa)
## I know there are more efficient ways to do this, but n is small so whatever
#def _get_unique_days(df):
#    days_df = df["day"]
#    unique_days = set(days_df)
#    return unique_days
#
#
##XXX assumes all csvs have been merged into one big holy dataset and will merge rows
## with same treatment to fill holes (ie there is one row with null for day 0, day 7, but
## not null 14 which needs to merge w one row with null day 7, 14 etc..)
## big_df is the dataframe with all measurement columns but with gaps
#def merge_same_treatment_csvs(big_df):
#    df = df.groupy(["Treatment", "ID", "Concentration"])["

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


# adds area, diameter, mean intensity info to the given dataframe
def add_relevant_info(in_prog_df, initial_df):
    print("initial df: ", initial_df)
    areas = initial_df.loc[:,'Size in pixels']
    #print("Areas: ", areas)
    diameters = initial_df.loc[:,'Diameter']
    intensities = initial_df.loc[:,'Mean Intensity_0']
    # copy the initial_df so we can add some stuff to it
    in_prog_df.loc[:,'Area'] = pd.Series(areas, index=in_prog_df.index)
    in_prog_df.loc[:,'Diameter'] = pd.Series(diameters, index=in_prog_df.index)
    in_prog_df.loc[:,'Mean Intensity'] = pd.Series(intensities, index=in_prog_df.index)
    #in_prog_df['Area'] = areas
    #in_prog_df['Diameter'] = diameters
    #in_prog_df['Mean Intensity'] = intensities
    #XXX return is redundant since this is a mutable data structure
    return in_prog_df

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

if __name__ == "__main__":
    print("args: ", str(sys.argv))
    csv_file = sys.argv[1]
    df = pd.read_csv(csv_file)
    #format_data(df)
    format_louisa_data(df)


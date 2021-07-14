import pandas as pd
import sys
import os


headers = ["Treatment", "Well", "Day", "Area (pixels)", "Diameter", "Mean Intensity"]

# old_headers =filename	object_id	timestep	labelimage_oid	User Label	Predicted Class	Probability of bkgrd	Probability of cystanoid	Minimum intensity_0	Minimum intensity_1	Minimum intensity_2	Maximum intensity_0	Maximum intensity_1	Maximum intensity_2	Size in pixels	Radii of the object_0	Radii of the object_1	Variance of Intensity_0	Variance of Intensity_1	Variance of Intensity_2	Mean Intensity_0	Mean Intensity_1	Mean Intensity_2	Diameter	Bounding Box Minimum_0	Bounding Box Minimum_1	Bounding Box Maximum_0	Bounding Box Maximum_1	Center of the object_0	Center of the object_1 


def format_data(df):
    #XXX make new headers + add to final df
    #df.columns = 
    # get cystanoid prediction rows
    cystanoid_rows = df.loc[df["Predicted Class"] == "cystanoid"]
    filename_df = cystanoid_rows["filename"]
    with_file_cols_df = _parse_filenames(filename_df)
    improved_df = add_relevant_info(with_file_cols_df)
    well_dfs = get_well_dfs(improved_df)
    get_full_csv(well_dfs)


# Should make a df that has treatment column, wellname column, and day column
# and merge with other df
# PRESUMED FILENAME FORMAT:
# 210623_control_day_7_f2_table.csv
# date_treatment_"day"_day_well_"table.csv"
# Headers to add --> ["Treatment", "Well", "Day"]
def _parse_filenames(filename_df):

    #XXX how to merge columns with dataframe
    treatments = []
    days = []
    wells = []

    for filename in filename_df:
        print("filename ", filename)
        items = filename.split("_")
        treatments.append(items[1])
        days.append(items[3])
        wells.append(items[4])
    print("treatments: ", treatments)
    print("days ", days)
    print("wells ", wells)
    tr = pd.DataFrame(treatments)
    days = pd.DataFrame(days)
    wells = pd.DataFrame(wells)
    new_df = pd.merge(tr, days)
    new_df = pd.merge(new_df, wells)
    return new_df

# adds area, diameter, mean intensity info to the given dataframe
def add_relevant_info(initial_df):
    # copy the initial_df so we can add some stuff to it
    new_df = pd.DataFrame(initial_df)
    new_df['Area'] = pd.Series(initial_df['Size in pixels'])
    new_df['Diameter'] = pd.Series(initial_df['Diameter'])
    new_df['Mean Intensity'] = pd.Series(initial_df['Mean Intensity_0'])
    #XXX return is redundant since this is a mutable data structure
    return new_df

# improved_df is a df with filename parsed into separate columns and 
# with just area, mean intensity, etc / groomed data
def get_well_dfs(improved_df):
    # {well name: [rows]
    well_df_dict = _get_unique_wells(improved_df)
    print("well rows: ", well_df_dict.keys()[0])
    # loop through rows in improved_df
    for well, well_dict in well_df_dict:
        well_df = pd.DataFrame(well_dict)
        # sorts by days for each well
        well_df.sort_values(by = "Day")
        # sub in a pandas dataframe for the list of rows that we had
        # cause I do what I want because Python isn't typed and I don't have to make 
        # a different datastructure
        well_df_dict[well] = well_df

    return well_df_dict
# then just concat / merge well_dfs together to get full df again and write out to csv

# returns well_df_dict, a dictionary with keys as unique well names and values of a list of 
# the rows corresponding to those well names
def _get_unique_wells(improved_df):
    
    well_dict = {}
    for row in improved_df:
        well = row["Well"]
        if well in well_dict.keys(): 
            well_dict[well].append(row)
        else:
            well_dict[well] = [row]
    return well_dict

# writes full csv to out.csv, merging all the data from each well into one df
def get_full_csv(well_df_dict):
    
    big_df = pd.DataFrame()
    for df in well_df_dict:
        big_df = pd.merge(big_df, df)
    # write to csv
    big_df.to_csv("modified_out.csv")

if __name__ == "__main__":
    print("args: ", str(sys.argv))
    csv_file = sys.argv[1]
    #XXX not sure we want this rn, may want to construct a diff df
    # w desired headers rather than altering original
    #df = pd.read_csv(csv_file, headers=None)
    df = pd.read_csv(csv_file)
    format_data(df)


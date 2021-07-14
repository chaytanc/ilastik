import pandas as pd
import sys
import os


col_headers = ["Treatment", "Well", "Day", "Area", "Diameter", "Mean Intensity"]

# old_headers =filename	object_id	timestep	labelimage_oid	User Label	Predicted Class	Probability of bkgrd	Probability of cystanoid	Minimum intensity_0	Minimum intensity_1	Minimum intensity_2	Maximum intensity_0	Maximum intensity_1	Maximum intensity_2	Size in pixels	Radii of the object_0	Radii of the object_1	Variance of Intensity_0	Variance of Intensity_1	Variance of Intensity_2	Mean Intensity_0	Mean Intensity_1	Mean Intensity_2	Diameter	Bounding Box Minimum_0	Bounding Box Minimum_1	Bounding Box Maximum_0	Bounding Box Maximum_1	Center of the object_0	Center of the object_1 


def format_data(df):
    #XXX make new headers + add to final df
    #df.columns = 
    # get cystanoid prediction rows
    print("out.csv df: ", df)
    cystanoid_rows = df.loc[df["Predicted Class"] == "cystanoid"].reset_index()
    print("cystanoid rows: ", cystanoid_rows)
    #XXX does this filename col access alter underlying cystanoid rows? super weird
    filename_df = cystanoid_rows.loc[:,"filename"]
    print("cystanoid rows 2: ", cystanoid_rows)
    print("filename_df : ", filename_df)
    with_file_cols_df = _parse_filenames(filename_df)
    print("with file info df: ", with_file_cols_df)
    improved_df = add_relevant_info(with_file_cols_df, cystanoid_rows)
    print("improved df: ", improved_df)
    well_dfs = _get_unique_wells(improved_df)
    #well_dfs = get_well_dfs(improved_df)
    #XXX wil this be the correct order of the labels?
    get_full_csv(well_dfs)


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
    #in_prog_df['Area'] = areas
    #in_prog_df['Diameter'] = diameters
    #in_prog_df['Mean Intensity'] = intensities
    #XXX return is redundant since this is a mutable data structure
    return in_prog_df

# improved_df is a df with filename parsed into separate columns and 
# with just area, mean intensity, etc / groomed data
#def get_well_dfs(improved_df):
#    # {well name: [rows]
#    well_df_dict = _get_unique_wells(improved_df)
#    print("well rows: ", list(well_df_dict.keys()))
#    # loop through rows in improved_df
#    for well, well_dict in well_df_dict:
#        print("well dict: ", well_dict)
#        well_df = pd.DataFrame(well_dict)
#        # sorts by days for each well
#        well_df.sort_values(by = "Day")
#        # sub in a pandas dataframe for the list of rows that we had
#        # cause I do what I want because Python isn't typed and I don't have to make 
#        # a different datastructure
#        well_df_dict[well] = well_df
#
#    return well_df_dict
# then just concat / merge well_dfs together to get full df again and write out to csv

# returns well_df_dict, a dictionary with keys as unique well names and values of a list of 
# the rows corresponding to those well names
def _get_unique_wells(improved_df):
    
    well_df_dict = {}
    wells = improved_df["Well"]
    for well in wells:
        row = improved_df.loc[improved_df['Well'] == well]
        #row = row.sort_values(by = "Day")
        well_df_dict[well] = row
#        if well in well_df_dict.keys(): 
#            new_well_df_dict[well].append(row)
#        else:
#            well_df_dict[well] = [row]
    return well_df_dict

# writes full csv to out.csv, merging all the data from each well into one df
def get_full_csv(well_df_dict):
    
    big_df = pd.concat(list(well_df_dict.values()))
    print("final df: ", big_df)
#    big_df = pd.DataFrame()
#    for df in well_df_dict.values():
#        print("final well df: ", df)
#        big_df = pd.concat([big_df, df)
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


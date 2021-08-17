# Welcome to the Ilastik Organoid Detection Pipeline! Nifty

## Overview
**The general flow is this:**
1) Get your raw images  
2) Run the start script  
	2.1) Transfers your files to Hyak  
	2.2) Logs you in to Hyak  
	2.3) Starts ML processing scripts  
	2.4) Analyzes the output  
	2.5) Cleans up extra files left on Hyak (can be turned off, but do be courteous and clean up files!)  
3) Move your output excel file back to your computer (may later be automatic)  

You are able to use models that are not the defaults provided to analyze your images.
You may do so by transferring your model files to /gscratch/iscrm/freedman/ilastik/models
and changing the referenced models in /gscratch/iscrm/freedman/ilastik/scripts/auto\_ilastik.sh.  

You will find that each script in the scripts directory has a description of uses and 
preconditions at the top. You may find this useful.

## Example File Structure Invariant
.
├── README.md
├── chaytan
│   ├── in
│   │   └── testRootDir
│   │       ├── day_0
│   │       │   ├── 210616_1%_DMSO_day_0_b7.tif
│   │       │   ├── 210616_1%_DMSO_day_0_c7.tif
│   │       │   └── 210616_1%_DMSO_day_0_d7.tif
│   │       └── day_1
│   │           ├── 210617_1%_DMSO_day_1_b7.tif
│   │           ├── 210617_1%_DMSO_day_1_c7.tif
│   │           └── 210617_1%_DMSO_day_1_d7.tif
│   └── out
│       ├── out.csv
│       ├── out.xlsx
│       └── testRootDir
│           ├── day_0
│           │   ├── 210616_1%_DMSO_day_0_b7_obj.tif
│           │   ├── 210616_1%_DMSO_day_0_b7_seg.tif
│           │   ├── 210616_1%_DMSO_day_0_b7_table.csv
│           │   ├── 210616_1%_DMSO_day_0_c7_obj.tif
│           │   ├── 210616_1%_DMSO_day_0_c7_seg.tif
│           │   ├── 210616_1%_DMSO_day_0_c7_table.csv
│           │   ├── 210616_1%_DMSO_day_0_d7_obj.tif
│           │   ├── 210616_1%_DMSO_day_0_d7_seg.tif
│           │   └── 210616_1%_DMSO_day_0_d7_table.csv
│           └── day_1
│               ├── 210617_1%_DMSO_day_1_b7_obj.tif
│               ├── 210617_1%_DMSO_day_1_b7_seg.tif
│               ├── 210617_1%_DMSO_day_1_b7_table.csv
│               ├── 210617_1%_DMSO_day_1_c7_obj.tif
│               ├── 210617_1%_DMSO_day_1_c7_seg.tif
│               ├── 210617_1%_DMSO_day_1_c7_table.csv
│               ├── 210617_1%_DMSO_day_1_d7_obj.tif
│               ├── 210617_1%_DMSO_day_1_d7_seg.tif
│               └── 210617_1%_DMSO_day_1_d7_table.csv
├── models
│   ├── cyst_object_det3.ilp
│   └── cyst_pixel_seg.ilp
└── scripts
    ├── __init__.py
    ├── auto_ilastik.sh
    ├── check_file_structure.sh
    ├── cleanup.sh
    ├── consolidate_csvs.py
    ├── format_data.py
    ├── remote_hyak_start.sh
    ├── rename_files.py
    ├── run_batches.py
    ├── setup_user.sh
    ├── start.sh
    └── tests
        ├── expected_out.csv
        └── test_consoldiate_csvs.py

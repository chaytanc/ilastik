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
--> In this example, the source folder of the raw images was called testRootDir   
--> The source folder of raw images **must store images under "day X" folders**  
--> The "chaytan" (replace with your UW NetID), "in" and "out" folders will be automatically created on the Hyak with the combination of the output of the setup_user.sh (one time setup) and start.sh scripts. The "in" folder will automatically contain a copy of the local raw data on the Hyak.

<img width="521" alt="image" src="https://user-images.githubusercontent.com/35582442/129659207-e91befc9-bacc-443b-b5bf-92f1eae1136b.png">

## Video Tutorials
One-Time Setup: https://youtu.be/rlr7TK4ywJY  
Typical Analysis Run: https://youtu.be/up1MHTRvY0c

## Presentation Tutorials
Aug. 19 2021: https://docs.google.com/presentation/d/1t2_UBNMZtbM7VbJMtYXJt2JeuKuj7qVD/edit#slide=id.ge71b74fc25_0_6
  
## Other Documentation
Ilastik Model Training Details: https://docs.google.com/document/d/1znWy9IdjHWWbI4t7tmr7bd7ny6agfQomOq-TpLebyLM/edit?usp=sharing  
Hyak Environment Setup: https://docs.google.com/document/d/1KQDwg4GJw9Nw_sEUWvbM072UghmKq1Amq_hwJXi1ryg/edit?usp=sharing  
Ilastik Model Training and "By Hand" Method Details: https://docs.google.com/document/d/1JDehptQJb-okzQRx_Ty2cPFCU_NRoqwVJCRtEk8YVFw/edit?usp=sharing  




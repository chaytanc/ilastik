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
NOTE: You will have to type in your NetID password many times as well as do 2FA quite a bit. This is expected due to Hyak access restrictions on ssh.  

You are able to use models that are not the defaults provided to analyze your images.
You may do so by transferring your model files to /gscratch/freedmanlab/ilastik/models
and changing the referenced models in /gscratch/freedmanlab/ilastik/scripts/auto\_ilastik.sh.  

You will find that each script in the scripts directory has a description of uses and 
preconditions at the top. You may find this useful.

## Example File Structure Invariant
--> In this example, the source folder of the raw images was called testRootDir   
--> The source folder of raw images **must store images under "day X" folders**  
--> The "chaytan" (replace with your UW NetID), "in" and "out" folders will be automatically created on the Hyak with the combination of the output of the setup_user.sh (one time setup) and start.sh scripts. The "in" folder will automatically contain a copy of the local raw data on the Hyak. It is recommended to place your data in a folder with a name of your choosing underneath the "in" folder, with the correctly managed "day X" folders under that, as seen in the example. Successfully running start.sh with the proper parameters as documented at the top of each file will result in the creation of the "out" folder as structured in the example, with the condensed analysis titled "out.xlsx" or similarly.  

<img width="481" alt="Screen Shot 2021-12-18 at 4 25 24 PM" src="https://user-images.githubusercontent.com/35582442/146659183-4c93c1ad-f5bb-4c8d-8e69-6989528d3e08.png"><img width="481" alt="Screen Shot 2021-12-18 at 4 28 47 PM" src="https://user-images.githubusercontent.com/35582442/146659216-55fdf12e-1a3e-440a-9e27-828e038bc558.png">


## Video Tutorials
One-Time Setup: https://youtu.be/rlr7TK4ywJY  
Typical start.sh Full Pipeline Run: https://youtu.be/up1MHTRvY0c

## Presentation Tutorials
Aug. 19 2021: https://docs.google.com/presentation/d/1t2_UBNMZtbM7VbJMtYXJt2JeuKuj7qVD/edit#slide=id.ge71b74fc25_0_6
  
## Other Documentation
Ilastik Model Training Details: https://docs.google.com/document/d/1znWy9IdjHWWbI4t7tmr7bd7ny6agfQomOq-TpLebyLM/edit?usp=sharing  
Hyak Environment Setup: https://docs.google.com/document/d/1KQDwg4GJw9Nw_sEUWvbM072UghmKq1Amq_hwJXi1ryg/edit?usp=sharing  
Ilastik Model Training and "By Hand" Method Details: https://docs.google.com/document/d/1JDehptQJb-okzQRx_Ty2cPFCU_NRoqwVJCRtEk8YVFw/edit?usp=sharing  
Standard File Naming Convention: https://docs.google.com/document/d/1Hrn7xmbiiVGniBQ8X8yr9IEx_727qR8H/edit  
Transferring Models to the Hyak: https://docs.google.com/document/d/1UPf58aQaBBOidGMZmWsRPX1V8In49qSf1lQ-AkhDK5I/edit?usp=sharing  
Changing Model Files Used on the Hyak: https://docs.google.com/document/d/1DKRIbaSFAym9NO0QGRwfrTHYavDsclfeZI13IRqOVuE/edit?usp=sharing  
Common Debugging Issues: https://docs.google.com/document/d/1XEcYQI6UjKCwsu2z3ughn3Je8sk3T-i6Vc76T3NUm-U/edit?usp=sharing  
Documentation Presentation: https://docs.google.com/presentation/d/1MLbJ1rVoqF8XGeI6eyVuRkZv-GB_JDC7/edit#slide=id.ge71b74fc25_0_6  




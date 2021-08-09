# Welcome to the Ilastik Organoid Detection Pipeline! Nifty

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


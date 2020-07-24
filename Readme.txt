1. Open config.py and define your dome in terms of radius in meters and order. Save the file.
2. Open Abaqus_Input_Script
	2A. Right click on the Nodes.txt file in the directory
	2B. Copy the path to the file. This can be found under variable labeled "Location"
	2C. Paste the path in line 8 of Abaqus_Input_Script.py. Make sure to double slash and add the word "Nodes.txt" to the end of the path
	2D. Repeat for line 19 and the Edges.txt file.
3. Open DomeGenerator.py and run it
4. Open Abaqus and run Abaqus_Input_Script to generate the dome

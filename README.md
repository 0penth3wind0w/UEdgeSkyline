# UEdgeSkyline  

Note: All code are runable in their working directory  

## Data  
Data can be generated using generator.py in data folder
The format of data is as follows:  

	name, probability_1, location_1, probability_2, location_2, ...  
	
For a single data, the sum of probability will be equal to 1  

## R-Tree  
R-Tree are used in this project. Note that there is a rtree folder in this project, but nothing is implemented. The file is use for test the function of rtree only.  

## Skyline  
All skyline method used are implemented in this folder.  
- `prunePSky`: The original concept of this skyline method. No sliding window version.  
- `slideBPSky`: Brute force approach of sliding window uncertain skyline query.  
- `slideUPSky`: The proposed approach use in this project.  

## Socket  
Program use in edge computing environment.  
- edge: In charge of updating local skyline query set and pass the local result to server.  
- server: Collect edge result and compute final uncertain skyline set.  

## Test  
Use for experiment results.  
Before using these script. Make sure to create following csv file by using `generator.py` locate in `data/`.  

	10000_dim2_pos3_rad5_01000.csv  
	10000_dim2_pos4_rad5_01000.csv  
	10000_dim2_pos5_rad3_01000.csv  
	10000_dim2_pos5_rad4_01000.csv  
	10000_dim2_pos5_rad5_01000.csv  
	10000_dim2_pos5_rad6_01000.csv  
	10000_dim2_pos5_rad7_01000.csv  
	10000_dim2_pos5_rad8_01000.csv  
	10000_dim2_pos5_rad9_01000.csv  
	10000_dim2_pos5_rad10_01000.csv  
	10000_dim2_pos6_rad5_01000.csv  
	10000_dim2_pos7_rad5_01000.csv  
	10000_dim2_pos8_rad5_01000.csv  
	10000_dim2_pos9_rad5_01000.csv  
	10000_dim2_pos10_rad5_01000.csv  
	10000_dim3_pos5_rad5_01000.csv  
	10000_dim4_pos5_rad5_01000.csv  
	10000_dim5_pos5_rad5_01000.csv  
	10000_dim6_pos5_rad5_01000.csv  
	10000_dim7_pos5_rad5_01000.csv  
	10000_dim8_pos5_rad5_01000.csv  
	10000_dim9_pos5_rad5_01000.csv  
	10000_dim10_pos5_rad5_01000.csv  

## Unit test
Data related unit test are provided.  
Just simply run the .py file  

## Visualization  
2D and 3D data can be visualized.  
Just input an array to the visualize function and the result will appaer in a flash.  

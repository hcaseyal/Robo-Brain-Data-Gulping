Robo-Brain-Data-Gulping
=======================
Graph.py crawls Opencyc for information and prints it to the terminal. This includes types/subtypes, instanceOfs/instances, wikipedia links, and aliases.
Change the source code to input a different OpenCyc URI (i.e., http://sw.opencyc.org/concept/Mx8Ngh4rvszjQ5wpEbGdrcN5Y29ycA2DHiu9WOR2nCkRsZ2tw3ljb3JwHiu9WPU8nCkRsZ2tw3ljb3JwHisVUk7kJNtB15k05A1gBj04) and how many layers of neighbors you want info about.

Graph2.py crawls Opencyc similarly but writes the information to files.
Create a file called "StartingNodes.txt" in the same directory as the Python script. Each line should have 1) URI of the desired concept and, separated by whitespace, 2) the desired name of the output file.
The output files will appear in the directory. 
You can change the number of layers you want info about in the source code. Default is 1.

Project 1- Opencyc gulping

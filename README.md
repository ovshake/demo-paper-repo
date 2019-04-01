# Code 
This repository houses the code for **Go Wide, Go Deep:  Quantifying the Impact of Scientific Papers through Influence Dispersion Trees**
(accepted at *ACM/IEEE Joint Conference on Digital Libraries (Core A\* Conference)* authored by Dattatreya Mohapatra, Abhishek Maiti, Sumit Bhatia & Tanmoy Chakraborty. 

## Directories 
### src
This has 3 has scripts named 
* ```init.py```
This script parses the Microsoft Academy Search (MAS) dataset. It parses for the names, the papers which have cited by other papers, the paper
which has been cited by other papers. This then makes the ```global_citation_graph```. In this, the invalid edges are removed, the Influence Dispersion
Graph (IDG) for each paper is isolated and converted to Influence Dispersion Tree (IDT) and serialised in the form of a dictionary. 
The agruments it takes are (All are mandatory):
    * ```--masdataset```: Path to the MAS dataset. 
    * ```--dumps```: Path to dump the serialised pickled files. 

* ```main.py```
This script takes the ID of the paper (according to the MAS dataset), and the year and gives the __Normalised Influence Dispersion__ (NID) and the 
__Influence Dispersion Index__ (IDI) of the paper. 
The agruments it takes are (All are mandatory):
    * ```--masdataset```: Path to the MAS dataset. 
    * ```--dumps```: Path to dump the serialised pickled files. 
    * ```--id```: ID of the query paper 
    * ```--year```: Year till which the NID and the IDI needs to be calculated. 
    
 * ```utils.py```
 This script houses all the functions used in the other two scripts. all the documentation can be accessed by ```function_name.__doc__```. 
 
 
### data 
This has the two data developed for this paper. 
* _MAS Datatset_:Each paper belongs with ```#index<paper-id>```. Then the year follows. After the year which will be prefixed by ```#y```, the citers and the citees follow. If there is a 
  ```$``` in the prefix of the any symbolic variable such as ```$y```, then that information pertains to one of the citers of the paper whose ```#index```
  is closest to and before the line in question. If the prefix is ```\*``` then the information pertains to a citee of the paper in a similiar paper. You can find the data [here](https://drive.google.com/drive/folders/1SXmrDoi9F80ojgbU7mHcKgpE9Lje2m7g?usp=sharing). 
  
 * _Test Of Time Dataset_: This is a ```.csv``` file which has the test of time dataset which has been manually curated. 
 
  

# Code 
This repository houses the code for **Go Wide, Go Deep:  Quantifying the Impact of Scientific Papers through Influence Dispersion Trees**
(accepted at *ACM/IEEE Joint Conference on Digital Libraries* authored by Dattatreya Mohapatra, Abhishek Maiti, Sumit Bhatia & Tanmoy Chakraborty. 

## Directories 
### src
This has 3 has scripts named 
* ```init.py```
This script parses the dataset. It parses for the names, the papers which have cited by other papers, the paper
which has been cited by other papers. This then makes the ```global_citation_graph```. In this, the invalid edges are removed, the Influence Dispersion
Graph (IDG) for each paper is isolated and converted to Influence Dispersion Tree (IDT) and serialised in the form of a dictionary. 
The agruments it takes are (All are mandatory):
    * ```--dataset```: Path to the dataset. 
    * ```--dumps```: Path to dump the serialised pickled files. 

* ```main.py```
This script takes the ID of the paper according to dataset, and the year and gives the __Normalised Influence Dispersion__ (NID) and the 
__Influence Dispersion Index__ (IDI) of the paper. 
The agruments it takes are (All are mandatory):
    * ```--dataset```: Path to the dataset. 
    * ```--dumps```: Path to dump the serialised pickled files. 
    * ```--id```: ID of the query paper 
    * ```--year```: Year till which the NID and the IDI needs to be calculated. 
    
 * ```utils.py```
 This script houses all the functions used in the other two scripts. all the documentation can be accessed by ```function_name.__doc__```. 
 
 
### data 
This has the two data developed for this paper. 
* _MAS Datatset_: The data which we have used is the Microsoft Academic Search Dataset (MAS), this dataset was created by crawling the [Microsoft Academic](https://academic.microsoft.com/home) web portal. 
The dataset description are as follows:

|            Number of Papers            | 3,908,805 |
|:--------------------------------------:|-----------|
|         Number of Unique Venues        |   5,149   |
|        Number of unique authors        | 1,186,412 |
|    Avg. number of papers per author    | 5.21      |
|    Avg. number of authors per paper    | 2.57      |
| Min/Max number of references per paper | 1/2,432   |
|  Min/Max number of citations per paper | 1/13,102  |
 
You can find the data [here](https://drive.google.com/drive/folders/1SXmrDoi9F80ojgbU7mHcKgpE9Lje2m7g?usp=sharing). 
  
 * _Test Of Time Dataset_:This is a ```.csv``` file which has the test of time dataset which has been manually curated. 
 

_Note_: We currently only support MAS-style datasets but will add support for other datasets later. 
To convert your Citation dataset to MAS-style, please keep in mind the following points. The features which weren't used for this paper but are in the dataset (MAS) we used are omitted. 

* ```#index<paper-id>``` indicates the paper-id of the paper whose information is in the following lines (also referred to as the index paper).
* ```#j<text>``` indicates the journal in which it was puclished. Replace ```j``` with ```c``` to get the conference name.
* ```#y<4-digit no.>``` indicates the year in which the paper was published.
* ```#%*<text>[.]``` indicates a paper which has cited the index paper. This is the paper name and the paper-id in this dataset for the same is enclosed in ```[.]```. 
* ```#%y``` indicates the year in which the paper citing the index paper has been published.
* ```#%j``` indicates the journal in which the paper citing the index paper has been published. Replace ```j``` with ```c``` to get the conference name.
* ```#$*<text>[.]``` indicates a paper which the index paper has cited. This the paper name and the paper-id in this dataset for the same is enclosed in ```[.]```. 
* ```#$y``` indicates the year in which the paper cited by the index paper has been published.
* ```#$j``` indicates the journal in which the paper cited by the index paper has been published. Replace ```j``` with ```c``` to get the conference name.

The end is demarcated by the beginning of another index paper. 
_Please follow the order in which the above points are when converting to your dataset._

Incase of any queries you can reach us at lcs2@iiitd.ac.in




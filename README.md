# ppinet - A Python package for biological network generation and analysis

# Installing

To build and install from source, run

```shell
python setup.py install
```
You can also install from pip with

```shell
pip install ppinet
``` 

# Overview

ppinet generates a network from a list of genes/proteins. It provides both an easy-to-use object-oriented Python API and a command-line interface (CLI) for generating a biological network and post-analysis.

ppinet features include:

    Generates a biological network from STRING database
    Calculates network metrics and enrichment
    Execute a louvain community detection
    Find important genes in network based on shortest-path analysis and betweenness centrality

# Command-line interface

ppinet can be executed from the command line using the ppinet command. It takes a gene list file, output folder name and organism taxid (based on STRING) as input and outputs a several analysis of the biological network generated. 

```
usage: ppinet [-h] --input_file INPUT_FILE --organism ORGANISM --output_folder OUTPUT_FOLDER [--genes GENES]

optional arguments:
  -h, --help            show this help message and exit
  --input_file INPUT_FILE
                        File containing a gene list.
  --organism ORGANISM   STRING taxonomy ID. Ex: 9606
  --output_folder OUTPUT_FOLDER
                        Output folder
  --genes GENES         Interesting genes for Shortest-path analysis..

example: python3 ppinet.py --input_file gene_list.txt --output ppinet_output --organism 9606
```
In the output_folder, ppinet generates the following outputs:

1. species.txt :  a file containg all STRING taxonomy IDs. If you provide a invalid taxid, we advised to inspect this file.
2. degree_distribution.pdf : a PDF file containing the degree distribution of the biological network
3. network.png : a snapshot of the biological network
4. network_bc.png : a snapshot of the biological network based on betweenness centrality 
5. nodes_network2cyto.txt : all nodes and your attributes for Cytoscape analysis
6. edges_network2cyto.txt : all edges and your attributes for Cytoscape analysis
7. reports_ppinet.txt : general metrics of the biological network
8. enrichment.txt : enrichment analysis of the biological network
  
if the --genes argument is taken as input, three extra files will be generated:

9. louvain_clustering.png :  louvain community detection of the network
10. enrichment_shortestpath.txt : a file containing the enrichment analysis of all genes present in all shorthest-path from interesting genes
11. shortestpath_BC.txt : a file containing all interesting genes and its betweenness centrality (bc). As higher the value of bc as more important the gene of interest becomes.
    
# Python library usage

ppinet generates a folder in currently folder with output_folder name. 

To use as a Python library

```python

import ppinet

# arguments of ppinet
input_data = '/opt/data/input_genes.txt'
genes = '/opt/data/genes.txt'
output_folder_name = 'ppinet_output'

#generates a conversion
string_genes = ppinet.initial(input_data,output_folder_name,4932)

#generates the network metrics and return the g graph
g = ppinet.network_metrics(string_genes,output_folder_name,4932)

# generates a louvain community plot
ppinet.cl(g,output_folder_name)

# shorthest-path analysis from interesting genes
ppinet.sp(g,output_folder_name,4932,genes)
```

# Examples

A *data* folder contains a list with 300 genes of *S. cerevisiae* (input.txt file) and a list with 9 interesting genes (genes.txt file)

* Example of a biological network from the list of 300 genes

```shell
ppinet --input_file data/input.txt --organism 4932 --output_file yeast_output
```

* Example of output containing a list of genes of interest

```shell
ppinet --input_file data/input.txt --organism 4932 --output_file yeast_output --genes data/genes.txt
```



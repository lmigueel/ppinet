import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import networkx as nx
import stringdb

def sp(g,output_folder,taxid,genes_list):

        
	int_genes = pd.read_csv(genes_list, sep='\t',header=None)
	genes = int_genes.iloc[:,0]
	genes = genes.tolist()

	n = int_genes.shape[0]
        
	my_final_genes=[]
	for i in range(0,n):
		if(genes[i] in g.nodes):
			my_final_genes.append(genes[i])

        

	sp_genes = []   
	for i in range(0,len(my_final_genes)):
		for j in range(i,len(my_final_genes)):
			geneA = my_final_genes[i]
			geneB = my_final_genes[j]
                        
			comp1 = nx.node_connected_component(g,geneA)
			if geneB in comp1:
				shortest_path = nx.shortest_path(g, source=geneA, target=geneB) 
				#print("GeneA: %s GeneB: %s SP: %s\n"%(geneA,geneB,shortest_path))
				if geneB != geneA:
					for x in shortest_path:
						if x not in sp_genes:
							sp_genes.append(x)
        

	betCent = nx.betweenness_centrality(g, normalized=True, endpoints=True)

	#print(sp_genes)
	enrichment_df = stringdb.get_enrichment(sp_genes,species=taxid)
	#print(enrichment_df)
	output = output_folder + "/enrichment_shortestpath.txt"
	enrichment_df.to_csv(output,sep="\t",index=False)


        
	column_names = ["gene", "betweness_centrality"]
	report2 = pd.DataFrame(columns = column_names)

	k=0
	for v in sp_genes:
		report2.loc[k] = [v,betCent[v]]
		k=k+1   


	output = output_folder + "/shortestpath_BC.txt"
	report2.to_csv(output,sep="\t",index=False)



import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import networkx as nx
import stringdb


def network_metrics(string_ids,output_folder,taxid):

	network_df = stringdb.get_network(string_ids.queryItem,species=taxid)

	g = nx.from_pandas_edgelist(network_df,'preferredName_A','preferredName_B',edge_attr=True)

	output = output_folder + "/reports_ppinet.txt"
	report_file = open(output, "w")
	print("Number of vertices:", g.number_of_nodes(),file=report_file)
	print("Number of edges:", g.number_of_edges(),file=report_file)
	print("Network is connected?",nx.is_connected(g),file=report_file)
	print("Network density:",nx.density(g),file=report_file)
	
	if nx.is_connected(g):
        	print('Average path length:',nx.average_shortest_path_length(g),file=report_file)
	        print('Average diameter:',nx.diameter(g),file=report_file)


	components = nx.connected_components(g)
	largest_component = max(components, key=len)
	subgraph = g.subgraph(largest_component)
	diameter = nx.diameter(subgraph)
	print("Network diameter of largest component:", diameter,file=report_file)

	print("Average clustering:",nx.average_clustering(g),file=report_file)

	cc = nx.closeness_centrality(g)
	df = pd.DataFrame.from_dict({
        	'node': list(cc.keys()),
	        'centrality': list(cc.values())
	    })
	selected = df.sort_values('centrality', ascending=False)['node'].iloc[0]
	value = df.sort_values('centrality', ascending=False)['centrality'].iloc[0]
	print("Node with max closeness centrality:[Node]-[Centrality]",selected,"-",value,file=report_file)

	bc = nx.betweenness_centrality(g)
	df = pd.DataFrame.from_dict({
        	'node': list(bc.keys()),
        	'centrality': list(bc.values())
	    })
	selected = df.sort_values('centrality', ascending=False)['node'].iloc[0]
	value = df.sort_values('centrality', ascending=False)['centrality'].iloc[0]
	print("Node with max betweenness centrality:[Node]-[Centrality]",selected,"-",value,file=report_file)


	### Degree histogram
	import collections

	degree_sequence = sorted([d for n, d in g.degree()], reverse=True)  # degree sequence
	degreeCount = collections.Counter(degree_sequence)
	deg, cnt = zip(*degreeCount.items())

	fig, ax = plt.subplots()
	plt.bar(deg, cnt, width=0.75, color="b")
	plt.title("Degree Histogram.")
	plt.ylabel("Count")
	plt.xlabel("Degree")
	ax.set_xticks([d + 0.4 for d in deg])
	ax.set_xticklabels(deg)


	# draw graph in inset
	plt.axes([0.4, 0.4, 0.5, 0.5])
	Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
	pos = nx.spring_layout(g)
	plt.axis("off")
	nx.draw_networkx_nodes(g, pos, node_size=20)
	nx.draw_networkx_edges(g, pos, alpha=0.4)
	output = output_folder + "/degree_distribution.pdf"
	plt.savefig(output)

	### draw network
	plt.clf()
	nx.draw_random(g,with_labels=True)
	output = output_folder + "/network.png"
	plt.savefig(output) 

	pos = nx.spring_layout(g)
	betCent = nx.betweenness_centrality(g, normalized=True, endpoints=True)
	color = [20000.0 * g.degree(v) for v in g]
	size =  [v * 11000 for v in betCent.values()]
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, pos=pos, with_labels=True,
                 node_color=color,
                 node_size=size )
	plt.axis('off')
	output = output_folder + "/network_bc.png"
	plt.savefig(output)

	######## Report #########

	column_names = ["gene", "color","Degree","size_bc"]
	report = pd.DataFrame(columns = column_names)

	k=0
	for v in g:
        	report.loc[k] = [v,color[k],g.degree(v),size[k]]
	        k=k+1

	output = output_folder + "/nodes_network2cyto.txt"
	report.to_csv(output,sep="\t",index=False)
	output = output_folder + "/edges_network2cyto.txt"
	network_df.to_csv(output,sep="\t",index=False)

	###### Enrichment ######

	enrichment_df = stringdb.get_enrichment(string_ids.queryItem,species=taxid)
	output = output_folder + "/enrichment.txt"
	enrichment_df.to_csv(output,sep="\t",index=False)

	return g

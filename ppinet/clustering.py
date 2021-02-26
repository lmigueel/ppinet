import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import networkx as nx
import stringdb
import community
import matplotlib.cm as cm

def cl(g,output_folder):

	# compute the best partition
	partition = community.best_partition(g)

	# draw the graph
	pos = nx.spring_layout(g)

	# color the nodes according to their partition
	cmap = cm.get_cmap('viridis', max(partition.values()) + 1)

	plt.clf()
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, pos=pos, with_labels=True,
        	         node_color=list(partition.values()),
                	 node_size=40,cmap=cmap)
	plt.axis('off')

	output = output_folder + "/louvain_clustering.png"
	plt.savefig(output)

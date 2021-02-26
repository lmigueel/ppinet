import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import stringdb

def initial(input_file,output_folder,taxid):

	### 1. INPUT #######

	genes_list = pd.read_csv(input_file, sep='\t',header=None)
	genes = genes_list.iloc[:,0]
	genes = genes.tolist()

	string_ids = stringdb.get_string_ids(genes)
	os.system("mkdir %s"%output_folder)

	########## 2. Verify taxon ###############

	output = output_folder + "/species.txt"
	os.system("wget -q https://stringdb-static.org/download/species.v11.0.txt -O %s"%output)
	taxons = pd.read_csv(output, sep='\t',header=None)

	if taxid not in taxons.iloc[:,0]:
		print("Invalid taxid. Please use a taxid present in species.txt file\n")
		exit()
	else:
		return string_ids

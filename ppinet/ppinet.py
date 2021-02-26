# -*- coding: utf-8 -*-
#
#   This file is part of the tspex package, available at:
#   https://github.com/lucasmiguel/ppinet/
#
#   Tspex is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#   Contact: lucasmigueel@gmail.com

"""
Command-line interface for ppinet
"""

import argparse
import sys
import ppinet


def ppinet_cli(input_file, organism, output_folder, genes):
	""" Biological network generation and analysis."""

	string_genes = ppinet.initial(input_file,output_folder,organism)
	g = ppinet.network_metrics(string_genes,output_folder,organism)
	ppinet.cl(g,output_folder)
	
	if genes:

		ppinet.sp(g,output_folder,organism,genes)



def main():


	usage_text = '''example:

	 python3 ppinet.py --input_file gene_list.txt --output ppinet_output --organism 9606 

	'''

	my_parser = argparse.ArgumentParser(epilog=usage_text)
	my_parser.add_argument('--input_file', type=str, help='File containing a gene list.',required=True)
	my_parser.add_argument('--organism', type=int,help='STRING taxonomy ID. Ex: 9606',required=True)
	my_parser.add_argument('--output_folder', type=str,help='Output folder',required=True)
	my_parser.add_argument('--genes', type=str,help='Interesting genes for Shortest-path analysis..',required=False)

	args = my_parser.parse_args()    


	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit(0)
	
	ppinet_cli(**vars(args))


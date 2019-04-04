import utils 
import argparse
import logging
import sys
import pickle
parser = argparse.ArgumentParser(description='Calculating the IDT metric...')
parser.add_argument('--dataset' , help = 'path of the dataset')
parser.add_argument('--dumps' , help = 'path to store the pickled files') 

args = parser.parse_args()
logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , level=logging.INFO) 

if __name__ == '__main__':
	logging.info('Parsing Dataset')
	global_citation_graph = utils.parse_MAS_dataset(args.dataset)
	print(global_citation_graph.nodes())
	logging.info('Parsing Dates from dataset')
	paper_year_dict = utils.parse_dates(args.dataset) 
	logging.info('Removing Invalid Edges')
	global_citation_graph = utils.check_edge_validity(global_citation_graph, paper_year_dict)
	logging.info('Removing Cycles')
	global_citation_graph = utils.remove_cycles(global_citation_graph) 
	IDT_Dict, IDT_root_to_leaf_paths = utils.IDT_init(global_citation_graph)
	logging.info('Serialising the Graph')
	utils.dump_file(args.dumps, 'global_citation_graph' , global_citation_graph)
	logging.info('Serialising Paper- Year Dictionary') 
	utils.dump_file(args.dumps , 'paper_year_dict' , paper_year_dict) 
	logging.info('Serialising IDT Dictionary & IDT_root_to_leaf_paths')
	utils.dump_file(args.dumps , 'IDT_Dict' , IDT_Dict) 
	utils.dump_file(args.dumps , 'IDT_root_to_leaf_paths' , IDT_root_to_leaf_paths)  




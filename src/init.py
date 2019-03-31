import utils 
import argparse
import logging
parser = argparse.ArgumentParser(description='Calculating the IDT metric...')
parser.add_argument('--masdataset' , help = 'path of the MAS dataset')
parser.add_argument('--dumps' , help = 'path to store the pickled files') 

args = parser.parse_args()
logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , level=logging.INFO) 

if __name__ == '__main__':
	logging.info('Parsing MAS Dataset')
	global_citation_graph = utils.parse_MAS_dataset(args.masdataset)
	logging.info('Parsing Dates from MAS dataset')
	paper_year_dict = utils.parse_dates(args.masdataset) 
	logging.info('Removing Invalid Edges')
	global_citation_graph = utils.check_edge_validity(args.masdataset)
	logging.info('Removing Cycles')
	global_citation_graph = utils.remove_cycles(args.masdataset) 
	IDT_Dict, IDT_root_to_leaf_paths = utils.IDT_init(global_citation_graph)
	logging.info('Serialising the Graph')
	utils.dump_file(arg.dumps, 'global_citation_graph' , global_citation_graph)
	logging.info('Serialising Paper- Year Dictionary') 
	utils.dump_file(arg.dumps , 'paper_year_dict' , paper_year_dict) 
	logging.info('Serialising IDT Dictionary & IDT_root_to_leaf_paths')
	utils.dump_file(arg.dumps , 'IDT_Dict' , IDT_Dict) 
	utils.dump_file(arg.dumps , 'IDT_root_to_leaf_paths' , IDT_root_to_leaf_paths)  




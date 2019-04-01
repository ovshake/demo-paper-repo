
#global Variables
INDEX_OFFSET = 6
CITE_OFFSET = 3
YEAR_OFFSET_SHORT = 2
YEAR_OFFSET_LONG = 3
EMPTY = ""


def get_pickle_dump(filepath,filename):
"""
@Params:
filename: filename inside the ./dumps folder
@Returns:
Variable: Returns the pickled variable
"""
	with open(filepath +'/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable


def dump_file(filepath,filename, Variable):
"""
@Params:
filename: filename inside the ./dumps folder for dumping
Variable: Variable to dump inside the file
@Returns:
None
"""
	with open(filepath +'/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)

def extract_paper_id(line):
"""
@Params:
line: text line
@Returns: 
paper_id: extracts the paper-id enclosed within "[*]"
"""
	line = line.split("[")
	# "-2" is to remove the last 2 characters for CLRF line endings.
	paper_id = line_array[-1][:-2]
	return paper_id


def parse_MAS_dataset(path):
"""
@Params
path: Path to the MAS Dataset
@Returns
A global citation graph with edges from the citer to the cited.
"""

	global_citation_graph = nx.DiGraph() 
	fields = os.listdir(path)
	for field in fields:
		if field.split("_")[-1] != 'data.txt': #if not a data text file
			continue
		dataset_path = path + "/" + field
		file = open(dataset_path, 'r')
		line = file.readline()
		line = (line.encode('ascii', 'ignore')).decode("utf-8")
		index_name = EMPTY
		while line:
			if line[:INDEX_OFFSET] == '#index':
				paper_name = line[INDEX_OFFSET:-1]

			elif line[:CITE_OFFSET] == '#%*' and name != EMPTY:
				cited_by_index_name = extract_paper_id(line) 
				global_citation_graph.add_edge(index_name , cited_by_index_name)

			elif line[:CITE_OFFSET] == "#$*" and name != EMPTY:
				citing_index_name = extract_paper_id(line) 
				global_citation_graph.add_edge(citing_index_name , index_name)
			line = file.readline()
			line = (line.encode('ascii', 'ignore')).decode("utf-8")

		return global_citation_graph

def parse_dates(path):
"""
@Params:
path: Path to MAS Dataset
@Returns: 
PAPER_YEAR_DICT: Dictionary with paper ids as keys publishing years as venues
"""
	PAPER_YEAR_DICT = {}
	fields = listdir(path)
	for field in fields:
		if field.split("_")[-1] != 'data.txt':
			continue

		dataset_path = path + "/" + field
		file = open(dataset_path, 'r')
		line = file.readline()
		line = (line.encode('ascii', 'ignore')).decode("utf-8")
		paper_name = EMPTY

		while line:
			if line[:INDEX_OFFSET] == "#index":
				paper_name = line[INDEX_OFFSET:-1]

			elif line[:YEAR_OFFSET_SHORT] == "#y" and paper_name != EMPTY and line[:4] != "#ypp" and line[:5] != "#yno.":
				year = line[YEAR_OFFSET_SHORT:-1]
				PAPER_YEAR_DICT[paper_name] = year 
				paper_name = EMPTY

			elif line[:CITE_OFFSET] == '#%*':
				paper_name = extract_paper_id(line)

			elif line[:YEAR_OFFSET_LONG] == '#%y' and paper_name != EMPTY and line[:5] != "#%ypp" and line[:6] != "#%yno.":
				year = line[YEAR_OFFSET_LONG:-1]
				PAPER_YEAR_DICT[paper_name] = year
				paper_name = EMPTY

			elif line[:CITE_OFFSET] == '#$*':
				paper_name = extract_paper_id(line)

			elif line[:YEAR_OFFSET_LONG] == '#$y' and paper_name != EMPTY and line[:5] != "#$ypp" and line[:6] != "#$yno.":
				year = line[YEAR_OFFSET_LONG:-1]
				PAPER_YEAR_DICT[paper_name] = year
				paper_name = EMPTY

			line = file.readline()
			line = (line.encode('ascii', 'ignore')).decode("utf-8")
	
	return PAPER_YEAR_DICT



def check_edge_validity(global_citation_graph, PAPER_YEAR_DICT):
"""
@Params:
global_citation_graph: The global citation graph with all edges
PAPEr_YEAR_DICT: Contains the publishing of the papers

@Returns:
global_citation_graph: The global citation graph with noisy edges removed 
						i.e. those edges whose citer's publishing year is 
						less than cited's publishing year
"""
	edge_set = list(global_citation_graph.edges())

	for edge_ in edge_set:
		edge_1_present = edge_[0] in PAPER_YEAR_DICT
		edge_2_present = edge_[1] in PAPER_YEAR_DICT
		if  edge_1_present and edge_2_present and PAPER_YEAR_DICT[edge_[0]] < PAPER_YEAR_DICT[edge_[1]]:
			global_citation_graph.remove_edge(edge_)

		if edge_[0] == edge_[1]:
			global_citation_graph.remove_edge(edge_)

		if not edge_1_present or not edge_2_present:
			global_citation_graph.remove_edge(edge_)

	global_citation_graph = nx.DiGraph() 
	global_citation_graph.add_edges_from(edge_set)

	return global_citation_graph



def remove_cycles(global_citation_graph):
"""
@Params:
global_citation_graph

@Returns: 
global_citation_graph: with no cycles due to noisy data by randomly removing one edge in the cycle
						any subgraphs

"""
	node_list = list(global_citation_graph.nodes())

	for paper in node_list:

		induced_subgraph = set()
		induced_subgraph_node_list = global_citation_graph.in_edges(nbunch = [paper])

		for e in induced_graph_list:
			induced_graph.add(e[0])

		induced_graph.add(paper)

		subgraph_ = global_citation_graph.subgraph(induced_subgraph)
		cycle_lists = (nx.simple_cycles(subgraph_))

		for cycle_list in list(cycle_lists):
			length_of_cycle = len(cycle_list)
			if length_of_cycle <= 2:
				try:
					global_citation_graph.remove_edge(cycle_list[0] , cycle_list[1])
				except nx.exception.NetworkXError:
					pass 
				continue

			#Removing a Random Edge
			r = random.randint(2,length_of_cycle - 1)
			try:
				global_citation_graph.remove_edge(cycle_list[r- 1] , cycle_list[r])
			except nx.exception.NetworkXError:
				pass 

	return global_citation_graph




def IDT_init(global_citation_graph):
"""
@Params:
global_citation_graph: The global citation graph 

@Returns:
IDT: a dictionary with key as the paper index and value as the IDT (Influence Dispersion Tree)
IDT_root_to_leaf_paths: Dict with keys as Paper Name and value as All Root to leaf paths
"""
	IDT = {}
	IDT_root_to_leaf_paths = {} 
	nodes_with_cycle = 0
	for paper in global_citation_graph.nodes().copy():

		depth_dict = {}
		induced_graph = set()
		induced_graph_list = list(global_citation_graph.in_edges(nbunch = paper))


		for e in induced_graph_list:
			induced_graph.add(e[0])

		induced_graph.add(paper)

		
		#IDG has the reversed edges compared to the IDG discussed in paper. This
		# has been taken care of at the end when the reversed IDT graph is returned
		IDG = global_citation_graph.subgraph(induced_graph)
		visited = set()
		not_visited = set(IDG.nodes())
		not_visited.discard(paper)
		visited.add(paper)
		depth_dict[paper] = 0
		cur_depth = 1
		while(len(not_visited) > 0):
			cur_visit_set = set()
			for p in not_visited:
				if all_edges_in_visited(IDG,p,visited):
					ancestor_paper = get_parent_with_most_depth(depth_dict , IDG , p)
					IDG = remove_edges_except(p , ancestor_paper , IDG)
					cur_visit_set.add(p)
					depth_dict[p] = cur_depth
			visited = visited.union(cur_visit_set)
			for p in cur_visit_set:
				not_visited.discard(p)
			cur_depth += 1

		branch = []
		total_branches = []
		get_depth_of_each_branch(H , paper , 0, branch , total_branches)
		IDT_root_to_leaf_paths[paper] = total_branches
		IDT_ = IDG.reverse(copy = False)
		IDT[paper] = IDT_

	return IDT , IDT_root_to_leaf_paths



def all_edges_in_visited(IDG,p, visited):
"""
@Params: 
IDG: IDG of the paper 
p: paper whose neighbours we need to check
visited: set of nodes which are visited
@Returns:
True if all the neighbours are visited else False
"""
	edge_list = list(IDG.out_edges(nbunch = [p]))
	for e in edge_list:
		if e[1] not in visited:
			return False
	return True


def get_parent_with_most_depth(depth_dict , IDG, p):
"""
@Params: 
IDG: IDG of the paper 
p: paper whose neighbours we need to check
depth_dict: Dict with all the depth of the papers in the IDG
@Returns:
The neighbour which has the most depth and has been visited.
"""
	edge_list = list(IDG.out_edges(nbunch = [p]))
	max_depth = -1
	ancestor_paper = EMPTY
	for e in edge_list:
		if depth_dict[e[1]] > max_depth:
			max_depth = depth_dict[e[1]]
			ancestor_paper = e[1]
	return ancestor_paper

def remove_edges_except(paper, ancestor_paper , IDG):
"""
@Params: 
IDG: IDG of the paper 
paper: paper whose neighbours we need to check
ancestor_paper: The ancestor with whom we need to preserve the edges
@Returns:
The IDG with all but the given ancestor's edge removed
"""
	edge_list = list(G.out_edges(nbunch = paper))
	for e in edge_list:
		if e[1] != ancestor_paper:
			IDG.remove_edge(*e) 
	return IDG


def convert_IDG_to_IDT(IDG):
	visited = set()
	not_visited = set(IDG.nodes())
	not_visited.discard(paper)
	visited.add(paper)
	depth_dict[paper] = 0
	cur_depth = 1
	while(len(not_visited) > 0):
		cur_visit_set = set()
		for p in not_visited:
			if all_edges_in_visited(IDG,p,visited):
				ancestor_paper = get_parent_with_most_depth(depth_dict , IDG , p)
				IDG = remove_edges_except(p , ancestor_paper , IDG)
				cur_visit_set.add(p)
				depth_dict[p] = cur_depth
		visited = visited.union(cur_visit_set)
		for p in cur_visit_set:
			not_visited.discard(p)
		cur_depth += 1

	branch = []
	total_branches = []
	get_depth_of_each_branch(H , paper , 0, branch , total_branches)
	IDT_ = IDG.reverse(copy = False)

	return IDT_, total_branches





def get_idi(IDT, year, PAPER_YEAR_DICT):

	return idi, max_idi, min_idi
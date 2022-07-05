import sys, os, json
import pandas as pd
import numpy as np
from lnsimulator.ln_utils import preprocess_json_file
import lnsimulator.simulator.transaction_simulator as ts

data_dir = "/home/lin/LNSimulator/ln_data"
amount = 60000
count = 7000
epsilon = 0.8
drop_disabled = True
drop_low_cap = True
with_depletion = True
find_alternative_paths = False

print("# 1. Load LN graph data")
directed_edges = preprocess_json_file("%s/second.json" % data_dir)

print("\n# 2. Load meta data")
node_meta = pd.read_csv("%s/1ml_meta_data.csv" % data_dir)
providers = list(node_meta["pub_key"])

print("\n# 3. Simulation")
j = 0
list_max_trans = [] #The number of nodes that forwarded the most transactions per simulation
list_total_top_five_trans = [] #The total number of nodes with the top five forwarding transactions per simulation
list_more_than_100_trans = [] #The number of nodes with more than 100 forwarding transactions per simulation
list_nodes_count = [] #The number of nodes participating in the forwarding transaction in each simulation
list_mean_fee_for_sources = []
while j < 100:
	print("\nThe " + str(j + 1) + "th times")
	simulator = ts.TransactionSimulator(directed_edges, providers, amount, count, drop_disabled=drop_disabled, drop_low_cap = drop_low_cap, epsilon=epsilon, with_depletion=with_depletion)
	transactions = simulator.transactions
	_, _, all_router_fees, _, success_rate, max_num_trans = simulator.simulate(weight="total_fee",with_node_removals=find_alternative_paths, max_threads=1)
	
	print("max_num_trans:", end = "")
	max_trans = np.array(max_num_trans.iloc[[0], [2]])
	max_trans = max_trans.tolist()
	int_max_trans = max_trans[0][0]
	print(int_max_trans)
	list_max_trans.append(int_max_trans)
	
	print("top_five_trans:", end = "")
	top_five_trans = np.array(max_num_trans.iloc[0:4, [2]].sum())
	#top_five_trans = top_five_trans.tolist()
	int_top_five_trans = top_five_trans[0]
	print(int_top_five_trans)
	list_total_top_five_trans.append(int_top_five_trans)
	
	count_more_than_100_trans = 0
	while True:
		more = np.array(max_num_trans.iloc[[count_more_than_100_trans], [2]])
		more = more.tolist()
		if more[0][0] >= 100:
			count_more_than_100_trans += 1
		else:
			break
	print("count_more_than_100_trans:", end = "")
	print(count_more_than_100_trans)
	list_more_than_100_trans.append(count_more_than_100_trans);
	
	print("nodes_count:", end = "")
	print(len(max_num_trans))
	list_nodes_count.append(len(max_num_trans))
	
	print("mean_fee_for_sources:", end="")
	print(simulator.mean_fee_for_sources())
	list_mean_fee_for_sources.append(simulator.mean_fee_for_sources())
	
	j += 1
#print(list_max_trans)
pd_max_trans = pd.DataFrame(list_max_trans, columns = ["max_trans"])
pd_nodes_count = pd.DataFrame(list_nodes_count, columns = ["nodes_count"])
pd_mean_fee_for_sources = pd.DataFrame(list_mean_fee_for_sources, columns = ["mean_fee_for_sources"])
pd_total_top_five_trans = pd.DataFrame(list_total_top_five_trans, columns = ["total_top_five_trans"])
pd_more_than_100_trans = pd.DataFrame(list_more_than_100_trans, columns = ["count_more_than_100_trans"])
#print(pd_max_trans)

#Export Datas
output_dir = "output_new2"
if not os.path.exists(output_dir):
	os.makedirs(output_dir)
pd_max_trans.to_csv("%s/max_trans2.csv" % output_dir)
pd_nodes_count.to_csv("%s/nodes_count2.csv" % output_dir)
pd_mean_fee_for_sources.to_csv("%s/mean_fee_for_sources2.csv" % output_dir)
pd_total_top_five_trans.to_csv("%s/total_top_five_trans2.csv" % output_dir)
pd_more_than_100_trans.to_csv("%s/count_more_than_100_trans2.csv" % output_dir)
print("\nExport DONE")

#i = 0
#while True:
#    i += 1
#    print("\nThe " + str(i) + "th times")
#    simulator = ts.TransactionSimulator(directed_edges, providers, amount, count, drop_disabled=drop_disabled, drop_low_cap = drop_low_cap, epsilon=epsilon, with_depletion=with_depletion)
#    transactions = simulator.transactions
#    _, _, all_router_fees, _, success_rate = simulator.simulate(weight="total_fee",with_node_removals=find_alternative_paths, max_threads=1)
#    if success_rate[1] >= 0.6 and success_rate[1] - 0.6 < 0.0000001:
#        output_dir = "output2"
#        total_income, total_fee = simulator.export(output_dir)
#        break
#print(all_router_fees.head(200))
print("Done")


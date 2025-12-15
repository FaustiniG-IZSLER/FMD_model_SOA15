# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

# Codes for Bellini et al. 2025. Simulating the Spread of Foot-and-Mouth Disease 
## in Densely Populated Areas as Part of Contingency Plans to Establish the Best Control Options. 
## Pathogens 2025, 14, 933; https://doi.org/10.3390/pathogens14090933.
## First phase: build a matrix of values between 0 and 1 based on herd type and kernel distance
## Second phase: obtain an adjacency matrix for each simulation and run an agent-based 
### dynamic network model based on the NDlib Python library https://ndlib.readthedocs.io/en/latest/

# Python (version 3.11.5)
import networkx as nx                      # NetworkX library
import ndlib.models.epidemics as ep        # Ndlib library
import pandas as pd                        # Pandas library 
import numpy                               # NumPy library
from scipy.spatial.distance import cdist   # SciPy library 

# Import database of farms with attributes and coordinates

mydata = pd.read_csv("database.csv", header = 0)
len(mydata)

#Extract coordinates as a NumPy array

coords = mydata[['X', 'Y']].to_numpy()

# Compute the distance matrix

distance_matrix = cdist(coords, coords)

# Calculate the Power-law kernel

def power_law_kernel(distances, k0, r0, alfa):
    return (k0 / (1 +  ((distances / 1000)/r0)**alfa))
kernel_matrix = power_law_kernel(distance_matrix, 1, 2.500, 2.3)

# Assign 0.0 to the diagonal

numpy.fill_diagonal(kernel_matrix, 0.0)

# 1000 simulations; results populate the outputtrends list
outputtrends =[]
for y in range(1000):
# Infectivity and susceptibility parameters from: 
# (Pesciaroli et al. 2025: https://doi.org/10.3390/ani15030386)
# Infectivity parameters of the farms type
# Farm included in the study Bellini et al. 2025, n=3074. In case of a new dataset, use N = len(mydata)
    mydata['sus'] = numpy.random.beta(90,10, 3074)     # Large swine farms
    mydata['bos'] = numpy.random.beta(45,55, 3074)     # Large cattle farms
    mydata['susmall'] = numpy.random.beta(45,55, 3074) # Small swine farms
    mydata['bosmall'] = numpy.random.beta(25,75, 3074) # Small cattle farms 
# Infectivity, four levels 
    mydata['release_lev_if'] = 0
    mydata.loc[mydata['tipo'] == 2, 'release_lev_if'] = mydata['sus']
    mydata.loc[mydata['tipo'] == 1, 'release_lev_if'] = mydata['bos']
    mydata.loc[mydata['tipo'] == 4, 'release_lev_if'] = mydata['susmall']
    mydata.loc[mydata['tipo'] == 3, 'release_lev_if'] = mydata['bosmall']
#####################################################################################
# Susceptibility parameters of the farms type 
    mydata['expbos'] = numpy.random.beta(90,10, 3074) # Cattle farms 
    mydata['expsus'] = numpy.random.beta(6, 94, 3074) # Swine farms 
######## Susceptibility, two levels 
    mydata['exposure_lev_if'] = 0
    mydata.loc[mydata['species'] == 2, 'exposure_lev_if'] = mydata['expsus'] # 2=swine
    mydata.loc[mydata['species'] == 1, 'exposure_lev_if'] = mydata['expbos'] # 1=bovine
#################### Multiply element wise by the kernel matrix #############
# Ensure these are numpy arrays
    release_lev_if = mydata.release_lev_if.to_numpy()[:, None] # shape (N, 1)
    exposure_lev_if = mydata.exposure_lev_if.to_numpy()[None, :] # shape (1, 3074)
# Vectorized operations
    mymat2 = kernel_matrix.copy()
    mymatrelease = mymat2 * release_lev_if
    mymatexp = mymat2 * exposure_lev_if
    mymatrelexp = mymatrelease * mymatexp 
###################################################################################################################
# For each simulations, an edge is obtained if the probability values in mymatrelexp > a fixed random number between 0 and 1  
# By the following code we obtain a fixed threshold for each of the 1000 simulations
# in this way, we consider uncertainty in the threshold of the transmission
# probability of mymatrelexp resulting from kernel distance and farm type   
    mymat3 = numpy.where(numpy.random.random(1)[0] < mymatrelexp, 1, 0) 
####################################################################################################################
# Build the farm network
# ----------------------------
    G = nx.DiGraph(numpy.array(mymat3))
# ----------------------------
# Random removal of n (1500) nodes  
#    g2=G.copy()
#    g2.remove_nodes_from(random.sample(list(G.nodes()), 1500))
# Alternative hard removal criterium: degree 
    top_nodes = sorted(dict(G.degree).items(),key=lambda x:x[1],reverse=True)
    top1500 = top_nodes[0:1500] # first 1500 herds in terms of degree as an index of connectedness 
    top1500names = [None] * 1500  # list of 1500 with None 
# Populate the list  
    for i in range(0,1500):
        top1500names[i] = top1500[i][0]
# Remove 1500 herds (nodes) with maximum degree 
    g2=G.copy()
    g2.remove_nodes_from(top1500names)
# Identify the index case as the node with maximum degree among the remained herds, in g2  
    top_nodes2 = sorted(dict(g2.degree).items(),key=lambda x:x[1],reverse=True)
    top1500names2 = [None] * 1 # di nuovo list 
    top1500names2[0] = top_nodes2[0][0] 
# Configure SEIR model
# ----------------------------
    model = ep.SEIRModel(g2)
#################################################
    import ndlib.models.ModelConfig as mc
#################################################
# Model Configuration
# (Pesciaroli et al. 2025: https://doi.org/10.3390/ani15030386)
    config = mc.Configuration()
    config.add_model_parameter('beta', 0.25)
    config.add_model_parameter('gamma', 0.1)
    config.add_model_parameter('alpha', 0.5)
#################################################
# initial infected node based on max degree in g2 (after removal of top degree nodes) 
    infected_nodes = top1500names2 
# Random assignment of index case can be used   
#    config.add_model_parameter("fraction_infected", 0.000325309) 
################################################
# Initial infected node or nodes could be identified, example using node index: 
#   infected_nodes = [2349]
################################################   
#   using one (or more) nodes as initially "Infected", in this case, the top degree node 
    config.add_model_initial_configuration("Infected", infected_nodes)
    model.set_initial_status(config)
# 60 days run   
    iterations = model.iteration_bunch(60)
    trends = model.build_trends(iterations)
#    obtain infected nodes during each day 
    trends_infected_nodes = trends[0]["trends"]["node_count"][1]
# append the result of each new simulation to the list outputtrends    
    outputtrends.append(trends_infected_nodes)
df1500removed = pd. DataFrame(outputtrends)
print(df1500removed.head())
df1500removed.to_csv('path to .csv')
# Results can be exported for further analysis and graphical representation
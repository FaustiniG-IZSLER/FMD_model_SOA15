# FMD_model_SOA15
Probabilistic SEIR model for FMD spread and depopulation strategies in hyper-dense livestock areas

This repository contains the code for a probabilistic SEIR transmission model developed to simulate the spread of foot-and-mouth disease (FMD) among farms in one of Italy’s most livestock-dense regions. The model integrates a dynamic inter-farm contact network, where nodes represent farms and edges represent potentially infectious contacts based on distance, infectivity, and susceptibility.
Instead of adopting a single static network, 1,000 alternative networks are generated for each simulation, and a SEIR framework is applied to model farm status transitions (Susceptible, Exposed, Infectious, Removed) on a daily time step.
The model was used to compare two preventive depopulation strategies:

Random farm removal to achieve legislative animal-density thresholds.
Targeted removal of highly connected farms identified by node degree in the contact network.

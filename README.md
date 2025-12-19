# Foot-and-mouth disease modelling - EUPA&W Project


## Repository Description
This repository provides access to the Foot-and-Mouth Disease (FMD) models developed within the EUPA&W project.
FMD models are available by tags or branches.

---

## Model description: Dynamic Network-Based SEIR Model for FMD Spread and Depopulation Strategies
A **probabilistic SEIR transmission model** was developed to simulate the spread of foot-and-mouth disease (FMD) among farms in one of Italy’s most livestock-dense regions. The model integrates a dynamic inter-farm contact network, where nodes represent farms and edges represent potentially infectious contacts based on distance, infectivity, and susceptibility.  
Instead of adopting a single static network, 1,000 alternative networks are generated for each simulation, and a SEIR framework is applied to model farm status transitions (Susceptible, Exposed, Infectious, Removed) on a daily time step.  

The model was used to compare two preventive depopulation strategies:  
- **Random farm removal** to achieve legislative animal-density thresholds.  
- **Targeted removal of highly connected farms** identified by node degree in the contact network.  

Simulations demonstrated that targeted depopulation outperforms random removal, reducing epidemic size and duration with fewer farms culled, especially under worst-case scenarios.

## Citation
If you use this model in your work, please cite the following article:

_Bellini, S.; Scaburri, A.; Tironi, M.; Cappa, V.; Mannelli, A.; Alborali, G.L. Simulating the Spread of Foot-and-Mouth Disease in Densely Populated Areas as Part of Contingency Plans to Establish the Best Control Options. Pathogens 2025, 14, 933_
https://doi.org/10.3390/pathogens14090933

To cite this github page, please use the following DOI: 10.5281/zenodo.17979632 . 

---

## License
Unless specified, the models are distributed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC-BY-NC-SA 4.0) license**.
You are free to share and adapt the material under the following terms:

- Attribution : You must give appropriate credit.
- NonCommercial : You may not use the material for commercial purposes.
- ShareAlike : If you remix, transform, or build upon the material, you must distribute your contributions under the same license.

Full license text: https://creativecommons.org/licenses/by-nc-sa/4.0/

##############################################################
###################### FMD ANALYSIS ##########################
##############################################################

library(openxlsx)
library(dplyr)
library(DescTools)
library(clipr)

options(scipen = 999)

if(Sys.getenv("RSTUDIO")=="1")
  setwd(dirname(rstudioapi:::getActiveDocumentContext()$path))


### GLOSSARY
# allev = farms
# capi = heads
# somma_capi = sum of heads
# comuni = municipalities
# provincia = province
# allev_densita = farm density
# capi_densita = head density


####### STUDY AREA
### FARMS IN DPLA
allev_3074_orig = read.xlsx("subarea3074PIVOT.xlsx", sheet = "subarea3074")

### MUNICIPALITIES
area_comuni_orig = read.xlsx("IT_COMUNI_2021.xlsx")
area_comuni = area_comuni_orig %>% select(COMUNE,Shape_Area) %>% distinct()
area_comuni$DS_COMUNE=toupper(area_comuni$COMUNE)
area_comuni$AREA=(area_comuni$Shape_Area)/1000000
area_comuni$DS_COMUNE[area_comuni$DS_COMUNE=="GABBIONETA-BINANUOVA"] = "GABBIONETA BINANUOVA"
area_comuni$DS_COMUNE[area_comuni$DS_COMUNE=="GADESCO-PIEVE DELMONA"] = "GADESCO PIEVE DELMONA"

allev_3074 = allev_3074_orig %>% left_join(area_comuni, by="DS_COMUNE")

comuni_greenbox = allev_3074 %>% select(PROVINCIA,DS_COMUNE,AREA) %>% distinct()


allev_capi_prov = allev_3074 %>% group_by(PROVINCIA) %>% summarise(n_allev = n(),
                                                                   somma_capi = sum(capi)) %>% distinct()
allev_capi_prov

allev_capi_tot = allev_3074 %>% summarise(n_allev = n(),
                                          somma_capi = sum(capi)) %>% distinct()
allev_capi_tot


area = 3020.7
dens_tot = capi_tot/area
dens_tot



### Acquafredda + Calvisano + Gottolengo
allev_3074_3comuni = allev_3074 %>% filter(COMUNE=="Acquafredda" | COMUNE=="Calvisano" | COMUNE=="Gottolengo")


desc2 = allev_3074_3comuni %>% group_by(COMUNE) %>% summarise(n_allev=n())
desc2

desc3 = allev_3074_3comuni %>% filter(capi>10) %>% group_by(COMUNE) %>% summarise(n_allev=n(),
                                                                                  somma_capi=sum(capi))
desc3

desc4 = allev_3074_3comuni %>% select(COMUNE,AREA) %>% distinct()
desc4


desc5 = allev_3074_3comuni %>% filter(capi>10) %>% group_by(COMUNE) %>% summarise(allev_densita=n()/AREA,
                                                                                  capi_densita=sum(capi)/AREA) %>% distinct()
  
desc5

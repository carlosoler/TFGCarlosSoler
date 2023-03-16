from rpy2.robjects import r
r('''
    library(plumber)
    apis <- plumb("/home/ubuntu/TFGCarlosSoler/Proyecto/motorR/4098796/apis.R")
    apis$run(port=8015)
''')
#apis <- plumb("/Users/carlosoler/Documents/GitHub/TFGWord/TFGCarlosSoler/Proyecto/motorR/4098796/apis.R")
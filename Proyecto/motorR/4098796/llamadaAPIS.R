library(plumber)

apis <- plumb("/home/ubuntu/TFGCarlosSoler/Proyecto/motorR/4098796/apis.R")

apis$run(port=8015)



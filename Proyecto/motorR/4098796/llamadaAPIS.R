library(plumber)

apis <- plumb("apis.R")

apis$run(port=8015)



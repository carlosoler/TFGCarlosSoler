from rpy2.robjects import r
r('''
    library(plumber)
    apis <- plumb("motorR/4098796/apis.R")
    apis$run(port=8015)
''')



# author: Carlos Soler
# date: junio, 2022

# Limpio el workspace
# rm(list = ls())

# Cambio el directorio de trabajo
# setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
# getwd()

# Instalo paquetes
# install.packages("funModeling")
# install.packages("openxlsx")
# install.packages("rjson")
#install.packages("jsonlite")

# Cargo las librerías que voy a necesitar
library(recommenderlab)
library(clusterSim)
library(reshape2)
library(tidyverse)
library(Matrix)
library(funModeling)
library(openxlsx)
library(rjson)

# Quito la notación científica
options(scipen=999)

#* @apiTitle Calculador dde json
#* @apiDescription El objetivo de esta API es probar el JSON

#* @post /prueba_json
prueba_json <- function(nombre_usuario) {
    username = nombre_usuario
    uri = 'http://127.0.0.1:5000/skills/'
    uri_get = paste(uri, username, sep="")
    
    curl_uri <- curl_fetch_memory(uri_get)
    xxx <- jsonlite::prettify(rawToChar(curl_uri$content))
    jjj <- fromJSON(xxx)
    df_xxx <- as.data.frame(jjj)
    #x <- req$body
    return(df_xxx["alumno_id"])
}

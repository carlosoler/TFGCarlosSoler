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

#* @apiTitle Calculador similaridad ofertas nuevas
#* @apiDescription El objetivo de esta API es calcular la similaridad de las ofertas nuevas con las ofertas asignadas

#* @post /ofertas_nuevas
ofertas_nuevas <- function(a,b) {
  
  
  # Cargo los datos
  ofertas_asignadas<-read.xlsx("ofertas_asign.xlsx")
  ofertas_nuevas<-read.xlsx("ofertas_nuevas.xlsx")
  # Uno ofertas_asignadas con ofertas_nuevas
  ofertas<-rbind(ofertas_asignadas,ofertas_nuevas)
  # Parto de ofertas y elimino las columnas con info de las ofertas no relevante
  ofertas1<-select(ofertas, -alumno_id,-job_id,-empresa_nombre,-job_tittle,-ciudad)
  # Transpongo ofertas1(80x13) y obtengo ofertas2 (13x80)
  ofertas2 <- t(ofertas1)
  # Convierto ofertas2 en un DF
  ofertas2<-data.frame(ofertas2)
  # Renombro las columnas de ofertas2 como las de ofertas
  colnames(ofertas2) <- ofertas[,2]
  # Utilizo el coseno que es una medida de similaridad cuando no hay nulos
  calculoCoseno <- function(x,y){
    coseno <- sum(x*y) / (sqrt(sum(x*x)) * sqrt(sum(y*y)))
    return(coseno)
  }
  # Creo la matriz de item-to-item (oferta-to-oferta)
  ofertas.matriz <- matrix(NA, 
                           nrow=ncol(ofertas2),
                           ncol=ncol(ofertas2),
                           dimnames=list(colnames(ofertas2),colnames(ofertas2)))
  similaridad_ofertas <- as.data.frame(ofertas.matriz)
  # Calculo la similaridad utilizando el coseno para esta matriz
  for(i in 1:ncol(ofertas2)) {
    for(j in 1:ncol(ofertas2)) {
      similaridad_ofertas[i,j]= calculoCoseno(ofertas2[i],ofertas2[j])
    }
  }
  # Convierto similaridad_ofertas en un DF
  similaridad_ofertas <- as.data.frame(similaridad_ofertas)
  # Identifico las 6 ofertas más similiares a cada oferta (6 ofertas)
  # La primera oferta mas similar es ella misma con una similitud de 1
  # Creo la matriz de vecinos (72x6)
  vecinos <- matrix(NA, nrow=ncol(similaridad_ofertas),ncol=6,dimnames=list(colnames(similaridad_ofertas)))
  # Identifico a los 6 vecinos para cada alumno
  for(i in 1:ncol(ofertas.matriz)){
    vecinos[i,] <- (t(head(n=6,rownames(similaridad_ofertas[order(similaridad_ofertas[,i],decreasing=TRUE),][i]))))
  }
  # Añado una columna a vecinos con el job_id 
  vecinos <- cbind(vecinos,job_id=c(row.names(vecinos)))
  # Ordeno las columnas de vecinos
  vecinos<-vecinos[, c(7,1,2,3,4,5,6)]
  # Convierto vecinos en un DF
  vecinos<-data.frame(vecinos)
  # Transformo formato numeric para job_id en vecinos
  vecinos$job_id <- as.numeric(vecinos$job_id)
  # Elimino V2
  vecinos<-select(vecinos, -V2)
  # Identifico vecinos ofertas_nuevas (71:80)
  vecinos_ofertas_nuevas<-vecinos[vecinos$job_id == a:b,]
  # Transformo el dataframe
  vecinos_ofertas_nuevas<-vecinos_ofertas_nuevas%>%
    gather(key="V",value="vecinos",2:6)
  vecinos_ofertas_nuevas<-select(vecinos_ofertas_nuevas, -V)
  # Creo archivo xlsx
  write.xlsx(vecinos_ofertas_nuevas,"vecinos_ofertas_nuevas.xlsx")
  
  return(vecinos_ofertas_nuevas)
}


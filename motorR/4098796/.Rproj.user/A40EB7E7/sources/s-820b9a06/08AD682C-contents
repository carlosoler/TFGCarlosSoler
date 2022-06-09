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

#* @apiTitle Recomendador ofertas alumno nuevo
#* @apiDescription El objetivo de esta API es recomendar al alumno nuevo las ofertas no asignadas que mejor se adpatan a su CV

#* @post /recomendacion_alumno_nuevo
recomendacion_alumno_nuevo <- function(alumnonuevo) {
  
  # Cargo los datos
  alumnos_antiguos<-read.xlsx("alumnos_antiguos.xlsx")
  alumno_nuevo<-read.xlsx("alumno_nuevo.xlsx")
  vecinos_ofertas_nuevas<-read.xlsx("vecinos_ofertas_nuevas.xlsx")
  ofertas_nuevas<-read.xlsx("ofertas_nuevas.xlsx")
  # Uno el alumno_nuevo con los alumnos_antiguos
  alumnos<-rbind(alumnos_antiguos,alumno_nuevo)
  # Parto de alumnos y elimino las columnas con info de los alumnos primera columna (me quedo solo con las skills)
  alumnos1<-select(alumnos, -alumno_id, -username,-password, -nombre, -apellido, -telefono, -email)
  # Transpongo alumnos1(71x36) y obtengo alumnos2 (36x71)
  alumnos2 <- t(alumnos1)
  # Convierto alumnos2 en un DF
  alumnos2<-data.frame(alumnos2)
  # Renombro las columnas de alumnos2 como las de alumnos
  colnames(alumnos2) <- alumnos[,1]
  # Utilizo el coseno que es una medida de similaridad cuando no hay nulos
  calculoCoseno <- function(x,y){
    coseno <- sum(x*y) / (sqrt(sum(x*x)) * sqrt(sum(y*y)))
    return(coseno)
  }
  # Creo la matriz de item-to-item (alumno-to-alumno)
  alumnos.matriz <- matrix(NA, 
                           nrow=ncol(alumnos2),
                           ncol=ncol(alumnos2),
                           dimnames=list(colnames(alumnos2),colnames(alumnos2)))
  similaridad_alumnos <- as.data.frame(alumnos.matriz)
  # Calculo la similaridad utilizando el coseno para esta matriz
  for(i in 1:ncol(alumnos2)) {
    for(j in 1:ncol(alumnos2)) {
      similaridad_alumnos[i,j]= calculoCoseno(alumnos2[i],alumnos2[j])
    }
  }
  # Convierto similaridad en un DF
  similaridad_alumnos <- as.data.frame(similaridad_alumnos)
  # Identifico los 6 alumnos más similiares a cada alumno (6 vecinos)
  # El primer alumno mas similar es el mismo con una similitud de 1
  # Creo la matriz de vecinos (72x6)
  vecinos <- matrix(NA, nrow=ncol(similaridad_alumnos),ncol=6,dimnames=list(colnames(similaridad_alumnos)))
  # Identifico a los 6 vecinos para cada alumno
  for(i in 1:ncol(alumnos.matriz)){
    vecinos[i,] <- (t(head(n=6,rownames(similaridad_alumnos[order(similaridad_alumnos[,i],decreasing=TRUE),][i]))))
  }
  # Añado una columna a vecinos con el alumno_id 
  vecinos <- cbind(vecinos,alumno_id=c(row.names(vecinos)))
  # Ordeno las columnas de vecinos
  vecinos<-vecinos[, c(7,1,2,3,4,5,6)]
  # Convierto vecinos en un DF
  vecinos<-data.frame(vecinos)
  # Transformo formato numeric para user_id en vecinos
  vecinos$alumno_id <- as.numeric(vecinos$alumno_id)
  # Elimino V2
  vecinos<-select(vecinos, -V2)
  # Identifico vecinos alumno71
  vecinos71<-vecinos[vecinos$alumno_id == alumnonuevo,]
  # Elimino alumno_id
  vecinos71<-select(vecinos71, -alumno_id)
  # Traspongo vecinos71
  vecinos71<-t(vecinos71)
  vecinos71<-data.frame(vecinos71)
  names(vecinos71)<-c("vecinos")
  # Identifico vecinos comunes entre vecinos71 y vecinos_ofertas_nuevas
  union<-merge(x = vecinos_ofertas_nuevas, y = vecinos71, by = "vecinos")
  # Identifico las ofertas nuevas a recomendar al alumno71
  rec_alumno71<-union[,-1]
  rec_alumno71<-data.frame(rec_alumno71)
  names(rec_alumno71)<-c("job_id")
  rec_alumno71$job_id <- as.numeric(rec_alumno71$job_id)
  # Elimino job_id repetidas
  rec_alumno71<- rec_alumno71 %>% distinct(job_id, .keep_all = TRUE)
  # Uno los DF rec_alumno71 y ofertas_nuevas para generar las recomendaciones del alumno71
  REC_alumno71<-merge(x = rec_alumno71, y = ofertas_nuevas, by = "job_id")
  REC_alumno71<-REC_alumno71[,1:5]
  REC_alumno71<-REC_alumno71[,-2]
  # Creo archivo xlsx y json
  # write.xlsx(REC_alumno71,"REC_alumno71.xlsx")
  # REC_alumno71 = toJSON(REC_alumno71)
  # write(REC_alumno71,"REC_alumno71.json")
  
  return(REC_alumno71)
}



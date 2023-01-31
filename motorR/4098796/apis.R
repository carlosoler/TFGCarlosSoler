# Cargo las librerías que voy a necesitar
library(recommenderlab)
library(clusterSim)
library(reshape2)
library(tidyverse)
library(Matrix)
library(funModeling)
library(openxlsx)
library(rjson)
library(curl)
library(jsonlite)

# Quito la notación científica
options(scipen=999)

#* @apiTitle Recomendador ofertas alumno nuevo
#* @apiDescription El objetivo de esta API es recomendar al alumno nuevo las ofertas no asignadas que mejor se adpatan a su CV

#* @post /recomendacion_alumno_nuevo
recomendacion_alumno_nuevo <- function(id_alum) {
  #GET alumno nuevo
  alumno_id = id_alum
  uri1_getalum = 'http://127.0.0.1:5000/alumnos/'
  uri2_getalum = '/CV'
  uri_get_alum_nuevo = paste(uri1_getalum, alumno_id, uri2_getalum,sep="")
  curl_uri_alum_nuevo <- curl_fetch_memory(uri_get_alum_nuevo)
  json_alum1 <- jsonlite::prettify(rawToChar(curl_uri_alum_nuevo$content))
  json_alum2 <- fromJSON(json_alum1)
  df_alum_json <- as.data.frame(json_alum2)
  
  #GET ofertas nuevas
  uri_ofertas = 'http://127.0.0.1:5000/empresas/ofertas'
  curl_uri_ofertas <- curl_fetch_memory(uri_ofertas)
  json_ofertas1 <- jsonlite::prettify(rawToChar(curl_uri_ofertas$content))
  json_ofertas2 <- fromJSON(json_ofertas1)
  df_ofertas <- as.data.frame(json_ofertas2)
  ofertas_sin_estado <- df_ofertas[,c(14,2,6,7,15,4,12,18,13,1,10,22,5,16,8,11,20,3,19,9,21,17)]
  df_ofertas_nuevas<-ofertas_sin_estado[ofertas_sin_estado$estado == "SIN ASIGNAR",]
  
  #GET CV alumnos con ofertas asignadas
  uri_alum_con_ofertas = 'http://127.0.0.1:5000/alumnos/CV/oferta_asignada'
  curl_uri_CV_alumnos_con_ofertas <- curl_fetch_memory(uri_alum_con_ofertas)
  json_CValum_con_ofertas1 <- jsonlite::prettify(rawToChar(curl_uri_CV_alumnos_con_ofertas$content))
  json_CValum_con_ofertas2 <- fromJSON(json_CValum_con_ofertas1)
  df_CV_alumnos_con_ofertas <- as.data.frame(json_CValum_con_ofertas2)
  
  # Cargo los datos
  alumnos_con_ofertas<- df_CV_alumnos_con_ofertas
  alumno_nuevo<- df_alum_json
  ofertas_nuevas<- df_ofertas_nuevas
  vecinos_ofertas_nuevas<-read.xlsx("vecinos_ofertas_nuevas.xlsx")
  
  # Parto de alumnos y elimino las columnas con info de los alumnos primera columna (me quedo solo con el CV)
  alumnos_con_ofertas<-dplyr::select(alumnos_con_ofertas, -alumno_id, -id)
  alumno_nuevo<-dplyr::select(alumno_nuevo, -alumno_id, -id)
  
  #Ordeno alumno nuevo
  alumno_nuevo <- alumno_nuevo[,c(14, 25, 15, 1, 12, 5, 34, 7, 27, 16, 20, 8, 28, 22, 10, 9, 23, 11, 13, 31, 33, 17, 4, 21, 2, 3, 6, 18, 24, 32, 35, 36, 30, 19, 26, 29 )]
  
  #Ordeno a los alumnos con ofertas asignadas
  alumnos_con_ofertas <- alumnos_con_ofertas[,c(14, 25, 15, 1, 12, 5, 34, 7, 27, 16, 20, 8, 28, 22, 10, 9, 23, 11, 13, 31, 33, 17, 4, 21, 2, 3, 6, 18, 24, 32, 35, 36, 30, 19, 26, 29 )]
  
  # Uno el alumno_nuevo con los alumnos con ofertas asignadas
  alumnos<-rbind(alumnos_con_ofertas,alumno_nuevo)
  
  # Transpongo alumnos1(71x36) y obtengo alumnos2 (36x71)
  alumnos2 <- t(alumnos)
  # Convierto alumnos2 en un DF
  alumnos2<-data.frame(alumnos2)
  # Renombro las columnas de alumnos2 como las de alumnos
  colnames(alumnos2) <- rownames(alumnos)
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
  vecinos<-dplyr::select(vecinos, -V2)
  # Identifico vecinos alumno71
  vecinos71<-vecinos[vecinos$alumno_id == 71,]
  # Elimino alumno_id
  vecinos71<-dplyr::select(vecinos71, -alumno_id)
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
  # Elimino los datos que no necesito
  REC_alumno71<-dplyr::select(REC_alumno71, -alumno_id, -empresa_id, -grado, -nota_media, -ingles, -aleman, -frances, -trabajo_equipo, -comunicacion, -matematicas, -estadistica, -gestion_proyectos, -sostenibilidad, -big_data, -programacion, -estado)
  # Creo archivo xlsx y json
  # write.xlsx(REC_alumno71,"REC_alumno71.xlsx")
  # REC_alumno71 = toJSON(REC_alumno71)
  # write(REC_alumno71,"REC_alumno71.json")
  
  return(REC_alumno71)
}

#* @apiTitle Calculador similaridad ofertas nuevas
#* @apiDescription El objetivo de esta API es calcular la similaridad de las ofertas nuevas con las ofertas asignadas

#* @post /ofertas_nuevas
ofertas_nuevas <- function() {
  
  # Cargo los datos y los ordeno
  uri = 'http://127.0.0.1:5000/empresas/ofertas'
  curl_uri <- curl_fetch_memory(uri)
  json_ofertas1 <- jsonlite::prettify(rawToChar(curl_uri$content))
  json_ofertas2 <- fromJSON(json_ofertas1)
  df_ofertas <- as.data.frame(json_ofertas2)
  ofertas <- df_ofertas[,c(14,2,6,7,15,4,12,18,13,1,10,22,5,16,8,11,20,3,19,9,21,17)]
  # Parto de ofertas y elimino las columnas con info de las ofertas no relevante
  ofertas1<-dplyr::select(ofertas,-job_id, -alumno_id, -empresa_id,-empresa_nombre,-job_tittle,-ciudad, -telefono, -nombre_contacto, -estado)
  # Transpongo ofertas1(80x13) y obtengo ofertas2 (13x80)
  ofertas2 <- t(ofertas1)
  # Convierto ofertas2 en un DF
  ofertas2<-data.frame(ofertas2)
  # Renombro las columnas de ofertas2 como las de ofertas
  colnames(ofertas2) <- ofertas[,1]
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
  # Añado una columna a vecinos con el job_id y con el estado
  vecinos <- cbind(vecinos,job_id=c(row.names(vecinos)), estado=ofertas[,20])
  # Ordeno las columnas de vecinos
  vecinos<-vecinos[, c(7,8,1,2,3,4,5,6)]
  # Convierto vecinos en un DF
  vecinos<-data.frame(vecinos)
  # Transformo formato numeric para job_id en vecinos
  vecinos$job_id <- as.numeric(vecinos$job_id)
  # Elimino V3
  vecinos<-dplyr::select(vecinos, -V3)
  # Identifico vecinos ofertas SIN ASIGNAR
  vecinos_ofertas_nuevas<-vecinos[vecinos$estado == "SIN ASIGNAR",]
  # Elimino columna estado
  vecinos_ofertas_nuevas<-dplyr::select(vecinos_ofertas_nuevas, -estado)
  # Transformo el dataframe
  vecinos_ofertas_nuevas<-vecinos_ofertas_nuevas%>%
    gather(key="V",value="vecinos",2:6)
  vecinos_ofertas_nuevas<-dplyr::select(vecinos_ofertas_nuevas, -V)
  # Creo archivo xlsx
  write.xlsx(vecinos_ofertas_nuevas,"vecinos_ofertas_nuevas.xlsx")
  
  return(vecinos_ofertas_nuevas)
}
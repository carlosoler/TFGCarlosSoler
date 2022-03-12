# author: Carlos Soler
# date: marzo, 2022

# Limpio el workspace
rm(list = ls())

# Cambio el directorio de trabajo
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
getwd()

# Instalo paquetes
install.packages("funModeling")
install.packages("openxlsx")

# Cargo las librerías que voy a necesitar
library(recommenderlab)
library(clusterSim)
library(reshape2)
library(tidyverse)
library(Matrix)
library(funModeling)
library(openxlsx)

# Quito la notación científica
options(scipen=999)

# Cargo los datos
alumnos<-read.csv("Alumnos.csv")
skills<-read.csv("Skills.csv")
offers<-read.csv("Offers.csv")
organizations<-read.csv("Organizations.csv")

# Preparo el DF skills
  # Elimino la primera columna
skills<-skills[,-1]
  # Analizo los datos. Hay 138 skills diferentes
df_status(skills)
  #Transformo el tipo de datos
skills$user_id <- as.numeric(skills$user_id)
skills$skill <- as.character(skills$skill)
skills$level <- as.numeric(skills$level)
  # Elimino filas iguales
skills1<-skills %>% distinct(user_id,skill, .keep_all = T)
  # Ordeno skills1 por user_id
skills1 <- skills1[order(skills1$user_id), ]
  # Transformo skills1 (1114x3) en skills2 (200x139)
  # colocando las skills por columnas con sus niveles
skills2<-skills1%>%spread(skill,level)
  # Sustituyo en skills2 NA por 0
skills2<- mutate_all(skills2, ~replace(., is.na(.), 0))

# Preparo el DF alumnos
  # Cambio el nombre de la primera 
  # columna para hacerla comun con skills2
names(alumnos)[1] = "user_id"

# Uno los DFs skills2 y alumnos por la columna comun user_id (inner join) 
alumnos1<-merge(x = alumnos, y = skills2, by = "user_id")

# Preparo el DF offers
  # Elimino las columnas que no necesito (id,status,contracts)
offers <- select(offers, -id, -status, -contracts)
  # Ordeno offers por user_id
offers <- offers[order(offers$user_id), ]

# Preparo el DF organizations
  # Elimino las columnas que no necesito (id,status,contracts)
organizations <- select(organizations, -email, -address, -size, -sectors)

# Uno los DFs offers y organizations por la columna comun organization_id (inner join) 
offers1<-merge(x = offers, y = organizations, by = "organization_id")
  # Elimino la primera columna (organization_id)
offers1<-offers1[,-1]
  # Ordeno offers1 por user_id
offers1 <- offers1[order(offers1$user_id), ]
  # Ordeno las columnas de offers1
offers1<-offers1[, c(1,3, 4, 2)]
  # Creo offers2 con las ofertas de cada alumno 
offers2<-unite(offers1, offer,c(2:4),  sep = "; ", remove = TRUE)

####################################################################################################
# SISTEMA DE RECOMENDACIÓN
# Item-based Collaborative Filtering (IBCF)
# Cálculos en vectores "vertical" por columnas buscando alumnos que tengan valoraciones similares en las skills
###############################################################################################################

# Parto de skills2 y elimino la primera columna (no necesito user_id)
skills3<-skills2[,-1]
  #Transformo el tipo de datos
skills2$user_id <- as.character(skills2$user_id)
df_status(skills2)

# Transpongo skills3(200x138) y obtengo alumnos3 (138x200)
alumnos3 <- t(skills3)
  # Convierto alumnos3 en un DF
alumnos3<-data.frame(alumnos3)
  # Renombro las columnas de alumnos3 como las de skills2
colnames(alumnos3) <- skills2[,1]

# Analizo la estructura de los datos y veo que hay columnas con demasiados ceros
df_status (alumnos3)
  # Obtengo la tabla de estado
datos_status=df_status(alumnos3, print_results = F)
  # Obtengo las variables a eliminar que tengan más de un 96.37% de valores a cero
vars_to_remove=filter(datos_status, p_zeros > 96.37)  %>% .$variable
vars_to_remove
  # Dejo todas las columnas salvo aquellas que estén en el vector que crea df_status 'vars_to_remove'
alumnos4=dplyr::select(alumnos3, -one_of(vars_to_remove))
df_status (alumnos4)
  # Me quedo con 72 alumnos que tienen al menos 5 (3,63% x 138) skills valoradas


# Utilizo el coseno que es una medida de similaridad cuando no hay nulos
calculoCoseno <- function(x,y){
  coseno <- sum(x*y) / (sqrt(sum(x*x)) * sqrt(sum(y*y)))
  return(coseno)
}

# Creo la matriz de item-to-item (alumno-to-alumno)
alumnos.matriz <- matrix(NA, 
                        nrow=ncol(alumnos4),
                        ncol=ncol(alumnos4),
                        dimnames=list(colnames(alumnos4),colnames(alumnos4)))

similaridad_alumnos <- as.data.frame(alumnos.matriz)

# Calculo la similaridad utilizando el coseno para esta matriz
for(i in 1:ncol(alumnos4)) {
  for(j in 1:ncol(alumnos4)) {
    similaridad_alumnos[i,j]= calculoCoseno(alumnos4[i],alumnos4[j])
  }
}
# Convierto similaridad en un DF
similaridad_alumnos <- as.data.frame(similaridad_alumnos)
head(similaridad_alumnos)

# Identifico los 6 alumnos más similiares a cada alumno (6 vecinos)
# El primer alumno mas similar es el mismo con una similitud de 1
  # Creo la matriz de vecinos (72x6)
vecinos <- matrix(NA, nrow=ncol(similaridad_alumnos),ncol=6,dimnames=list(colnames(similaridad_alumnos)))
  # Identifico a los 6 vecinos para cada alumno
for(i in 1:ncol(alumnos.matriz)){
  vecinos[i,] <- (t(head(n=6,rownames(similaridad_alumnos[order(similaridad_alumnos[,i],decreasing=TRUE),][i]))))
}
  # Añado una columna a vecinos con el user_id 
vecinos <- cbind(vecinos,user_id=c(row.names(vecinos)))
  # Ordeno las columnas de vecinos
vecinos<-vecinos[, c(7,1,2,3,4,5,6)]
  # Convierto vecinos en un DF
vecinos<-data.frame(vecinos)
df_status (vecinos)

# Transformo formato numeric para user_id en vecinos y offers2
vecinos$user_id <- as.numeric(vecinos$user_id)
offers2$user_id <- as.numeric(offers2$user_id)

# Transformo vecinos (72x7) en vecinos2 (432x3) 432=72 alumnos x 6 vecinos
vecinos2<- base::transform(reshape2::melt(vecinos, 
                                                    id.var='user_id', 
                                                    na.rm=TRUE), 
                                     variable=base::match(variable,names(vecinos)[-1]))
  # Ordeno skills1 por user_id
vecinos2<-vecinos2[order(vecinos2$user_id), ]
  # Elimino la columna 2 (variable)
vecinos2<-vecinos2[,-2]
  # Renombro "user_id" como "user" y "value" como "user_id"
names(vecinos2)<-c("user","user_id")

# Uno los DF vecinos2 y offers2 para generar las recomendaciones de ofertas de trabajo
recomendaciones<-merge(x = vecinos2, y = offers2, by = "user_id")
  # Transformo formato numeric para user_id
recomendaciones$user_id <- as.numeric(recomendaciones$user_id)
  # Ordeno recomendaciones por user
recomendaciones<-recomendaciones[order(recomendaciones$user), ]
  # Ordeno las columnas de recomendaciones
recomendaciones<-recomendaciones[, c(2,1,3)]
  # Renombro "user" como "user_id" y "user_id" como "vecinos"
names(recomendaciones)<-c("user_id","vecinos","offers")
  # Elimino la columna 2 (vecinos)
recomendaciones2<-recomendaciones[,-2]
  # Elimino filas (ofertas) iguales (que en este caso no las hay)
recomendaciones2<-recomendaciones2 %>% distinct(user_id,offers, .keep_all = T)



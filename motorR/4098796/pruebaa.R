install.packages("jsonlite")
install.packages("curl")
library(curl)
library(jsonlite)

#get_alum <- curl("http://127.0.0.1:5000/skills/marquitos")

#Forma 1 haciendo un get y pasando desde otra API el username

username = 'marquitos'
uri = 'http://127.0.0.1:5000/skills/'
uri_get = paste(uri, username, sep="")
alum_skill <- fromJSON(uri_get)
df_alum_skill <- as.data.frame(alum_skill)


#Forma 2 pasandole el JSON
json_alum <- '{
    "aleman": 2,
    "alumno_id": 71,
    "analisis_datos": 2,
    "bases_datos": 2,
    "big_data": 2,
    "capacidad_analitica": 2,
    "cloud": 2,
    "comunicacion": 2,
    "decision_making": 2,
    "diseno_grafico": 2,
    "e_commerce": 2,
    "estadistica": 2,
    "frances": 2,
    "gestion_proyectos": 2,
    "grado": 2,
    "id": 71,
    "ingles": 2,
    "inovacion": 2,
    "inteligencia_artificial": 2,
    "intenet_of_things": 2,
    "java": 2,
    "liderazgo": 2,
    "machine_learning": 2,
    "marketing": 2,
    "matematicas": 2,
    "networks": 2,
    "nota_media": 2,
    "pascal": 2,
    "pensamiento_critico": 2,
    "problem_solving": 2,
    "python": 2,
    "r": 2,
    "redes_sociales": 2,
    "sistemas_operativos": 2,
    "sostenibilidad": 2,
    "trabajo_equipo": 2,
    "web_desarrollo": 2,
    "web_diseno": 2
}'

pruebaa <- fromJSON(json_alum)
df_oruebaa <- as.data.frame(pruebaa)
print(df_oruebaa["alumno_id"])


#Forma 3
username = 'marquitos'
uri = 'http://127.0.0.1:5000/skills/'
uri_get = paste(uri, username, sep="")
curl_uri <- curl_fetch_memory(uri_get)
xxx <- jsonlite::prettify(rawToChar(curl_uri$content))
jjj <- fromJSON(xxx)
df_xxx <- as.data.frame(jjj)


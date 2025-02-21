import pandas as pd

# Conexiòn con el dataset
tabla=pd.read_csv("C:/Users/rherr/Documents/Proyecto final/dataseriea.csv")

# Exploraciòn del dataset
print(tabla.head())
print(tabla.info())
print(tabla.describe())
print(tabla.columns)

#Limpieza de datos
tabla['Club'] = tabla['Club'].str.strip()

#Analisis del dataset
#1 Goles aportados para el club Inter 
inter_goles =tabla[tabla['Club'] == 'Inter']['Goles'].sum()
print(f"Total de goles del club Inter: {inter_goles}")

#2 Jugadores del Inter filtrados por goles-asistencias y ordenados por su aportaciòn
inter_aportacion = tabla[tabla['Club'] == 'Inter'].copy()
inter_aportacion['Aportacion_Total'] = inter_aportacion['Goles'] + inter_aportacion['Asistencias']
inter_ordenado = inter_aportacion[['Jugador', 'Goles', 'Asistencias', 'Aportacion_Total']].sort_values('Aportacion_Total', ascending=False)
print("Aportación de jugadores del Inter (Goles + Asistencias):")
print(inter_ordenado)

#3 Top 10 Nacionalidades con mas goles (excluyendo a Italia por ser el campeonato italiano)
goleadores_por_pais = tabla[tabla['Nacionalidad'] != 'Italia'].groupby('Nacionalidad').agg({
    'Jugador': 'count',  
    'Goles': 'sum',     
}).sort_values('Goles', ascending=False).head(10)
goleadores_por_pais.columns = ['Cantidad de Jugadores', 'Total de Goles']
print("Top 10 paises (excluyendo Italia) que más aportan goles a la Serie A:")
print(goleadores_por_pais)

#4 Aportaciones de jugadores argentinos ordenados por mayor cantidad de goles 
argentinos = tabla[tabla['Nacionalidad'] == 'Argentina'][['Jugador', 'Club', 'Goles', 'Asistencias', 'Partidos']]
argentinos_ordenados = argentinos.sort_values('Goles', ascending=False)
print("Jugadores argentinos ordenados por goles:")
print(argentinos_ordenados)

#5 Aportaciones de jugadores franceses ordenados por mayor cantidad de goles
franceses = tabla[tabla['Nacionalidad'] == 'Francia'][['Jugador', 'Club', 'Goles', 'Asistencias', 'Partidos']]
franceses_ordenados = franceses.sort_values('Goles', ascending=False)
print("Jugadores franceses ordenados por goles:")
print(franceses_ordenados)

#6 Top 10 Jugadores con 30 o más partidos con mejor promedio de gol 
jugadores_30 = tabla[tabla['Partidos'] >= 30].copy()
jugadores_30['Promedio_Goles'] = jugadores_30['Goles'] / jugadores_30['Partidos']
top_10 = jugadores_30[['Jugador', 'Club', 'Goles', 'Partidos', 'Promedio_Goles']]\
    .sort_values('Promedio_Goles', ascending=False)\
    .head(10)
top_10['Promedio_Goles'] = top_10['Promedio_Goles'].round(2) 
print("Top 10 jugadores con mejor promedio de gol (minimo 30 partidos):")
print(top_10)

#7 Top 10 goles y asistencias por club
goles_por_club = tabla.groupby('Club').agg({
    'Goles': 'sum',
    'Asistencias': 'sum'
}).sort_values('Goles', ascending=False).head(10)
print("Top 10 clubes por goles:")
print(goles_por_club)

#8 Top 10 jugadores mas efectivos de la liga con al menos 10 goles
jugadores_efectivos = tabla[tabla['Goles'] >= 10].copy()
jugadores_efectivos['Efectividad'] = (jugadores_efectivos['Goles'] / jugadores_efectivos['Partidos']).round(2)
top_10_efectivos = jugadores_efectivos[['Jugador', 'Club', 'Goles', 'Partidos', 'Efectividad']]\
    .sort_values('Efectividad', ascending=False)\
    .head(10)
print("Top 10 jugadores mas efectivos (10+ goles):")
print(top_10_efectivos)

#9 Jugadores con menos aportes para su equipo con al menos 30 partidos
jugadores_30 = tabla[tabla['Partidos'] >= 30].copy()
jugadores_30['Aporte_Total'] = jugadores_30['Goles'] + jugadores_30['Asistencias']
jugadores_30['Promedio_Aporte'] = (jugadores_30['Aporte_Total'] / jugadores_30['Partidos']).round(2)
menos_efectivos = jugadores_30[['Jugador', 'Club', 'Partidos', 'Goles', 'Asistencias', 'Aporte_Total', 'Promedio_Aporte']]\
    .sort_values(['Aporte_Total', 'Promedio_Aporte'])\
    .head(10)
print("Top 10 jugadores con menos aportes (minimo 30 partidos):")
print(menos_efectivos)

#10 Top 10 jugadores con mayor aporte total / aporte por partido 
tabla['Aporte_Total'] = tabla['Goles'] + tabla['Asistencias']
tabla['Aporte_Por_Partido'] = (tabla['Aporte_Total'] / tabla['Partidos']).round(2)
top_10_aporte = tabla[['Jugador', 'Club', 'Partidos', 'Goles', 'Asistencias', 'Aporte_Total', 'Aporte_Por_Partido']]\
    .sort_values('Aporte_Total', ascending=False)\
    .head(10)
print("Top 10 jugadores con mayor aporte total:")
print(top_10_aporte)

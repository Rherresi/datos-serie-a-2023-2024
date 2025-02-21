import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Conexión con el dataset
tabla = pd.read_csv("C:/Users/rherr/Documents/Proyecto final/dataseriea.csv")

#Grafico1: Top 10 Jugadores del Inter por contribución total 
jugadores_inter = tabla[tabla['Club'] == 'Inter'][['Jugador', 'Goles', 'Asistencias']]
jugadores_inter['Total_Aporte'] = jugadores_inter['Goles'] + jugadores_inter['Asistencias']
jugadores_inter = jugadores_inter.sort_values('Total_Aporte', ascending=True).tail(10)

plt.figure(figsize=(12, 6))
plt.barh(jugadores_inter['Jugador'], jugadores_inter['Goles'], color='blue', label='Goles')
plt.barh(jugadores_inter['Jugador'], jugadores_inter['Asistencias'], 
         left=jugadores_inter['Goles'], color='green', label='Asistencias')
plt.title('Top 10 Jugadores del Inter - Goles y Asistencias')
plt.xlabel('Cantidad')
plt.ylabel('Jugadores')
plt.legend()
for i, (goles, asist) in enumerate(zip(jugadores_inter['Goles'], jugadores_inter['Asistencias'])):
    if goles > 0:
        plt.text(goles/2, i, str(goles), ha='center', va='center')
    if asist > 0:
        plt.text(goles + asist/2, i, str(asist), ha='center', va='center')
plt.tight_layout()
plt.show()

#Grafico2: Top 10 Jugadores de la liga agrupados por nacionalidad (excluyendo Italia)
goleadores_por_pais = tabla[tabla['Nacionalidad'] != 'Italia'].groupby('Nacionalidad').agg({
    'Jugador': 'count',  
    'Goles': 'sum',     
}).sort_values('Goles', ascending=False).head(10)
goleadores_por_pais.columns = ['Cantidad de Jugadores', 'Total de Goles']
fig, ax1 = plt.subplots(figsize=(12, 6))
x = np.arange(len(goleadores_por_pais.index))
width = 0.35
bars1 = ax1.bar(x - width/2, goleadores_por_pais['Total de Goles'], width, label='Goles', color='blue')
bars2 = ax1.bar(x + width/2, goleadores_por_pais['Cantidad de Jugadores'], width, label='Jugadores', color='green')
ax1.set_ylabel('Cantidad')
ax1.set_title('Top 10 Nacionalidades en Serie A (excluyendo Italia)')
ax1.set_xticks(x)
ax1.set_xticklabels(goleadores_por_pais.index, rotation=45, ha='right')
ax1.legend()
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(bars1)
autolabel(bars2)
plt.tight_layout()
plt.show()

#Grafico3: Aportacion de jugadores argentinos ordenados por mayor cantidad de goles 
argentinos = tabla[tabla['Nacionalidad'] == 'Argentina'][['Jugador', 'Club', 'Goles', 'Asistencias', 'Partidos']]
argentinos_ordenados = argentinos.sort_values('Goles', ascending=True)  
plt.figure(figsize=(12, 6))
plt.barh(argentinos_ordenados['Jugador'], argentinos_ordenados['Goles'], 
         color='skyblue', label='Goles')
plt.barh(argentinos_ordenados['Jugador'], argentinos_ordenados['Asistencias'], 
         left=argentinos_ordenados['Goles'], color='lightgreen', label='Asistencias')
plt.title('Aportación de Jugadores Argentinos en Serie A')
plt.xlabel('Cantidad')
plt.ylabel('Jugadores')
plt.legend()
for i, (goles, asist) in enumerate(zip(argentinos_ordenados['Goles'], argentinos_ordenados['Asistencias'])):
    if goles > 0:
        plt.text(goles/2, i, str(goles), ha='center', va='center', color='black')
    if asist > 0:
        plt.text(goles + asist/2, i, str(asist), ha='center', va='center', color='black')
nombres_con_club = [f"{j} ({c})" for j, c in zip(argentinos_ordenados['Jugador'], argentinos_ordenados['Club'])]
plt.yticks(range(len(nombres_con_club)), nombres_con_club)
plt.tight_layout()
plt.show()

#Grafico4: Efectividad para jugadores con al menos 1 partido
tabla['Efectividad'] = tabla['Goles'] / tabla['Partidos']
plt.figure(figsize=(12, 6))
n, bins, patches = plt.hist(tabla['Efectividad'], bins=20, color='salmon', 
                          edgecolor='black', label='Jugadores')
media = tabla['Efectividad'].mean()
plt.axvline(x=media, color='red', linestyle='dashed', 
            label=f'Media: {media:.2f}')
mediana = tabla['Efectividad'].median()
plt.axvline(x=mediana, color='green', linestyle='dashed', 
            label=f'Mediana: {mediana:.2f}')
plt.title('Distribucion de la Efectividad (Goles por Partido)', pad=20)
plt.xlabel('Goles por Partido')
plt.ylabel('Cantidad de Jugadores')
plt.grid(True, alpha=0.3)
plt.legend()
stats = f'Estadísticas:\n'
stats += f'Media: {media:.2f}\n'
stats += f'Mediana: {mediana:.2f}\n'
stats += f'Máx: {tabla["Efectividad"].max():.2f}\n'
stats += f'Mín: {tabla["Efectividad"].min():.2f}'
plt.text(0.95, 0.95, stats, transform=plt.gca().transAxes, 
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.tight_layout()
plt.show()

#Grafico5: Relaciòn entre goles y asistencias entre jugadores con mas de 8 goles y 5 asistencias 
plt.figure(figsize=(12, 8))
plt.scatter(tabla['Asistencias'], tabla['Goles'], 
           alpha=0.6, 
           c='blue', 
           s=100)     
plt.title('Relacion entre Goles y Asistencias en la Serie A', pad=20, size=14)
plt.xlabel('Numero de Asistencias', size=12)
plt.ylabel('Numero de Goles', size=12)
plt.grid(True, alpha=0.3)
for i, row in tabla.iterrows():
    if row['Goles'] > 8 or row['Asistencias'] > 5:  
        plt.annotate(f"{row['Jugador']} ({row['Club']})", 
                    (row['Asistencias'], row['Goles']),
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=8,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
media_goles = tabla['Goles'].mean()
media_asistencias = tabla['Asistencias'].mean()
plt.axhline(y=media_goles, color='r', linestyle='--', alpha=0.3, label=f'Media Goles: {media_goles:.2f}')
plt.axvline(x=media_asistencias, color='g', linestyle='--', alpha=0.3, label=f'Media Asistencias: {media_asistencias:.2f}')
plt.legend()
plt.tight_layout()
plt.show()


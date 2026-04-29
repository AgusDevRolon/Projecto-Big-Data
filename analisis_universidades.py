# Proyecto de Visualización de Datos: Universidades en Buenos Aires
# Este script carga, limpia, analiza y visualiza datos de universidades en Buenos Aires.

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import re

# Sección 1: Carga de datos
print("=== CARGA DE DATOS ===")
# Cargar el dataset desde el archivo CSV
df = pd.read_csv('universidades.csv')
print("Dataset cargado exitosamente.")
print(f"Dimensiones iniciales: {df.shape}")

# Sección 2: Limpieza de datos
print("\n=== LIMPIEZA DE DATOS ===")

# Mostrar información inicial
print("Información inicial del dataset:")
print(df.info())

# Eliminar valores nulos (NaN) solo en columnas críticas
df = df.dropna(subset=['geometry', 'nombre', 'barrio', 'comuna'])
print(f"Después de eliminar NaN en columnas críticas: {df.shape}")

# Eliminar registros duplicados
df = df.drop_duplicates()
print(f"Después de eliminar duplicados: {df.shape}")

# Normalización de textos: convertir barrio a title case
df['barrio'] = df['barrio'].str.title()

# Procesar el campo de coordenadas (geometry)
# El formato es "POINT (long lat)", extraeremos latitud y longitud
def extraer_coordenadas(geometry):
    # Usar regex para extraer los números
    match = re.search(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)', geometry)
    if match:
        long, lat = match.groups()
        return float(lat), float(long)  # Nota: en POINT es (long lat), pero convencionalmente lat primero
    return None, None

df['latitud'], df['longitud'] = zip(*df['geometry'].apply(extraer_coordenadas))

# Eliminar filas donde no se pudieron extraer coordenadas
df = df.dropna(subset=['latitud', 'longitud'])
print(f"Después de procesar coordenadas: {df.shape}")

# Procesar comuna: extraer el número
df['comuna_num'] = df['comuna'].str.extract(r'(\d+)').astype(int)

# Resumen del dataset limpio
print("\n=== RESUMEN DEL DATASET LIMPIO ===")
print("Primeras 5 filas:")
print(df.head())
print("\nInformación del dataset:")
print(df.info())
print("\nEstadísticas descriptivas:")
print(df.describe())

# Sección 3: Análisis de datos con NumPy
print("\n=== ANÁLISIS DE DATOS CON NUMPY ===")

# Cantidad de universidades por barrio
barrios, counts_barrios = np.unique(df['barrio'].values, return_counts=True)
universidades_por_barrio = dict(zip(barrios, counts_barrios))
print("Universidades por barrio:")
for barrio, count in universidades_por_barrio.items():
    print(f"{barrio}: {count}")

# Cantidad de universidades por comuna
comunas, counts_comunas = np.unique(df['comuna_num'].values, return_counts=True)
universidades_por_comuna = dict(zip(comunas, counts_comunas))
print("\nUniversidades por comuna:")
for comuna, count in universidades_por_comuna.items():
    print(f"Comuna {comuna}: {count}")

# Sección 4: Visualización de datos con Plotly
print("\n=== VISUALIZACIÓN DE DATOS CON PLOTLY ===")

# Gráfico de barras: cantidad de universidades por barrio
# Justificación: El gráfico de barras es efectivo para comparar cantidades entre categorías discretas como barrios.
# Permite ver rápidamente cuáles barrios tienen más universidades.
fig_bar = px.bar(x=barrios, y=counts_barrios, 
                 title='Cantidad de Universidades por Barrio en Buenos Aires',
                 labels={'x': 'Barrio', 'y': 'Cantidad de Universidades'},
                 color=counts_barrios, color_continuous_scale='Blues')
fig_bar.update_layout(xaxis_tickangle=-45)

# Gráfico de torta: distribución por comuna
# Justificación: El gráfico de torta es ideal para mostrar proporciones y distribución porcentual entre categorías.
# Ayuda a visualizar qué porcentaje del total representan las universidades en cada comuna.
labels_comuna = [f'Comuna {c}' for c in comunas]
fig_pie = px.pie(values=counts_comunas, names=labels_comuna,
                 title='Distribución de Universidades por Comuna en Buenos Aires')

# Mapa de ubicaciones
fig_map = px.scatter_map(df, lat='latitud', lon='longitud', 
                         hover_name='nombre', hover_data=['barrio', 'comuna'],
                         title='Ubicación de Universidades en Buenos Aires',
                         zoom=10, height=600)

# Crear subplots para combinar gráficos
fig_combined = make_subplots(rows=1, cols=2, 
                             subplot_titles=('Universidades por Barrio', 'Distribución por Comuna'),
                             specs=[[{'type': 'bar'}, {'type': 'domain'}]])

# Agregar gráficos a subplots
fig_combined.add_trace(fig_bar.data[0], row=1, col=1)
fig_combined.add_trace(fig_pie.data[0], row=1, col=2)

# Actualizar layout
fig_combined.update_layout(height=600, title_text="Dashboard de Universidades en Buenos Aires")

# Guardar como HTML para la landing page
fig_combined.write_html("dashboard_universidades.html")
print("Dashboard guardado como 'dashboard_universidades.html'")

# Exportar los datos procesados a JSON para la página web interactiva
dashboard_data = {
    'barrios': barrios.tolist(),
    'counts_barrios': counts_barrios.tolist(),
    'comunas': labels_comuna,
    'counts_comunas': counts_comunas.tolist(),
    'universidades': df[['nombre', 'unidad_aca', 'sede', 'dirreccion', 'barrio', 'comuna', 'telefono', 'web', 'latitud', 'longitud']].to_dict(orient='records')
}
import json
with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
print("Datos exportados a 'dashboard_data.json' para la página interactiva")

# Mostrar gráficos (en entorno interactivo)
fig_combined.show()

print("\n=== FIN DEL ANÁLISIS ===")
print("El proyecto ha completado la carga, limpieza, análisis y visualización de los datos.")
print("El dashboard interactivo ha sido guardado como archivo HTML.")
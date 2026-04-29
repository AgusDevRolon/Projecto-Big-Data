# Guía de Ejecución del Proyecto

## Inicio Rápido (5 minutos)

### 1. Abrir el Dashboard

**Opción A: Directamente (Recomendado para primer acceso)**
```
1. Navega a: c:\Users\Agustín\Desktop\big data\Projecto-Big-Data
2. Haz doble click en: index.html
3. Se abrirá en tu navegador por defecto
```

**Opción B: Servidor Local (Para desarrollo)**
```powershell
cd "c:\Users\Agustín\Desktop\big data\Projecto-Big-Data"
python -m http.server 8000
# Luego abre: http://localhost:8000
```

### 2. Explorar el Dashboard

- **KPIs:** Ve los números clave en la parte superior
- **Filtros:** Selecciona una comuna o barrio
- **Gráficos:** Haz click en barras o torta para filtrar
- **Mapa:** Haz zoom y explora ubicaciones
- **Detalles:** Selecciona una comuna en el selector inferior

---

## Ejecución Completa (Con Regeneración de Datos)

### Paso 1: Configurar Entorno Python

```powershell
cd "c:\Users\Agustín\Desktop\big data\Projecto-Big-Data"

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install pandas numpy plotly
```

### Paso 2: Ejecutar Procesamiento de Datos

```powershell
# Ejecutar el script de análisis
python analisis_universidades.py
```

**Salida esperada:**
```
=== CARGA DE DATOS ===
Dataset cargado exitosamente.
Dimensiones iniciales: (199, 11)

=== LIMPIEZA DE DATOS ===
...
=== ANÁLISIS COMPLETADO ===
```

### Paso 3: Verificar Archivos Generados

```powershell
# Ver archivos generados
Get-ChildItem -Filter "*.json" | Format-Table Name, Length

# Ejemplo de salida:
#   Name                          Length
#   ----                          ------
#   universidades.json            185000
#   dashboard_data.json           180000
#   dashboard_data_inline.js      190000
```

### Paso 4: Abrir el Dashboard

```
Opción A: Doble click en index.html
Opción B: Servir con http.server y abrir navegador
```

---

## Troubleshooting

### **Problema: "ModuleNotFoundError: No module named 'pandas'"**

**Solución:**
```powershell
# Instalar pandas
pip install pandas

# Si sigue fallando:
pip install --upgrade pandas numpy plotly
```

### **Problema: El navegador muestra página en blanco**

**Posibles causas y soluciones:**

1. **Archivo no encontrado:**
   - Verifica que `dashboard_data_inline.js` existe en el mismo directorio que `index.html`
   - Abre consola del navegador (F12) para ver errores

2. **Datos no cargados:**
   - Asegúrate de que ejecutaste `python analisis_universidades.py` primero
   - Verifica que `universidades.csv` existe

3. **Problema de CORS (si usas http.server):**
   ```powershell
   # Usa Python con servidor apropiado
   python -m http.server 8000 --bind 127.0.0.1
   ```

### **Problema: Mapa no aparece**

**Solución:**
- Verifica conexión a internet (necesita descargar tiles de OpenStreetMap)
- Abre consola (F12) y busca errores de Leaflet.js

### **Problema: Los gráficos están vacíos**

**Posibles causas:**

1. **Datos no filtrados correctamente:**
   - Abre consola (F12) y ejecuta: `console.log(window.dashboardData)`
   - Verifica que vea universidades

2. **Problema de Plotly:**
   - Verifica que CDN de Plotly está accesible
   - Prueba en otro navegador

---

## Scripts Útiles

### **Verificar Integridad de Datos**

```python
import pandas as pd
import json

# Cargar y validar
df = pd.read_csv('universidades.csv')
print(f"Registros: {len(df)}")
print(f"Campos: {df.columns.tolist()}")
print(f"NaN: {df.isnull().sum().sum()}")

# Verificar JSON generado
with open('dashboard_data_inline.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Verificar que contiene JSON válido
    if 'window.dashboardData = {' in content:
        print("✓ JSON estructura correcta")
```

### **Regenerar Datos (Forzar)**

```powershell
# Eliminar archivos generados
Remove-Item "universidades.json" -Force
Remove-Item "dashboard_data.json" -Force
Remove-Item "dashboard_data_inline.js" -Force

# Regenerar
python analisis_universidades.py
```

### **Generar Reporte de Calidad de Datos**

```python
# Agregar al final de analisis_universidades.py

print("\n=== REPORTE DE CALIDAD ===")
print(f"Total: {len(df)} registros")
print(f"Completos: {len(df[df.isnull().sum(axis=1) == 0])} ({100*len(df[df.isnull().sum(axis=1) == 0])/len(df):.1f}%)")
print(f"Comunas: {df['comuna'].nunique()}")
print(f"Barrios: {df['barrio'].nunique()}")
print(f"Coordenadas: {len(df[(df['latitud'].notna()) & (df['longitud'].notna())])}")
```

---

## Optimizaciones para Mejor Rendimiento

### **1. Minificar JavaScript (Opcional)**

Si el HTML se hace muy grande, puedes separar la lógica:

```powershell
# Crear archivo separado src/js/dashboard.js
# Cargar con <script src="src/js/dashboard.js"></script>
```

### **2. Caché de Datos**

Agregar Service Worker para offline:

```javascript
// src/js/service-worker.js
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/dashboard_data_inline.js'
      ]);
    })
  );
});
```

### **3. Compresión de Imágenes**

Si agregas logos o screenshots:

```bash
# Usar ImageMagick o similar
magick image.jpg -quality 85 image-optimized.jpg
```

---

## Verificación Post-Ejecución

### **Checklist de Validación**

- [ ] Dashboard carga sin errores
- [ ] KPIs muestran números correctos
- [ ] Gráfico de barras se dibuja
- [ ] Gráfico de torta se dibuja
- [ ] Mapa aparece centrado en Buenos Aires
- [ ] Click en barra filtra datos
- [ ] Click en torta filtra datos
- [ ] Filtro por comuna funciona
- [ ] Filtro por barrio funciona
- [ ] Botón "Reiniciar filtros" reseteea todo
- [ ] Selector de comuna muestra universidades
- [ ] Click en universidad navega al mapa

### **Verificación de Rendimiento**

Abre la consola del navegador (F12) y ejecuta:

```javascript
// Ver tiempo de carga
console.time("renderizado");
// ... interactúa con dashboard
console.timeEnd("renderizado");

// Ver memoria usada
console.log("Datos cargados:", window.dashboardData.universidades.length);
```

**Valores esperados:**
- Carga inicial: < 2 segundos
- Cambio de filtro: < 500ms
- Memoria datos: ~2MB

---

## Desarrollo y Debugging

### **Activar Modo Depuración**

Agregar al inicio del `<script>` en index.html:

```javascript
// Modo debug
const DEBUG = true;
const log = (...args) => DEBUG && console.log('[DEBUG]', ...args);

log('Dashboard iniciando...');
log('Datos disponibles:', window.dashboardData);
```

### **Ver Estado del Dashboard en Consola**

```javascript
// En consola del navegador
console.log('Estado actual:', {
  filtroComuna: document.getElementById('filter-comuna').value,
  filtroBarrio: document.getElementById('filter-barrio').value,
  datosVisibles: getFilteredUniversidades().length
});
```

### **Inspeccionar Datos de Gráfico**

```javascript
// En consola
const barChartData = document.getElementById('bar-chart')._fullLayout;
console.log('Barras:', barChartData.xaxis.title);

const pieChartData = document.getElementById('pie-chart')._fullLayout;
console.log('Comunas:', pieChartData.title);
```

---

## Próximos Pasos

1. **Separar código JavaScript** en módulos (charts.js, map.js, filters.js)
2. **Agregar persistencia** de filtros en URL
3. **Implementar exportación** de datos (CSV, PNG)
4. **Crear versión móvil** optimizada
5. **Agregar análisis adicional** (estadísticas, tendencias)

---

## Contacto y Soporte

- **Errores en ejecución:** Revisa el Troubleshooting
- **Preguntas de datos:** Ver docs/PREPARACION_DATOS.md
- **Preguntas de arquitectura:** Ver docs/ARQUITECTURA.md
- **Modificaciones:** Ver comentarios en index.html

---

*Última actualización: 29 de abril de 2026*

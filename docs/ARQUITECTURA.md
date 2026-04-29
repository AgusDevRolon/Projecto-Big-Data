# Arquitectura Técnica del Dashboard

## Descripción General

El dashboard de universidades utiliza una arquitectura **cliente-servidor ligeramente acoplada** con:
- **Backend:** Python (Pandas/NumPy) para procesamiento de datos
- **Frontend:** HTML5 + JavaScript (Plotly + Leaflet) para visualización
- **Comunicación:** JSON como formato de intercambio

```
┌─────────────────────────────────────────┐
│        PIPELINE DE DATOS                │
├─────────────────────────────────────────┤
│                                         │
│  CSV (universidades.csv)                │
│    ↓                                    │
│  Python (analisis_universidades.py)     │
│    • Carga: pd.read_csv()               │
│    • Limpieza: dropna(), drop_duplicates│
│    • Transformación: Regex parsing      │
│    ↓                                    │
│  JSON (dashboard_data_inline.js)        │
│    ↓                                    │
│  HTML (index.html) + JavaScript         │
│    • Plotly.js (gráficos)               │
│    • Leaflet.js (mapa)                  │
│    • Filtros e interactividad           │
│    ↓                                    │
│  Navegador web (Visualización)          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Componentes Principales

### 1. **Capa de Datos (Data Layer)**

**Archivo:** `universidades.csv` → `universidades.json` → `dashboard_data_inline.js`

**Estructura del objeto `dashboardData`:**
```javascript
window.dashboardData = {
  universidades: [
    {
      nombre: "Universidad de Buenos Aires",
      barrio: "San Nicolás",
      comuna: 1,
      latitud: -34.603722,
      longitud: -58.381592,
      dirreccion: "Avenida Figueroa Alcorta 2263",
      telefono: "11-4576-3600",
      web: "www.uba.ar",
      sede: "Matriz",
      unidad_aca: "Rectorado"
    },
    // ... más universidades
  ],
  comunas: [1, 2, 3, ..., 15],
  barrios: ["San Nicolás", "Recoleta", ...]
};
```

**Características:**
- Datos pre-procesados (sin necesidad de cálculos en cliente)
- Carga única al inicio de la página
- ~50KB gzipeado

---

### 2. **Capa de Presentación (Presentation Layer)**

**Archivo:** `index.html`

**Estructura HTML:**
```html
<html>
├── HEAD
│   └── Estilos CSS + CDN (Plotly, Leaflet)
└── BODY
    ├── Container
    │   ├── Encabezado
    │   ├── Panel de Justificación
    │   ├── Panel de KPIs
    │   ├── Panel de Filtros
    │   ├── Gráfico de Barras
    │   ├── Gráfico de Torta
    │   ├── Mapa Interactivo
    │   ├── Selector de Comuna
    │   └── Pie de página
    └── SCRIPT
        └── Lógica de interactividad
```

---

### 3. **Capa de Lógica (Business Logic Layer)**

**Localización:** Dentro del `<script>` de `index.html`

**Funciones Principales:**

#### A. **Funciones de Construcción de Datos**
```javascript
buildCounts(dataArray, key)
  → Construye objeto de conteos
  → Input: Array de universidades, clave a agrupar
  → Output: Array de {name, count}
```

#### B. **Funciones de Actualización de UI**
```javascript
updateKPIs(filteredData)
  → Actualiza indicadores clave
  
updateFilterOptions()
  → Carga opciones de filtros
  
updateBarChart(filteredData)
  → Redibuja gráfico de barras
  
updatePieChart(filteredData)
  → Redibuja gráfico de torta
  
updateLeafletMarkers(filteredData)
  → Actualiza markers en mapa
```

#### C. **Funciones de Filtrado**
```javascript
getFilteredUniversidades()
  → Aplica filtros globales
  → Retorna: Array filtrado
  
setGlobalFilters(comuna, barrio)
  → Establece filtros desde gráficos
  
resetFilters()
  → Limpia todos los filtros
  
applyFilters()
  → Orquesta actualización de todo
```

#### D. **Funciones de Interacción**
```javascript
attachBarClickHandler()
  → Escucha clicks en barras
  
attachPieClickHandler()
  → Escucha clicks en torta
  
mostrarDetalle(universidad, marker)
  → Muestra información detallada
  
actualizarComuna()
  → Maneja cambio de comuna
```

---

## Flujo de Interacción

### **Caso 1: Usuario selecciona filtro por comuna**

```
Usuario: Click en "Filtrar por Comuna"
  ↓
JavaScript: Event listener 'change' en select
  ↓
applyFilters() [línea 507]
  ↓
getFilteredUniversidades() [aplica condiciones]
  ↓
Paralelo:
  ├─ updateKPIs(filteredData)        [actualiza números]
  ├─ updateBarChart(filteredData)    [redibuja barras]
  ├─ updatePieChart(filteredData)    [redibuja torta]
  └─ updateLeafletMarkers(filteredData) [actualiza mapa]
  ↓
Resultado visual: Todos los gráficos muestran datos filtrados
```

### **Caso 2: Usuario hace click en una barra del gráfico**

```
Usuario: Click en barra "Recoleta"
  ↓
JavaScript: Event listener 'plotly_click' en barChartDiv
  ↓
attachBarClickHandler() [línea 355]
  ↓
Extrae barrio de eventData.points[0].y
  ↓
setGlobalFilters() [línea 495]
  • Establece filterBarrio.value = "Recoleta"
  • Encuentra comuna asociada
  • Establece filterComuna.value también
  ↓
Dispara applyFilters() [misma orquestación]
  ↓
Resultado visual: Filtro aplicado, gráficos actualizados, mapa centrado
```

### **Caso 3: Usuario navega entre comunas en el selector inferior**

```
Usuario: Selecciona Comuna en dropdown
  ↓
JavaScript: Event listener 'change' en comunaSelect
  ↓
actualizarComuna() [línea 530]
  ↓
Filtra universidades por comuna seleccionada
  ↓
Genera lista HTML con eventos de click
  ↓
Event listeners en items de lista
  ↓
Click en universidad → mostrarDetalle()
  ↓
Resultado visual: Información detallada, mapa centrado
```

---

## Mejoras Propuestas para Interacción Gráficos-Mapa

### **Problema Actual:**
- Lógica de interacción está mezclada en un único `<script>`
- Difícil de mantener y extender
- Sincronización entre componentes acoplada

### **Solución Propuesta: Separación en Módulos**

**Estructura recomendada:**

```
src/js/
├── core/
│   ├── state.js           # Gestión de estado global
│   ├── data.js            # Gestión de datos
│   └── events.js          # Sistema de eventos
│
├── components/
│   ├── kpis.js            # Actualización de KPIs
│   ├── charts.js          # Gráficos (Plotly)
│   ├── map.js             # Mapa (Leaflet)
│   └── filters.js         # Filtros y selectors
│
└── main.js                # Punto de entrada
```

**Ventajas:**
- Mayor modularidad
- Fácil testing
- Reutilización de componentes
- Mejor rendimiento (lazy loading)

---

## Sincronización Gráficos-Mapa Mejorada

### **Arquitectura de Eventos Sugerida:**

```javascript
// Sistema de eventos centralizado
const EventBus = {
  listeners: {},
  
  on(event, handler) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(handler);
  },
  
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(h => h(data));
    }
  }
};

// Uso:
EventBus.on('filter-applied', (filteredData) => {
  updateBarChart(filteredData);
  updatePieChart(filteredData);
  updateLeafletMarkers(filteredData);
  updateKPIs(filteredData);
});

EventBus.on('barrio-selected', (barrio) => {
  setGlobalFilters(null, barrio);
});
```

---

## Consideraciones de Rendimiento

### **Optimizaciones Aplicadas:**
1. ✓ Datos inlineados (evita HTTP request extra)
2. ✓ Plotly responsive: renderización adaptativa
3. ✓ Leaflet optimizado: clustering de markers
4. ✓ CSS minimalista: sin frameworks pesados

### **Posibles Mejoras:**
- [ ] Virtualización de listas largas
- [ ] Web Workers para cálculos
- [ ] Service Workers para caché
- [ ] Compresión gzip en servidor

---

## Dependencias Externas

| Librería | Versión | Propósito | URL |
|----------|---------|----------|-----|
| Plotly.js | 2.24.2 | Gráficos | https://cdn.plot.ly/plotly-2.24.2.min.js |
| Leaflet | 1.9.4 | Mapas | https://unpkg.com/leaflet@1.9.4/ |
| OpenStreetMap | - | Tiles | https://tile.openstreetmap.org/ |

Todas son CDN públicas sin necesidad de API keys.

---

## Seguridad

- ✓ No hay datos sensibles en el frontend
- ✓ Validación de entrada en filtros
- ✓ XSS protection (texto sanitizado)
- ✓ No hay conexión a base de datos externa

---

## Testing

### **Recomendaciones para QA:**

1. **Pruebas funcionales:**
   - [ ] Filtro por comuna: actualiza todos los gráficos
   - [ ] Filtro por barrio: filtra correctamente
   - [ ] Click en barra: aplica filtro barrio
   - [ ] Click en torta: aplica filtro comuna
   - [ ] Reset filtros: muestra datos completos

2. **Pruebas de rendimiento:**
   - [ ] Tiempo de renderización inicial < 2s
   - [ ] Cambio de filtro < 500ms
   - [ ] Sin memory leaks en múltiples cambios

3. **Pruebas cross-browser:**
   - [ ] Chrome/Edge (Chromium)
   - [ ] Firefox
   - [ ] Safari
   - [ ] Navegadores móviles

---

*Última actualización: 29 de abril de 2026*

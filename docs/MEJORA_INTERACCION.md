# Plan de Mejora: Interacción Gráficos-Mapa

## Descripción del Problema Actual

El dashboard actual integra gráficos, filtros y mapa en una página única con interactividad bidireccional. Sin embargo, la sincronización entre componentes puede mejorarse significativamente.

### **Interacción Actual:**

```
Usuario selecciona en gráfico
         ↓
Event handler en Plotly
         ↓
Filtros globales se actualizan
         ↓
applyFilters() dispara
         ↓
Todos los componentes se redibujan
```

**Problemas:**
- Lógica acoplada en un único script
- Difícil de depurar
- No escalable para más visualizaciones

---

## Solución Propuesta: Sistema de Eventos

### **Arquitectura Mejorada:**

```
┌─────────────────────────────────────────┐
│         EVENT BUS (Central)             │
│  ┌──────────────────────────────────┐   │
│  │ Eventos disponibles:             │   │
│  │ - 'filter-applied'               │   │
│  │ - 'barrio-selected'              │   │
│  │ - 'comuna-selected'              │   │
│  │ - 'marker-clicked'               │   │
│  │ - 'filters-reset'                │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
         ↑         ↑         ↑
         │         │         │
    ┌────┴──┬─────┴──┬──────┴────┐
    │       │        │           │
 CHARTS   MAP    FILTERS       KPIs
```

### **Implementación del Event Bus:**

```javascript
// core/events.js
class EventBus {
  constructor() {
    this.listeners = {};
  }
  
  on(event, handler) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(handler);
    
    // Retornar función para unsubscribe
    return () => {
      this.listeners[event] = this.listeners[event].filter(h => h !== handler);
    };
  }
  
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(handler => {
        handler(data);
      });
    }
  }
}

// Exportar instancia global
window.eventBus = new EventBus();
```

---

## Casos de Uso Específicos

### **Caso 1: Usuario Hace Click en Barra del Gráfico**

**Flujo Mejorado:**

```javascript
// components/charts.js
function attachBarClickHandler() {
  document.getElementById('bar-chart').on('plotly_click', function(data) {
    const barrio = data.points[0].y;
    
    // Emitir evento
    window.eventBus.emit('barrio-selected', {
      barrio: barrio,
      timestamp: Date.now()
    });
  });
}

// components/filters.js
window.eventBus.on('barrio-selected', (data) => {
  const { barrio } = data;
  
  // Actualizar select
  document.getElementById('filter-barrio').value = barrio;
  
  // Buscar comuna
  const universidad = window.dashboardData.universidades.find(
    u => u.barrio === barrio
  );
  if (universidad) {
    document.getElementById('filter-comuna').value = universidad.comuna;
  }
  
  // Emitir evento de filtros aplicados
  window.eventBus.emit('filters-applied', {
    comuna: universidad.comuna,
    barrio: barrio
  });
});

// components/charts.js
window.eventBus.on('filters-applied', (filters) => {
  const filteredData = getFilteredUniversidades();
  updateBarChart(filteredData);
  updatePieChart(filteredData);
});

// components/map.js
window.eventBus.on('filters-applied', (filters) => {
  const filteredData = getFilteredUniversidades();
  updateLeafletMarkers(filteredData);
  // Opcionalmente, centrar mapa en barrio seleccionado
  if (filters.barrio) {
    centerMapOnBarrio(filters.barrio);
  }
});

// components/kpis.js
window.eventBus.on('filters-applied', (filters) => {
  const filteredData = getFilteredUniversidades();
  updateKPIs(filteredData);
});
```

**Ventajas:**
- Cada componente es independiente
- No hay acoplamiento fuerte
- Fácil agregar nuevos componentes
- Facilita testing

---

### **Caso 2: Sincronización Bidireccional Mapa-Gráficos**

**Mejora sugerida: Click en Marker del Mapa**

```javascript
// components/map.js
function attachMarkerClickHandlers() {
  markers.forEach(marker => {
    marker.on('click', function(e) {
      const universidad = e.target.universidad; // almacenar en marker
      
      // Emitir evento
      window.eventBus.emit('marker-clicked', {
        universidad: universidad,
        latitud: e.latlng.lat,
        longitud: e.latlng.lng
      });
    });
  });
}

// components/filters.js
window.eventBus.on('marker-clicked', (data) => {
  const { universidad } = data;
  
  // Aplicar filtros basados en universidad
  document.getElementById('filter-barrio').value = universidad.barrio;
  document.getElementById('filter-comuna').value = universidad.comuna;
  
  window.eventBus.emit('filters-applied', {
    comuna: universidad.comuna,
    barrio: universidad.barrio,
    source: 'map-marker'
  });
});

// components/detail-panel.js
window.eventBus.on('marker-clicked', (data) => {
  const { universidad } = data;
  mostrarDetalle(universidad);
  
  // Scroll a detalles
  document.getElementById('universidad-detalle').scrollIntoView();
});
```

---

## Modularización del Código JavaScript

### **Estructura Propuesta:**

```
src/
├── js/
│   ├── core/
│   │   ├── events.js          # EventBus central
│   │   ├── state.js           # Gestión de estado
│   │   └── data.js            # Acceso a datos
│   │
│   ├── components/
│   │   ├── kpis.js            # Actualización de KPIs
│   │   ├── charts.js          # Gráficos (Plotly)
│   │   │   ├── bar-chart.js
│   │   │   └── pie-chart.js
│   │   ├── map.js             # Mapa (Leaflet)
│   │   ├── filters.js         # Filtros y selectors
│   │   └── detail-panel.js    # Panel de detalles
│   │
│   ├── utils/
│   │   ├── formatters.js      # Formateo de datos
│   │   ├── validators.js      # Validaciones
│   │   └── helpers.js         # Funciones auxiliares
│   │
│   └── main.js                # Punto de entrada
```

### **Archivo: src/js/core/state.js**

```javascript
// Gestión centralizada de estado
class StateManager {
  constructor() {
    this.state = {
      filters: {
        comuna: '',
        barrio: ''
      },
      selectedItem: null,
      filteredData: []
    };
  }
  
  getState() {
    return this.state;
  }
  
  setState(newState) {
    this.state = { ...this.state, ...newState };
    window.eventBus.emit('state-changed', this.state);
  }
  
  getFilteredData() {
    const { universidades } = window.dashboardData;
    const { Comuna, barrio } = this.state.filters;
    
    return universidades.filter(u => {
      const comunaMatch = !comuna || u.comuna === parseInt(comuna);
      const barrioMatch = !barrio || u.barrio === barrio;
      return comunaMatch && barrioMatch;
    });
  }
}

window.stateManager = new StateManager();
```

### **Archivo: src/js/main.js**

```javascript
// Punto de entrada unificado
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Verificar datos disponibles
    if (!window.dashboardData) {
      throw new Error('Dashboard data no cargada');
    }
    
    // Inicializar componentes
    await Promise.all([
      initKPIs(),
      initFilters(),
      initCharts(),
      initMap(),
      initDetailPanel()
    ]);
    
    // Establecer listeners de eventos
    window.eventBus.on('filters-applied', () => {
      console.log('Filtros aplicados, sincronizando...');
    });
    
    console.log('✓ Dashboard inicializado correctamente');
  } catch (error) {
    console.error('Error en inicialización:', error);
    showErrorMessage(error.message);
  }
});

// Funciones de inicialización
async function initKPIs() {
  // Lógica de KPIs
}

async function initFilters() {
  // Lógica de filtros
}

async function initCharts() {
  // Lógica de gráficos
}

async function initMap() {
  // Lógica de mapa
}

async function initDetailPanel() {
  // Lógica de panel de detalles
}
```

---

## Persistencia de Filtros en URL

### **Implementación Sugerida:**

```javascript
// utils/url-state.js
class URLStateManager {
  save(state) {
    const params = new URLSearchParams();
    params.set('comuna', state.filters.comuna || '');
    params.set('barrio', state.filters.barrio || '');
    
    window.history.replaceState(null, '', `?${params}`);
  }
  
  restore() {
    const params = new URLSearchParams(window.location.search);
    return {
      filters: {
        comuna: params.get('comuna') || '',
        barrio: params.get('barrio') || ''
      }
    };
  }
}

// En main.js
const urlState = new URLStateManager();
const savedState = urlState.restore();
window.stateManager.setState(savedState);

// Guardar cuando cambian filtros
window.eventBus.on('filters-applied', (filters) => {
  urlState.save(window.stateManager.getState());
});
```

**Uso:**
```
http://localhost:8000/?comuna=1&barrio=Recoleta
→ Se cargarán automáticamente los filtros
```

---

## Testing de Interacción

### **Suite de Tests Recomendada:**

```javascript
// tests/filters.test.js
describe('Interaction Tests', () => {
  beforeEach(() => {
    // Setup
    initDashboard();
  });
  
  it('debería filtrar cuando se selecciona una comuna', async () => {
    selectComuna('1');
    await delay(500);
    
    const visibleUniversities = getVisibleUniversities();
    expect(visibleUniversities).toHaveLength(
      window.dashboardData.universidades.filter(u => u.comuna === 1).length
    );
  });
  
  it('debería actualizar mapa cuando se hace click en barra', async () => {
    clickBar('Recoleta');
    await delay(500);
    
    const mapCenter = window.map.getCenter();
    const recoletaUniv = window.dashboardData.universidades.find(
      u => u.barrio === 'Recoleta'
    );
    
    expect(mapCenter).toBeCloseTo(
      [recoletaUniv.latitud, recoletaUniv.longitud]
    );
  });
  
  it('debería sincronizar filtros cuando se hace click en marcador', async () => {
    clickMarker(0);
    await delay(500);
    
    const selectedUniversity = window.dashboardData.universidades[0];
    const filterBarrio = getFilterValue('filter-barrio');
    
    expect(filterBarrio).toBe(selectedUniversity.barrio);
  });
});
```

---

## Performance Optimization

### **Técnicas Recomendadas:**

```javascript
// 1. Debounce para eventos frecuentes
function debounce(func, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

// Uso:
const debouncedApplyFilters = debounce(applyFilters, 300);
filterSelect.addEventListener('change', debouncedApplyFilters);

// 2. Memoization de datos filtrados
const memoizedFilter = (() => {
  let cache = {};
  return (filters) => {
    const key = JSON.stringify(filters);
    if (cache[key]) return cache[key];
    
    const result = getFilteredUniversidades(filters);
    cache[key] = result;
    return result;
  };
})();

// 3. Virtual scrolling para listas largas
// Usar bibliotecas como: 'virtual-scroll' o 'react-virtual'
```

---

## Roadmap de Implementación

### **Fase 1: Preparación (1-2 horas)**
- [ ] Crear estructura de carpetas `src/js/`
- [ ] Crear EventBus en `core/events.js`
- [ ] Crear StateManager en `core/state.js`

### **Fase 2: Refactorización (3-4 horas)**
- [ ] Separar código de gráficos en `components/charts.js`
- [ ] Separar código de mapa en `components/map.js`
- [ ] Separar código de filtros en `components/filters.js`
- [ ] Separar código de KPIs en `components/kpis.js`

### **Fase 3: Mejoras (2-3 horas)**
- [ ] Implementar persistencia de URL
- [ ] Agregar manejo de errores robusto
- [ ] Optimizar performance con debounce/memoization

### **Fase 4: Testing (2-3 horas)**
- [ ] Escribir tests unitarios
- [ ] Tests de integración
- [ ] Testing de performance

---

## Beneficios de Esta Arquitectura

✓ **Modularidad:** Cada componente es independiente  
✓ **Escalabilidad:** Fácil agregar nuevas visualizaciones  
✓ **Mantenibilidad:** Código más limpio y organizado  
✓ **Testabilidad:** Componentes aislados y testables  
✓ **Reusabilidad:** Componentes reutilizables  
✓ **Performance:** Optimizaciones más simples  

---

*Última actualización: 29 de abril de 2026*

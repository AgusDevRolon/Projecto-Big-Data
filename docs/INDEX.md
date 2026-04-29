# Índice de Documentación del Proyecto

## 📁 Estructura del Proyecto

```
Projecto-Big-Data/
│
├── 📄 README.md                          ← COMIENZA AQUÍ
│   └── Documentación completa del proyecto (7 requisitos académicos)
│
├── 📄 index.html                         ← DASHBOARD PRINCIPAL
│   └── Landing page interactiva con todos los gráficos
│
├── 📁 src/                               
│   ├── analisis_universidades.py         ← Script de procesamiento de datos
│   └── (Próximamente: módulos JavaScript separados)
│
├── 📁 data/
│   ├── universidades.csv                 ← Dataset original (Bruno Aires Data)
│   ├── universidades.json                ← JSON procesado
│   └── dashboard_data.json               ← Datos optimizados
│
├── 📁 public/
│   ├── dashboard_data_inline.js          ← Datos inline para HTML
│   └── dashboard_universidades.html      ← Gráficos generados (alternativa)
│
├── 📁 docs/                              ← DOCUMENTACIÓN TÉCNICA
│   ├── 📖 ARQUITECTURA.md                ← Diseño técnico del sistema
│   ├── 📖 PREPARACION_DATOS.md           ← Limpieza y transformación de datos
│   ├── 📖 COMO_EJECUTAR.md               ← Guía de uso y troubleshooting
│   ├── 📖 MEJORA_INTERACCION.md          ← Plan de mejora futura
│   └── 📖 INDEX.md                       ← Este archivo
│
└── 📁 .git/                              ← Control de versiones

```

---

## 📚 Guía de Lectura Recomendada

### **Para Entender el Proyecto:**
1. **[README.md](../README.md)** (15-20 min)
   - Visión general del proyecto
   - Requisitos académicos cubiertos (1-7)
   - Justificación de tecnologías

### **Para Usar el Dashboard:**
2. **[COMO_EJECUTAR.md](./COMO_EJECUTAR.md)** (5-10 min)
   - Pasos para abrir el dashboard
   - Troubleshooting común
   - Modo debug

### **Para Entender la Arquitectura:**
3. **[ARQUITECTURA.md](./ARQUITECTURA.md)** (20-30 min)
   - Componentes del sistema
   - Flujos de interacción
   - Stack tecnológico

### **Para Entender la Calidad de Datos:**
4. **[PREPARACION_DATOS.md](./PREPARACION_DATOS.md)** (20-30 min)
   - Fases de procesamiento
   - Problemas encontrados y soluciones
   - Estadísticas finales

### **Para Futuro Desarrollo:**
5. **[MEJORA_INTERACCION.md](./MEJORA_INTERACCION.md)** (30-40 min)
   - Plan de modularización
   - Sistema de eventos propuesto
   - Roadmap técnico

---

## 🎯 Requisitos Académicos Cubiertos

### ✅ **Requisito 1: Selección del Dataset**
- **Ubicación:** README.md - Sección "Requisito 1: Selección del Dataset"
- **Resumen:** Dataset de Buenos Aires Data con 191 universidades
- **Tamaño:** 199 registros → 191 después de limpieza (100% validados)

### ✅ **Requisito 2: Justificación de Visualizaciones**
- **Ubicación:** README.md - Sección "Requisito 2: Justificación de Visualizaciones"
- **Visualizaciones:**
  - Gráfico de barras horizontal (comparación)
  - Gráfico de torta (composición)
  - Mapa interactivo (ubicación geográfica)
  - KPIs (resumen ejecutivo)

### ✅ **Requisito 3: Preparación de Datos**
- **Ubicación:** 
  - README.md - Sección "Requisito 3: Preparación de Datos"
  - PREPARACION_DATOS.md - Documentación completa
- **Fases:** Exploración → Limpieza → Transformación → Validación
- **Problemas resueltos:** 7 problemas comunes (NaN, duplicados, encoding, etc.)

### ✅ **Requisito 4: Herramientas Utilizadas**
- **Ubicación:** README.md - Sección "Requisito 4: Herramientas Utilizadas"
- **Backend:** Python 3.9+, Pandas, NumPy, Plotly
- **Frontend:** HTML5, CSS3, JavaScript, Plotly.js, Leaflet.js
- **Datos:** CSV, JSON, OpenStreetMap

### ✅ **Requisito 5: Elementos del Dashboard**
- **Ubicación:** README.md - Sección "Requisito 5: Elementos del Dashboard"
- **Elementos:**
  - Panel de KPIs
  - Filtros globales
  - Gráficos interactivos
  - Mapa con sincronización
  - Explorador de detalles
  - Explicaciones contextuales

### ✅ **Requisito 6: Landing Page Web**
- **Ubicación:** index.html (archivo principal)
- **Características:**
  - Diseño responsivo (mobile-friendly)
  - Todos los gráficos integrados
  - Interactividad completa
  - Zero dependencies críticas

### ✅ **Requisito 7: Efectividad de Visualizaciones**
- **Ubicación:** README.md - Sección "Requisito 7: Efectividad de Visualizaciones"
- **Análisis:** Claridad, Precisión, Eficiencia, Estética, Integridad
- **Validación:** Contra estándares internacionales (Tufte, Tableau, etc.)

---

## 🔧 Archivos Principales

### **analisis_universidades.py**
```python
# Funciones principales:
# 1. Cargar CSV
# 2. Limpiar datos (NaN, duplicados, normalización)
# 3. Transformar (extracción de coordenadas con regex)
# 4. Exportar JSON para dashboard
# 5. Generar dashboard_data_inline.js
```

### **index.html**
```html
<!-- Componentes principales: -->
<!-- 1. Estilos CSS embebidos (responsive) -->
<!-- 2. Panel de KPIs -->
<!-- 3. Panel de Filtros -->
<!-- 4. Gráficos (Plotly.js) -->
<!-- 5. Mapa (Leaflet.js) -->
<!-- 6. Explorador de detalles -->
<!-- 7. Lógica JavaScript embebida -->
```

### **dashboard_data_inline.js**
```javascript
// Contiene:
window.dashboardData = {
  universidades: [...],  // 191 registros con todas las propiedades
  comunas: [...],        // 15 comunas (1-15)
  barrios: [...]         // 48 barrios únicos
}
```

---

## 📊 Estadísticas del Proyecto

### **Datos:**
- Registros procesados: 199 → 191 (limpieza: 4%)
- Campos utilizados: 11 originales → 9 críticos
- Comunas: 15
- Barrios: 48
- Coordenadas válidas: 191 (100%)

### **Código:**
- Líneas Python: ~150
- Líneas HTML: ~600
- Líneas JavaScript: ~450
- Líneas CSS: ~150
- Documentación: ~2500 líneas

### **Rendimiento:**
- Tamaño HTML: ~180 KB
- Tamaño JSON inline: ~45 KB (gzipeado)
- Tiempo de carga: <2 segundos
- Tiempo de interacción: <500ms

---

## 🚀 Quick Start

### **Opción 1: Instante (Recomendado)**
```
1. Navega a: c:\Users\Agustín\Desktop\big data\Projecto-Big-Data
2. Haz doble click en: index.html
3. Disfruta del dashboard
```

### **Opción 2: Con Servidor Local**
```bash
cd "c:\Users\Agustín\Desktop\big data\Projecto-Big-Data"
python -m http.server 8000
# Abre: http://localhost:8000
```

### **Opción 3: Regenerar Datos (si quieres entender el proceso)**
```bash
python analisis_universidades.py
# Luego abre index.html
```

---

## 📖 Temas Documentados

| Tema | Ubicación | Duración |
|------|-----------|----------|
| Visión general del proyecto | README.md | 5 min |
| Uso del dashboard | COMO_EJECUTAR.md | 5 min |
| Fases de data preparation | PREPARACION_DATOS.md | 20 min |
| Troubleshooting | COMO_EJECUTAR.md | 10 min |
| Arquitectura técnica | ARQUITECTURA.md | 20 min |
| Flujos de interacción | ARQUITECTURA.md | 10 min |
| Futuras mejoras | MEJORA_INTERACCION.md | 30 min |
| Justificación académica | README.md | 15 min |

---

## 🔍 Índice por Pregunta Frecuente

### **¿Cómo abro el dashboard?**
→ COMO_EJECUTAR.md - "Inicio Rápido"

### **¿Qué datos usaste?**
→ README.md - "Requisito 1: Selección del Dataset"

### **¿Por qué estos gráficos?**
→ README.md - "Requisito 2: Justificación de Visualizaciones"

### **¿Cómo limpian los datos?**
→ PREPARACION_DATOS.md - Completo

### **¿Cómo funcionan los filtros?**
→ ARQUITECTURA.md - "Flujo de Interacción"

### **¿Cómo mejoro la interacción?**
→ MEJORA_INTERACCION.md - Completo

### **¿Qué significa cada KPI?**
→ README.md - "Requisito 5: Elementos del Dashboard"

### **¿Es responsive el dashboard?**
→ README.md & index.html (CSS @media queries)

### **¿Puedo exportar datos?**
→ MEJORA_INTERACCION.md - "Fase 3: Mejoras"

### **¿Cómo agrego nuevas universidades?**
→ COMO_EJECUTAR.md - "Scripts Útiles"

---

## 🎓 Para Presentación Académica

### **Diapositivas recomendadas:**
1. **Portada:** Título del proyecto
2. **Contexto:** Buenos Aires Data, 191 universidades
3. **Metodología:** Fases de preparación (PREPARACION_DATOS.md)
4. **Dataset:** Estructura y campos (README.md - Requisito 1)
5. **Limpieza:** Problemas encontrados (PREPARACION_DATOS.md)
6. **Visualizaciones:** Justificación (README.md - Requisito 2)
7. **Herramientas:** Stack tecnológico (README.md - Requisito 4)
8. **Dashboard:** Demo en vivo (index.html)
9. **Resultados:** Estadísticas finales
10. **Conclusión:** Impacto y futuro

### **Demostración Live:**
```
1. Abrir dashboard en pantalla completa
2. Mostrar KPIs (números clave)
3. Hacer click en una barra → filtro aplicado
4. Hacer click en torta → filtro aplicado
5. Hacer click en mapa → mostrar detalles
6. Filtrar por comuna → todo se sincroniza
```

---

## 🤝 Colaboración

### **Para contribuyentes:**
1. Lee README.md primero
2. Luego ARQUITECTURA.md
3. Propón cambios en MEJORA_INTERACCION.md
4. Implementa en rama separada
5. Documenta cambios

---

## 📋 Checklist de Completitud

- [x] Dataset seleccionado y validado
- [x] Datos limpios y transformados
- [x] Visualizaciones justificadas
- [x] Herramientas seleccionadas
- [x] Dashboard funcional
- [x] Landing page completa
- [x] Documentación académica
- [x] Documentación técnica
- [x] Código bien estructurado
- [x] Ejemplos y tutoriales

---

## 📚 Referencias Externas

- [Buenos Aires Data](https://datos.buenosaires.gob.ar/)
- [Plotly Documentation](https://plotly.com/javascript/)
- [Leaflet Documentation](https://leafletjs.com/)
- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)
- [Python Pandas Guide](https://pandas.pydata.org/docs/)

---

## ❓ Preguntas o Problemas

Consulta en este orden:
1. README.md (conceptos)
2. COMO_EJECUTAR.md (ejecución)
3. ARQUITECTURA.md (técnica)
4. PREPARACION_DATOS.md (datos)

---

*Última actualización: 29 de abril de 2026*

**Proyecto Académico - Visualización de Datos**  
**Universidades en Buenos Aires**

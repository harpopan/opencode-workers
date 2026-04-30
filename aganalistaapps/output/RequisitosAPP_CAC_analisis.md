# Análisis de Requisitos - Aplicación Móvil CAC

## 1. Resumen del Alcance

**Proyecto:** Aplicación móvil interactiva multiplataforma para la Ciutat de les Arts i les Ciències (Valencia)

**Tipo de aplicación:** Móvil nativaplataforma (iOS + Android) con posible versión web

**Características principales:**
- Geolocalización y posicionamiento GPS en tiempo real
- Realidad aumentada (AR) con ARKit/ARCore
- Inteligencia artificial (chatbot conversacional)
- Sistema de notificaciones push con Bluetooth beacons
- Audioguías interactivas
- Planos interactivos y mapas de calor
- Gamificación y sistema de recompensas
- Modo "en casa" post-visita

**Alcance temporal:** Desarrollo + Mantenimiento (4 años)

---

## 2. Evaluación de Complejidad Técnica

| Criterio | Nivel | Justificación |
|----------|-------|---------------|
| Complejidad técnica | **ALTA** | Integración múltiple de tecnologías avanzadas (AR, AI, beacons, geolocalización) |
| Cantidad de módulos | **ALTA** | 15 módulos funcionales claramente diferenciados |
| Integraciones externas | **ALTA** | Sistemas de control de aforo, beacons Bluetooth, App Stores, potencialmente sistemas legacy de CAC |
| Requisitos de rendimiento | **MEDIA-ALTA** | Tiempo real para geolocalización y notificaciones |
| Seguridad y privacidad | **ALTA** | Cumplimiento RGPD, datos de usuarios, registros de recorrido |
| Accesibilidad | **ALTA** | WCAG 2.1 AA, compatibilidad con lectores de pantalla |
| Multiidioma | **MEDIA** | 3 idiomas mínimos, arquitectura escalable |

**Clasificación general:** PROYECTO DE ALTA COMPLEJIDAD

---

## 3. Desglose de Funcionalidades Identificadas

### Módulos Principales

1. **Desarrollo Multiplataforma** - Compatibilidad iOS/Android (2 versiones anteriores mínima)
2. **Sistema Multiidioma** - Español, Valenciano, Inglés + arquitectura escalable
3. **Accesibilidad** - WCAG 2.1 AA, lectores de pantalla, subtítulos
4. **Perfiles de Usuario** - Registro opcional, personalización por edad/idioma/intereses
5. **Notificaciones Push + Beacons** - Bluetooth LE, geolocalización, tiempo real
6. **Geolocalización** - GPS, mapa interno, cálculo de tiempos, registros anónimos
7. **Realidad Aumentada** - ARKit/ARCore, experiencias 360°, captura y compartición
8. **Audioguía** - Reproducción automática, offline, velocidad, transcripción
9. **Sistema de Itinerarios** - Algoritmo redistribución, mapa de calor, estadísticas
10. **Plano Interactivo** - Zoom, POIs clicables, indicaciones paso a paso
11. **Chatbot AI** - Modelo conversacional, multilingüe, aprendizaje supervisado
12. **Gamificación** - Retos, insignias, rankings
13. **Valoraciones** - Sistema de puntuación de experiencias
14. **Modo "En Casa"** - Recursos post-visita, notificaciones eventos, recuerdos automáticos
15. **Backend/Admin** - Panel de gestión, estadísticas, contenidos

### Integraciones Requeridas

- Sistema de control de aforo (existente o a desarrollar)
- Red de datos/beacons de CAC
- App Store / Google Play
- potential sistemas de ticketing de CAC
- Redes sociales (compartición)

---

## 4. Estimación de Tiempo de Desarrollo

### Metodología Aplicada

- Factor de seguridad: **1.5x - 2x** sobre estimación base
- Buffer de imprevistos: **20-30%**
- Testing: **40-50%** del tiempo de desarrollo
- Redondeo: SIEMPRE hacia arriba

### Desglose por Fase

#### Fase 1: Análisis y Planificación

| Actividad | Estimación Base | Factor (1.25) | Resultado |
|-----------|-----------------|---------------|-----------|
| Análisis de requisitos | 40 horas | +25% | **50 horas** |
| Arquitectura del sistema | 24 horas | +25% | **30 horas** |
| Diseño UX/UI | 40 horas | +25% | **50 horas** |
| Planificación sprints | 16 horas | +25% | **20 horas** |
| **TOTAL FASE 1** | **120 horas** | | **150 horas (19 días)** |

#### Fase 2: Desarrollo

| Módulo | Estimación Base | Factor (1.5) | Resultado |
|--------|-----------------|---------------|-----------|
| Infraestructura backend | 80 horas | +50% | **120 horas** |
| API y servicios | 120 horas | +50% | **180 horas** |
| App iOS (核心 funcionalidades) | 200 horas | +50% | **300 horas** |
| App Android (core) | 200 horas | +50% | **300 horas** |
| Sistema de auth/perfiles | 40 horas | +50% | **60 horas** |
| Geolocalización y mapas | 80 horas | +50% | **120 horas** |
| Integración beacons | 60 horas | +50% | **90 horas** |
| Realidad Aumentada | 120 horas | +50% | **180 horas** |
| Audioguía | 60 horas | +50% | **90 horas** |
| Chatbot AI | 100 horas | +50% | **150 horas** |
| Gamificación | 60 horas | +50% | **90 horas** |
| Plano interactivo | 80 horas | +50% | **120 horas** |
| Itinerarios y estadísticas | 80 horas | +50% | **120 horas** |
| Modo "En Casa" | 40 horas | +50% | **60 horas** |
| Panel administrativo | 80 horas | +50% | **120 horas** |
| **TOTAL DESARROLLO** | **1,340 horas** | | **2,010 horas (252 días)** |

#### Fase 3: Testing

| Tipo de Prueba | Estimación Base | Factor (1.5) | Resultado |
|----------------|-----------------|---------------|-----------|
| Pruebas unitarias | 200 horas | +50% | **300 horas** |
| Pruebas integración | 160 horas | +50% | **240 horas** |
| Pruebas UI/UX | 80 horas | +50% | **120 horas** |
| Pruebas rendimiento | 60 horas | +50% | **90 horas** |
| Pruebas accesibilidad | 40 horas | +50% | **60 horas** |
| Beta testing (usuarios reales) | 80 horas | +50% | **120 horas** |
| **TOTAL TESTING** | **620 horas** | | **930 horas (116 días)** |

#### Fase 4: Documentación

| Documento | Estimación Base | Factor (1.25) | Resultado |
|-----------|-----------------|---------------|-----------|
| Documentación técnica | 40 horas | +25% | **50 horas** |
| Documentación de usuario | 24 horas | +25% | **30 horas** |
| Manuales de admin | 16 horas | +25% | **20 horas** |
| **TOTAL DOCUMENTACIÓN** | **80 horas** | | **100 horas (13 días)** |

#### Fase 5: Despliegue

| Actividad | Estimación Base | Factor (1.4) | Resultado |
|-----------|-----------------|---------------|-----------|
| Configuración infraestructura | 40 horas | +40% | **56 horas** |
| CI/CD pipeline | 24 horas | +40% | **34 horas** |
| Despliegue producción | 24 horas | +40% | **34 horas** |
| Publicación stores | 16 horas | +40% | **22 horas** |
| **TOTAL DESPLIEGUE** | **104 horas** | | **146 horas (18 días)** |

---

## 5. Resumen de Estimación Total (Desarrollo Inicial)

| Fase | Horas | Días (8h/día) |
|------|-------|---------------|
| Análisis y Planificación | 150 horas | 19 días |
| Desarrollo | 2,010 horas | 252 días |
| Testing | 930 horas | 116 días |
| Documentación | 100 horas | 13 días |
| Despliegue | 146 horas | 18 días |
| **TOTAL** | **2,336 horas** | **292 días** |

> **Nota:** 292 días ≈ 14-15 meses considerando fines de semana y festivos. Se estima **16 meses** con buffers adicionales para imprevistos.

---

## 6. Estimación de Mantenimiento (4 Años)

Según especificaciones del cliente: mantenimiento de 4 años incluido.

| Servicio | Estimación Anual | Factor (1.4) | 4 Años |
|----------|-----------------|---------------|--------|
| Corrección de errores | 320 horas | +40% | **448 horas/año** |
| Actualizaciones OS (iOS/Android) | 160 horas | +40% | **224 horas/año** |
| Soporte técnico | 480 horas | +40% | **672 horas/año** |
| Evolución funcional menor | 240 horas | +40% | **336 horas/año** |
| Seguridad y vulnerabilidades | 80 horas | +40% | **112 horas/año** |
| **TOTAL MANTENIMIENTO** | **1,280 horas/año** | | **1,792 horas/año** |

**Total mantenimiento 4 años:** **7,168 horas (896 días)**

Coste estimado: Considerando tasa horaria media de 50€/hora → **358,400€** (4 años)

---

## 7. Timeline Sugerido de Implementación

### Sprint 0: Preparación (Semanas 1-2)
- Setup entornos desarrollo
- Definición arquitectura técnica
- Kickoff con stakeholders

### Sprint 1-4: Fundamentos (Meses 2-3)
- Backend core y API
- Autenticación y perfiles
- Infraestructura base

### Sprint 5-10: Módulos Core (Meses 4-7)
- Geolocalización y mapas
- Sistema de notificaciones
- Integración beacons
- Panel administrativo

### Sprint 11-16: Features Avanzados (Meses 8-11)
- Realidad Aumentada
- Chatbot AI
- Audioguía
- Gamificación

### Sprint 17-20: Integración y Testing (Meses 12-14)
- Testing integral
- Beta testing
- Optimización rendimiento
- Accesibilidad

### Sprint 21-22: Despliegue (Meses 15-16)
- Publicación stores
- Monitorización
- Formación equipo CAC

### Mantenimiento Continuo (Meses 17+)
- Soporte y evolutivos
- Actualizaciones системы

---

## 8. Dependencias Identificadas

1. **Sistemas de CAC:** Sistema de control de acceso/aforo (requiere integración)
2. **Infraestructura de red:** Red WiFi/beacons de CAC para interior
3. **Proveedor beacons:** Suministro e instalación de hardware Bluetooth
4. **Modelos AI:** Selección de proveedor LLM o entrenamiento de modelo propio
5. **Sistemas de ticketing:** Integración opcional con venta de entradas
6. **Políticas stores:** apple App Store Review Guidelines, Google Play Policies

---

## 9. Riesgos Potenciales

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Retrasos por integración beacons | ALTA | ALTO | Prototipado temprano, proveedor dedicado |
| Problemas de rendimiento AR | MEDIA | ALTO | Testing en dispositivos reales, optimización progresiva |
| Cambios en políticas de stores | MEDIA | MEDIO | Monitorización continua, cumplimiento proactivo |
| Complejidad AI/ML | ALTA | ALTO | Proveedor especializado, MVP iterativo |
| Alcance cambiantes (scope creep) | ALTA | ALTO | Control de cambios riguroso, priorización |
| Disponibilidad sistemas de CAC | MEDIA | ALTO | Mockups y abstracción, desarrollo paralelo |
| Accesibilidad en AR | ALTA | MEDIO | Consultoría especializada, testing con usuarios |

---

## 10. Recomendaciones

1. **Enfoque iterativo:** Priorizar funcionalidades core (geolocalización, mapas, notificaciones) para primer release, features avanzadas (AR, AI) en actualizaciones posteriores.

2. **Proveedor beacons:** La empresa adjudicataria debe gestionar suministro e instalación. Incluir este entregable claramente en contrato.

3. **MVP sugerido:**
   - App base multiplataforma
   - Mapas interactivos
   - Geolocalización
   - Notificaciones básicas
   - Información de POIs
   - Audioguía básica

4. **Fase 2 (post-lanzamiento):**
   - Realidad Aumentada
   - Chatbot AI
   - Gamificación completa
   - Modo "En Casa"

5. **Contrato de mantenimiento:** Asegurar SLA <48h respuesta como especifica el pliego.

---

## 11. Contenidos

No se especifica volumen exacto de contenidos en los requisitos. Se asume necesario:

| Tipo | Estimación Preliminar | Tiempo Estimado |
|------|----------------------|-----------------|
| Textos (descripciones POIs) | ~50-100 páginas | 40-80 horas |
| Imágenes (fotos, infografías) | ~200-300 unidades | 50-75 horas |
| Audios (audioguías) | ~20-30 puntos × 2 idiomas | 80-120 horas |
| Videos (contenidos 360°) | ~5-10 unidades | 50-100 horas |
| **TOTAL APROXIMADO** | | **220-375 horas** |

> **Recomendación:** Solicitar al cliente volumen exacto de contenidos para refinamiento de estimación.

---

## 12. Notas sobre la Estimación

- **Factor de seguridad aplicado:** 1.5x mínimo en todas las fases
- **Buffer de imprevistos:** 20-30% incluido en factores
- **Testing:** 45% del tiempo de desarrollo (por encima del 40% mínimo especificado)
- **Redondeo:** Todos los valores redondeados hacia arriba
- **Supuestos:**
  - Equipo de 4-6 desarrolladores full-time
  - Disponibilidad de specs de integración con sistemas CAC
  - Proveedor de beacons asignado desde inicio
  - Acceso a entorno de producción para testing

**Estimación final consolidada:**

| Concepto | Horas | Días |
|----------|-------|------|
| Desarrollo inicial | 2,336 horas | 292 días (~16 meses) |
| Mantenimiento 4 años | 7,168 horas | 896 días |
| **TOTAL PROYECTO** | **9,504 horas** | **1,188 días** |

---

*Documento generado automáticamente. Los valores son estimaciones preliminares sujetas a refinamiento con información adicional del cliente.*
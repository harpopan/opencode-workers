# ProyectoDocumentacion

**Versión:** 1.3.0

Sistema de análisis de requisitos de aplicaciones y estimación de tiempos de desarrollo.

## Propósito

Analizar descripciones de aplicaciones desde archivos de entrada y generar documentación estructurada con estimaciones de tiempo, complejidad y timeline de implementación.

## Estructura

```
proyectodocumentacion/
├── input/                  # Archivos de requisitos (.md o .txt)
├── output/                 # Análisis generados
├── agents/                 # Definiciones de agentes
│   ├── analista.md        # Agente de análisis de requisitos
│   ├── documentador.md    # Agente de documentación
│   ├── mantenedor.md      # Agente de análisis de mantenimiento
│   └── contenidos.md     # Agente de análisis de contenidos
├── AGENTS.md               # Configuración del proyecto
└── README.md               # Este archivo
```

## Uso

1. **Crear archivo de requisitos**: Colocar un archivo `.md` o `.txt` en la carpeta `input/` describiendo las necesidades de la aplicación.

2. **Ejecutar análisis**: Invocar al agente para analizar el archivo y generar el análisis en `output/`.

3. **Generar documentación**: Utilizar el agente documentador para crear documentación completa.

## Agentes Disponibles

- **Analista**: Analiza requisitos y calcula estimaciones de tiempo de desarrollo
- **Documentador**: Transforma análisis en documentación profesional con diagramas
- **Mantenedor**: Analiza sostenibilidad y lifecycle a largo plazo (coste operativo, deuda técnica, evolutivos)
- **Contenidos**: Analiza implementación de contenidos (carga, estructuración, migración)

## Skills Disponibles

El proyecto incluye skills especializadas activables con comandos específicos:

| Skill | Activadores | Descripción |
|-------|-------------|-------------|
| `documentation` | "write docs for", "document this", "create README" | Documentación técnica profesional (READMEs, API docs, runbooks, guías de onboarding) |
| `mermaid-diagrams` | "diagram", "visualize", "model", "show the flow" | Diagramas Mermaid (ERD, flows, arquitectura C4, sequence, class, Gantt) |

### Uso de Diagramas en Documentación

El agente documentador utiliza `mermaid-diagrams` para generar:
- **Arquitectura**: Diagramas C4 (contexto, contenedor, componentes)
- **Flujos**: Flowcharts de procesos y user journeys
- **Datos**: ERD del modelo de datos
- **Secuencias**: Diagramas de interacción entre componentes
- **Timeline**: Gantt charts para cronogramas

## Formato de Entrada

El archivo de entrada debe incluir:
- Descripción del proyecto
- Funcionalidades requeridas
- Requisitos técnicos (frontend, backend, base de datos, etc.)
- Restricciones (plazo, presupuesto, equipo)

## Formato de Salida

Los archivos generados en `output/` incluyen:
- Resumen del alcance
- Evaluación de complejidad técnica
- Estimación de horas/días por fase
- Timeline de implementación
- Dependencias y riesgos
- Mantenimiento (si aplica): costes anuales y recursos necesarios

## Mantenimiento a Largo Plazo

Para proyectos que requieren mantenimiento durante X años, el flujo completo es:

1. **Analista** → Genera análisis con fase de mantenimiento
2. **Mantenedor** → Genera `output/<nombre>_mantenimiento.md` con:
   - Deuda técnica y score de mantenibilidad
   - Operational costs (infraestructura, licencias, monitorización)
   - Evolutivos previstos por año
   - Recursos necesarios (FTE)
   - Roadmap de actualizaciones

**Activación**: Cuando los requisitos incluyan horizonte de mantenimiento ("mantener X años", "soporte durante...")

## Implementación de Contenidos

Para proyectos que incluyen contenidos (textos, fotos, videos, documentos):

1. **Analista** → Genera análisis con fase de contenidos
2. **Contenidos** → Genera `output/<nombre>_contenidos.md` con:
   - Volumen por tipo de contenido
   - Tiempo de procesamiento por unidad
   - Timeline de carga
   - Recursos necesarios

**Activación**: Cuando los requisitos incluyan "implementar contenidos", "cargar contenidos", "catálogo de obras", etc.

### Tiempos de Referencia
| Tipo | Tiempo por unidad |
|------|-------------------|
| Texto (1000 palabras) | 45 min |
| Imagen | 20 min |
| Video <5 min | 85 min |
| Audio <10 min | 45 min |
| Documento PDF | 40 min |

Aplicar factores: x1.5 revisiones, x0.7 por idioma adicional, x1.2 SEO/metadatos.

## Parametrización de Estimaciones

Las estimaciones del agente analista siguen un enfoque **conservador** para garantizar plazos realistas:

### Principio Fundamental
**Siempre estimar al alza**. Las estimaciones cubren el peor escenario posible.

### Reglas de Cálculo
- Factor de seguridad: 1.5x a 2x sobre estimación base
- Buffer de imprevistos: 20-30% adicional
- Testing: 40-50% del tiempo de desarrollo (no 20%)
- Despliegue: margen extra para infraestructura y CI/CD

### Buffers por Fase
| Fase | Buffer |
|------|--------|
| Análisis | +25% |
| Desarrollo | +50% |
| Testing | +50% |
| Documentación | +25% |
| Despliegue | +40% |
| Contenidos | +35% |
| Mantenimiento | +40% |

### Redondeo
Los valores se redondean **siempre hacia arriba** al entero superior (día u hora).
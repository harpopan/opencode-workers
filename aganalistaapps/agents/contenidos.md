# Agente Contenidos - Análisis de Implementación de Contenidos

## Propósito

Analizar y estimar el tiempo necesario para la implementación de contenidos en una aplicación, incluyendo carga, estructuración, migración y organización de materiales digitales.

## Entrada

- Requisitos donde se especifica implementación de contenidos
- Archivo de entrada describiendo tipos y volumen de contenidos
- Materiales proporcionados por el cliente (descripción o inventario)

## Detección de Necesidad

ACTIVAR este análisis cuando los requisitos incluyan:
- "Implementar contenidos", "cargar contenidos", "agregar contenidos"
- "Secciones con fotos/videos/imágenes"
- "Catálogo de obras/piezas/artículos"
- "Base de contenidos", "gestor de contenidos"
- "Migración de contenidos", "importar contenidos"
- Listados o inventarios de materiales a incluir

## Proceso de Análisis

### 1. Identificación de Tipos de Contenidos

Determinar categorías presentes:
- **Textuales**: descripciones, artículos, biografías, fichas técnicas
- **Visuales**: fotografías, ilustraciones, infografías, banners
- **Audiovisuales**: videos, documentales, clips, tutoriales
- **Audio**: podcasts, guías sonoras, narraciones
- **Documentos**: PDFs, fichas, catálogos, manuales
- **Interactivos**: elementos 3D, tours virtuales, audio 360°

### 2. Cuantificación

Solicitar al cliente volumen exacto:
| Tipo | Cantidad | Formato/Duración |
|------|---------|-----------|
| Textos (palabras) | X | - |
| Imágenes | X | jpg/png/webp |
| Videos | X | X min |
| Audios | X | X min |
| Documentos | X | PDF |

### 3. Evaluación de Complejidad

Factores que aumentan tiempo:
- Metaetiquetas SEO requeridas
- Multilingüe (X idiomas)
- Taxonomía/categorización compleja
- Relaciones entre contenidos (relacionados, sugerido)
- Contenidos interactivos o especiales
- Formateo especial (markdown, código)
- Agua terminada o incompleta

### 4. Estimación de Tiempo

**Tiempos base por unidad:**
| Tipo | Processing | Estructura | Carga CMS | QA | Total |
|------|-----------|-----------|-----------|-----|-------|
| Texto 1000 palabras | 15 min | 10 min | 10 min | 10 min | 45 min |
| Imagen (estándar) | 5 min | 5 min | 5 min | 5 min | 20 min |
| Imagen (alta resolución) | 10 min | 8 min | 8 min | 5 min | 31 min |
| Video <5 min | 25 min | 20 min | 25 min | 15 min | 85 min |
| Video >5 min | +15 min | +10 min | +15 min | +10 min | (+50 min) |
| Audio <10 min | 15 min | 10 min | 10 min | 10 min | 45 min |
| Documento PDF | 10 min | 10 min | 10 min | 10 min | 40 min |
| Elemento interactivo | 30 min | 25 min | 25 min | 20 min | 100 min |

**Aplicar factores:**
- Contenido en brouh: x1.5 (revisiones adicionales)
- Multilingüe: x0.7 por idioma adicional
- SEO/metadatos: x1.2
- Taxonomía compleja: x1.15
- Dependencia de terceros: x1.3

## Salida

Generar en `output/<nombre_archivo>_contenidos.md`:

### Resumen Ejecutivo
- Volumen total de contenidos
- Tiempo total estimado
- Distribución por tipo

### Desglose por Tipo
| Tipo | Cantidad | Tiempo Unitario | Tiempo Total |
|------|---------|-----------------|--------------|
| Textos | X | X min | Xh |
| Imágenes | X | X min | Xh |
| ... | ... | ... | ... |

### Timeline de Implementación
- Secuencia de carga
- Dependencias entre tipos
- Milestones

### Recursos Necesarios
- Acceso CMS y credenciales
- Materiales finales del cliente
- Revisiones requeridas

### Riesgos
- Contenidos incompletos
- Formatos no compatibles
- Retrasos en aprovación

## Directrices

- SIEMPRE solicitar volumen exacto al cliente antes de estimar
- Incluir buffer del 50% para revisiones y correcciones
- Considerar tiempo de revisión por parte del cliente
- Si hay idiomas, estimar primero idioma base luego aplicar factor
- Para contenidos de terceros (licenciados), añadir tiempo de gestión
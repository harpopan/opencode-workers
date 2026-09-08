---
version: 1.1
fecha: 2026-06-23
estado: ACTIVO
descripcion: Taxonomía de documentos, frontmatter YAML, estados y convenciones de documentación para proyectos de software (independiente de proyecto)
tipo: Referencia de documentación
---

# REF - TAXONOMIA DEVS.md — Taxonomía y Convenciones de Documentación

**Propósito**: Unificar criterios de documentación en proyectos de software. Copiar y adaptar por proyecto.

---

## Frontmatter YAML

Campos **obligatorios**: `version`, `fecha`, `estado`, `descripcion`
Campos **opcionales**: `tipo`, `autor`, `ultima_revision`

```yaml
---
version: 1.0
fecha: YYYY-MM-DD
estado: [ACTIVO|COMPLETADO|PROPUESTA|OBSOLETO]
descripcion: Breve descripción del contenido
---
```

## Estados de Documentos

| Estado | Significado |
|--------|-------------|
| **ACTIVO** | Vigente y actualizado |
| **COMPLETADO** | Plan/tarea finalizada |
| **PROPUESTA** | Propuesta en evaluación |
| **OBSOLETO** | Información desactualizada |

## Prefijos de Archivos

| Prefijo | Tipo | Uso |
|---------|------|-----|
| `GUIA-` | Guías | Normativas de trabajo (arquitectura, desarrollo) |
| `REF-` | Referencia | Documentación técnica de referencia |
| `SPEC-` | Especificación | Especificación técnica o funcional |
| `PROY-` | Proyecto | Documento troncal del proyecto (roadmap, plan) |
| `SAM-` | Samjoko | Notas o fragmentos del compañero Samjoko |
| `IDEA-` | Ideas | Banco de ideas, brainstorming |
| `LAB-` | Laboratorio | Exploración, pruebas, WIP |
| `NOTA-` | Apunte | Captura breve, nota rápida |
| `PEND-` | Pendiente | Tarea o decisión pendiente |
| `LOG-` | Bitácora | Historial de trabajo, transcripción |
| `PROMPT-` | Prompts | Prompt para IA |
| `ANEXO-` | Anexo | Detalle complementario de otro documento |
| `DOC-` | General | Cuando no aplica otro prefijo |
| `TAREA-` | Tareas | Lista de tareas, backlog |
| `TIP-` | Consejo | Tip, truco o consejo breve |
| `CHK-` | Checklist | Lista de verificación |
| `META-` | Sistema | Documentos del propio sistema/normas |
| `MAP-` | Mapa | Índice, mapa de documentación |
| `PLANT-` | Plantilla | Template reutilizable |
| `FRAG-` | Fragmento | Fragmento breve reutilizable |
| `LEGAL-` | Legal | Licencias, avisos legales |
| `ART-` | Artículo | Pieza de reflexión o artículo |

## Ciclo de Vida

Los documentos `LOG` y los de estado `COMPLETADO`/`OBSOLETO` se archivan en un directorio `historico/`. La raíz de `docs/` solo contiene documentos `ACTIVO` o `PROPUESTA`.

## Glosario de Iconos

| Icono | Significado |
|-------|-------------|
| ✅ | Completado |
| 🔄 | En progreso |
| ⏳ | Pendiente |
| ⚠️ | Advertencia/Limitación |
| 🔴 | Prioridad crítica |
| 🟡 | Prioridad alta |
| 🟢 | Prioridad media |
| 🔵 | Prioridad baja |

---

**Versión**: 1.0
**Fecha**: 2026-06-23
**Proyecto**: (independiente, reutilizable entre proyectos)

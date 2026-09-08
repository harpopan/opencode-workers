---
version: 1.0.0
fecha: YYYY-MM-DD
estado: INMUTABLE
descripcion: Reglas base del sistema y punto de entrada para subagentes y documentación
---

# AGENTS.md — (Reglas Base + Subagentes)

Documento maestro de reglas base de comportamiento e instrucciones del sistema. **Leer primero**.

> 📍 **Mapa de Documentación**: Toda la estructura, referencias, guías e índice de archivos del proyecto se encuentran en el archivo maestro **`docs/MAP - DOCUMENTACION.md`**. Consultar dicho mapa siempre que se necesite ubicar o navegar la documentación.

---

## REGLAS GLOBALES

### 1. Documentación y Estructura

- **Documento Maestro**: Para explorar, consultar o actualizar el estado de la documentación, referirse siempre a `docs/MAP - DOCUMENTACION.md`.
- **Cabecera YAML (frontmatter)**: Obligatoria en todo documento `.md` nuevo dentro de `docs/`.
- **Taxonomía**: Respetar los prefijos de documentación estandarizados (p. ej., `MAP -`, `REF -`, `PROY -`, `SPEC -`, `GUIA -`, `LOG -`).
- **Histórico**: Archivar en `docs/historico/` todo documento obsoleto o de registro completado, y actualizar su referencia en el mapa de documentación.

### 2. Normas de Código

- **Identificadores en Castellano**: Usar nombres descriptivos en castellano para la lógica de negocio, funciones, clases, métodos, variables y tipos de dominio.
- **Términos Genéricos**: Reservar el inglés únicamente para conceptos de infraestructura, patrones de diseño o librerías externas (`config`, `state`, `adapter`, `props`, `controller`, etc.).
- **Nomenclatura de Archivos**: Nombrar archivos y carpetas en `kebab-case`.

### 3. Calidad y Estilo

- El código debe cumplir estrictamente con los linters y formateadores configurados (`npm run lint && npm run format:check`).
- **JSDoc Obligatorio**: Incluir documentación JSDoc (`@param`, `@returns`) en todas las funciones y métodos públicos de servicios, módulos y componentes.

---

## 🎯 SUBAGENTES Y SKILLS

La lista completa de subagentes activos y sus capacidades técnicas asociadas se encuentra indexada en `docs/MAP - DOCUMENTACION.md`.

- Cada habilidad técnica se ubica en su directorio correspondiente: `.opencode/skills/<identificador-habilidad>/SKILL.md`.
- La invocación o carga de habilidades se realiza bajo demanda mediante `skill('<identificador-habilidad>')`.

---

## 🔄 RITUAL DE CIERRE DE TRABAJO

Al finalizar una tarea o bloque de trabajo:

1. **Documentación**: Marcar avances en `docs/PROY - ROADMAP.md` y refrescar el mapa en `docs/MAP - DOCUMENTACION.md` si se han creado o movido archivos.
2. **Registro de Cambios**: Añadir una entrada concisa (1-4 líneas) en el changelog correspondiente.
3. **Versionado**: Incrementar la versión según la envergadura de los cambios (parche, menor, mayor).
4. **Git**: Inspeccionar los cambios realizados (`git status` / `git diff`) y **solicitar confirmación explícita al usuario** antes de realizar cualquier commit.
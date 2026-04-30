# Análisis de Requisitos: Sistema de Gestión de Tareas (TaskFlow)

## Resumen Ejecutivo

| Aspecto | Detalle |
|---------|---------|
| **Tipo de aplicación** | Web (SPA) |
| **Usuarios objetivo** | Profesionales y equipos que necesitan gestionar tareas personales y laborales |
| **Complejidad general** | Media-Alta |
| **Timeline estimado** | 8-10 semanas (56-70 días hábiles) |
| **Equipo requerido** | 2 backend + 1 frontend |
| **Riesgo de cumplimiento de plazo** | Medio (colaboración v2 podría comprometer fechas) |

---

## 1. Alcance del Proyecto

### Funcionalidades Core (v1)

| Categoría | Funcionalidades |
|-----------|----------------|
| **Autenticación** | Registro, login, recuperación de contraseña, remember me |
| **Gestión de Tareas** | CRUD completo, filtros, ordenamiento, categorización |
| **Notificaciones** | Recordatorios por email, notificaciones in-app |

### Funcionalidades Postergadas (v2)

| Categoría | Funcionalidades |
|-----------|----------------|
| **Colaboración** | Compartir tareas, asignar a miembros, comentarios |

> **Nota**: Las funcionalidades de colaboración se marcan como v2 para proteger el plazo de 3 meses.

---

## 2. Evaluación de Complejidad Técnica

### Por Área

| Componente | Complejidad | Justificación |
|------------|-------------|---------------|
| **Frontend** | Media | React + TypeScript es stack conocido; requiere estado complejo para filtros/ordenamiento |
| **Backend** | Media | API REST bien definida; Express es ligero |
| **Base de datos** | Media | PostgreSQL requiere modelado adecuado para relaciones tarea-categoría |
| **Autenticación** | Media | JWT + email recovery + reset password |
| **Notificaciones** | Media-Alta | Integración con servicio SMTP, trabajo en background |
| **DevOps** | Media | Docker, configuración de servidor Linux |

### Entidades y Relaciones

```
Usuario (1) ──< Tarea (N)
Tarea (N) ──< Categoria/Tags (N)
Tarea (N) ──> Notificacion (N)
```

- **3 entidades principales**: Usuario, Tarea, Categoría
- **1 entidad secundaria**: Notificación
- **Relaciones**: Moderado complejidad (muchos a muchos con tags)

---

## 3. Desglose de Funcionalidades y Estimación de Horas

### 3.1 Autenticación

| Funcionalidad | Análisis | Desarrollo | Testing | Docs | Despliegue | **Total** |
|---------------|----------|------------|---------|------|------------|-----------|
| Registro de usuarios | 2h | 4h | 4h | 1h | 1h | **12h** |
| Inicio de sesión | 2h | 4h | 4h | 1h | 1h | **12h** |
| Recuperación de contraseña | 2h | 6h | 5h | 1h | 1h | **15h** |
| Sesión persistente (remember me) | 1h | 3h | 3h | 1h | 1h | **9h** |
| **Subtotal** | **7h** | **17h** | **16h** | **4h** | **4h** | **48h** |

### 3.2 Gestión de Tareas

| Funcionalidad | Análisis | Desarrollo | Testing | Docs | Despliegue | **Total** |
|---------------|----------|------------|---------|------|------------|-----------|
| Crear tarea (título, descripción, fecha límite) | 2h | 6h | 6h | 1h | 1h | **16h** |
| Editar tarea | 1h | 3h | 4h | 1h | 0h | **9h** |
| Eliminar tarea | 1h | 2h | 3h | 1h | 0h | **7h** |
| Marcar como completada | 1h | 2h | 3h | 0h | 0h | **6h** |
| Filtrar (todas/pendientes/completadas) | 2h | 8h | 6h | 1h | 1h | **18h** |
| Ordenar (fecha creación/límite) | 1h | 4h | 4h | 0h | 0h | **9h** |
| Categorías/Tags | 3h | 10h | 8h | 2h | 1h | **24h** |
| **Subtotal** | **11h** | **35h** | **34h** | **6h** | **3h** | **89h** |

### 3.3 Notificaciones

| Funcionalidad | Análisis | Desarrollo | Testing | Docs | Despliegue | **Total** |
|---------------|----------|------------|---------|------|------------|-----------|
| Recordatorios por email | 4h | 12h | 8h | 2h | 2h | **28h** |
| Notificaciones in-app | 3h | 8h | 6h | 2h | 1h | **20h** |
| **Subtotal** | **7h** | **20h** | **14h** | **4h** | **3h** | **48h** |

### 3.4 Requisitos Transversales

| Funcionalidad | Análisis | Desarrollo | Testing | Docs | Despliegue | **Total** |
|---------------|----------|------------|---------|------|------------|-----------|
| Diseño responsive | 2h | 10h | 6h | 1h | 1h | **20h** |
| Accesibilidad WCAG AA | 4h | 8h | 8h | 2h | 1h | **23h** |
| Performance (<3s carga) | 2h | 6h | 4h | 1h | 2h | **15h** |
| **Subtotal** | **8h** | **24h** | **18h** | **4h** | **4h** | **58h** |

---

## 4. Resumen de Estimación Total

| Fase | Horas |
|------|-------|
| Análisis y Planificación | 33h |
| Desarrollo | 96h |
| Testing | 82h |
| Documentación | 18h |
| Despliegue | 14h |
| **TOTAL** | **243h** |

### Distribución por Rol

| Rol | Horas |
|-----|-------|
| Backend (2 devs) | ~120h (80h dev + 40h soporte testing/docs) |
| Frontend (1 dev) | ~90h (dev + testing frontend) |
| DevOps (compartido) | ~33h |

### Conversión a Días (8h/día)

| Métrica | Valor |
|---------|-------|
| Total horas | 243h |
| Días laborales | ~30 días (6 semanas) |
| Con buffer 20% | ~37 días (8 semanas) |

---

## 5. Timeline Sugerido

### Fase 1: Foundation (Semanas 1-2)

```
□ Semana 1: Setup infraestructura
  - Configurar repositorio, Docker, PostgreSQL
  - Diseñar modelo de datos
  - Implementar autenticación básica (registro/login)
  
□ Semana 2: Auth completa
  - JWT, remember me
  - Recuperación de contraseña por email
```

### Fase 2: Core Features (Semanas 3-4)

```
□ Semana 3: CRUD de tareas
  - API REST de tareas
  - Frontend: crear/editar/eliminar/completar
  
□ Semana 4: Filtros y categorización
  - Filtros y ordenamiento en frontend
  - Sistema de tags/categorías
```

### Fase 5: Notificaciones (Semana 5)

```
□ Semana 5: Sistema de notificaciones
  - Integración SMTP para emails
  - Recordatorios programados (cron jobs)
  - Notificaciones in-app
```

### Fase 6: Calidad y Polish (Semanas 6-7)

```
□ Semana 6: Testing y accesibilidad
  - Pruebas de integración completas
  - Validación WCAG AA
  - Optimizaciones de performance
  
□ Semana 7: Responsive y polish
  - Testing en dispositivos móviles
  - Ajustes UI/UX
```

### Fase 7: Despliegue (Semana 8)

```
□ Semana 8: Deployment
  - Configurar servidor Linux con Docker
  - Despliegue a producción
  - Documentación final
```

---

## 6. Dependencias entre Funcionalidades

| Depende de | Funcionalidad | Tipo |
|------------|---------------|------|
| Setup infrastructure | Autenticación | Hard |
| Autenticación | Gestión de tareas | Hard |
| Gestión de tareas | Notificaciones | Soft |
| Gestión de tareas | Filtros y categorización | Soft |

> **Nota**: Las tareas solo pueden desarrollarse después de que el sistema de autenticación esté operativo.

---

## 7. Riesgos Potenciales

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Integración SMTP falla o retrasa | Media | Medio | Usar servicios third-party (SendGrid, SES) como fallback |
| Equipo no familiarizado con TypeScript | Baja | Alto | Capacitación previa; fase inicial más lenta |
| Scope creep por colaboración | Alta | Alto | Mantener v2 fuera del scope inicial |
| Performance no alcanza <3s | Media | Medio | Lazy loading, code splitting, CDN |
| Accesibilidad WCAG AA más compleja de lo esperado | Media | Medio | Auditorías tempranas con Lighthouse/aXe |

---

## 8. Supuestos Realizados

1. **Email service**: Se asume disponibilidad de servidor SMTP o servicio como SendGrid
2. **Hosting**: Acceso a servidor Linux con Docker preinstalado o capacidad de instalarlo
3. **Experiencia del equipo**: Conocimiento medio-alto en React, Node.js, PostgreSQL
4. **Scope**: Funcionalidades v2 (colaboración) no se incluyen en la estimación
5. **BDD tests**: No se incluyen; solo unit tests e integración
6. **UX Design**: Se asume disponibilidad de mockups/wireframes

---

## 9. Ambigüedades Identificadas

| Aspecto | Ambigüedad | Recomendación |
|---------|------------|---------------|
| Recuperación de contraseña | ¿Email transaccional simple o flujo completo con tokens? | Clarificar con stakeholders |
| Notificaciones in-app | ¿Polling, WebSockets, o push notifications? | Definir arquitectura de realtime |
| Categorías | ¿Precargadas o editables por usuario? | Decidir si hay categorías globales o por usuario |
| Límite de tareas | ¿Hay límite por usuario? | Definir políticas de uso |

---

## 10. Opciones de Arquitectura Alternativas

### Opción A: Monolito Moderno (Recomendada para presupuesto limitado)

- **Stack**: Next.js (full-stack) + PostgreSQL
- **Pros**: Menor complejidad DevOps, desarrollo más rápido
- **Cons**: Menos escalable a futuro

### Opción B: Separación estricta (Recomendada para escalabilidad)

- **Stack**: React SPA + Node.js API + PostgreSQL
- **Pros**: Mejor separación de concerns, más escalable
- **Cons**: Mayor complejidad de desarrollo y deployment

> **Recomendación**: Para un equipo de 3 personas con plazo de 3 meses y presupuesto limitado, la **Opción A** es más práctica.

---

## Conclusión

El proyecto TaskFlow es viable dentro del plazo de 3 meses con el equipo de 3 personas, siempre que:
- Las funcionalidades de colaboración (v2) se excluyan del scope inicial
- Se mantenga disciplina de scope durante el desarrollo
- Se allocate buffer de tiempo para requisitos transversales (accesibilidad, performance)

La estimación de **243 horas** (8 semanas con buffer) está alineada con las restricciones del proyecto.

---

*Documento generado: $(Get-Date -Format "yyyy-MM-dd")*  
*Agente Analista v1.0*
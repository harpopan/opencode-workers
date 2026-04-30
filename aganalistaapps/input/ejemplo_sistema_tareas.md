# Requisitos: Sistema de Gestión de Tareas (TaskFlow)

## Descripción del Proyecto

Desarrollar una aplicación web para gestión de tareas personales y profesionales que permita a los usuarios organizar su trabajo diario.

## Funcionalidades Requeridas

### Autenticación
- Registro de usuarios con email y contraseña
- Inicio de sesión
- Recuperación de contraseña por email
- Sesión persistente (remember me)

### Gestión de Tareas
- Crear tareas con título, descripción y fecha límite
- Editar y eliminar tareas
- Marcar tareas como completadas
- Filtrar tareas por: todas, pendientes, completadas
- Ordenar por fecha de creación o fecha límite
- Categorías/tags para organizar tareas

### Colaboración (v2)
- Compartir tareas con otros usuarios
- Asignar tareas a miembros del equipo
- Comentarios en tareas

### Notificaciones
- Recordatorios por email antes de fecha límite
- Notificaciones in-app de tareas próximas

## Requisitos Técnicos

- Frontend: React con TypeScript
- Backend: Node.js con Express
- Base de datos: PostgreSQL
- Autenticación: JWT
- Despliegue: Docker en servidor Linux

## Restricciones

- Plazo máximo: 3 meses
- Presupuesto: limitado
- Equipo: 2 desarrolladores backend, 1 frontend

## Consideraciones Adicionales

- Debe ser responsive (funcionar en móvil)
- Accesibilidad: cumplir WCAG nivel AA
- Performance: tiempo de carga < 3 segundos
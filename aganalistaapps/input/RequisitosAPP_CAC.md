# Requerimientos Técnicos — Aplicación Móvil Multiplataforma para la Ciutat de les Arts i les Ciències

## 1. Objeto del Proyecto
Diseño, desarrollo, implantación, puesta en marcha y mantenimiento (4 años) de una **aplicación móvil interactiva multiplataforma (iOS y Android)** destinada a mejorar la experiencia del visitante mediante tecnologías de:
- Geolocalización
- Realidad aumentada
- Inteligencia artificial
- Sistemas interactivos
- Otros sistemas adecuados a la actividad del complejo

Incluye también una **versión app web** (si procede).

---

## 2. Antecedentes y Contexto
La empresa pública CACSA tiene como funciones principales:
1. Gestión de actividades necesarias para la preparación, construcción y puesta en funcionamiento de proyectos de la Generalitat Valenciana relacionados con la Ciudad de las Artes y las Ciencias.
2. Gestión de la explotación de actividades y servicios en los inmuebles e instalaciones del complejo.
3. Actividades adicionales: venta de entradas, organización de eventos propios o de terceros, consultoría y asistencia técnica en proyectos similares.

La aplicación móvil se considera una **herramienta estratégica** para mejorar la experiencia del visitante.

---

# 4. Requisitos Técnicos y Funcionales

## 4.1. Desarrollo Multiplataforma
- Compatibilidad con versiones actuales y al menos dos anteriores de iOS y Android.
- Publicación en App Store y Google Play.
- Actualizaciones periódicas.
- Cumplimiento de políticas oficiales de ambas plataformas.
- Posible coexistencia de **app nativa** y **app web**.

---

## 4.2. Multiidioma
- Idiomas mínimos: español, valenciano, inglés.
- Arquitectura preparada para añadir nuevos idiomas.
- Traducciones gestionables desde panel administrativo.
- Detección automática del idioma del dispositivo.

---

## 4.3. Accesibilidad
Cumplimiento de:
- WCAG 2.1 nivel AA.
- Compatibilidad con lectores de pantalla (VoiceOver, TalkBack).
- Contrastes adecuados.
- Subtitulación en audioguías.
- Tamaño de fuente ajustable.

---

## 4.4. Parametrización por Perfil del Visitante
- Registro opcional de usuario.
- Adaptación de contenidos según edad, idioma, intereses o historial.
- Personalización de itinerarios y notificaciones.
- Gestión desde panel administrativo.

---

## 4.5. Notificaciones Push Interactivas (Bluetooth + Geolocalización)
- Notificaciones push en tiempo real.
- Integración con beacons Bluetooth.
  - La empresa adjudicataria suministra, instala, configura y pone en producción los elementos del sistema.
  - Integración con la red de datos existente en CAC.
- Activación por proximidad física.
- Interacción directa desde la notificación.
- Cumplimiento RGPD.

---

## 4.6. Geolocalización (Mapa tipo Google Maps interno)
- Posicionamiento GPS en tiempo real.
- Notificaciones por proximidad.
- Visualización del usuario en mapa interactivo.
- Cálculo de tiempo hasta destino.
- Registro anónimo de recorridos para análisis estadístico.

---

## 4.7. Realidad Aumentada (AR) y Experiencias 360°
- Superposición de elementos digitales sobre el entorno real.
- Posibilidad de capturar fotos y compartir en redes sociales.
- Integración con ARKit (iOS) y ARCore (Android).
- Experiencias inmersivas 360°.
- Activación contextual por ubicación o marcador visual.
- (Opcional) Extensión hacia experiencias tipo metaverso.

---

## 4.9. Audioguía
- Reproducción automática por proximidad.
- Descarga previa para uso offline.
- Control de velocidad.
- Subtítulos y transcripción textual.

---

## 4.10. Propuesta de Recorridos según Perfil y Aforo
- Integración con sistema de control de aforo.
- Algoritmo de redistribución de visitantes.
- Sugerencias alternativas en tiempo real.
- Mapa de calor.
- Panel estadístico para gestores.

---

## 4.11. Plano Interactivo
- Mapa dinámico con zoom.
- Puntos de interés clicables.
- Indicaciones paso a paso.
- Actualizable desde backend.

---

## 4.12. Chatbot con Inteligencia Artificial
- Integración con modelo conversacional.
- Respuestas contextualizadas.
- Soporte multilingüe.
- Aprendizaje supervisado.
- Registro de consultas para análisis.

---

## 4.13. Gamificación
- Sistema de retos y recompensas.
- Insignias digitales.
- Ranking opcional.
- Incentivo para completar recorridos.

---

## 4.14. Valoración de la Experiencia
- Espacio para que el visitante valore la experiencia.
- Puntuación de exposiciones, proyecciones o actividades.

---

## 4.15. Modo “Ciutat de les Arts i les Ciències en Casa”
- Acceso a recursos tras la visita.
- Envío de notificaciones sobre próximos eventos.
- Generación automática de un recuerdo de la visita para compartir.

---

# 6. Mantenimiento (4 Años)
Incluye:
- Corrección de errores.
- Actualización ante cambios de iOS y Android.
- Soporte técnico.
- Evolución funcional menor.
- SLA: respuesta < 48h.

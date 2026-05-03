# Configuración de OpenCode con LM Studio

Este documento contiene la guía necesaria para conectar OpenCode con modelos de inteligencia artificial ejecutándose localmente a través de LM Studio.

## 🚀 Requisitos Previos

1. Tener instalada la aplicación **LM Studio** en tu ordenador.
2. Haber descargado el modelo **Qwen3.5 9B** (o cualquier otro modelo que vayas a usar) dentro de LM Studio.
3. Tener OpenCode instalado y funcionando.

---

## 🛠️ Paso 1: Configurar el Servidor en LM Studio

1. Abre LM Studio.
2. Carga tu modelo (ej. `qwen/qwen3.5-9b`).
3. Ve a la pestaña **Local Server** (icono de la doble flecha `↔`).
4. Haz clic en **Start Server**.
5. Asegúrate de que el servidor esté expuesto en la dirección IP correcta de tu red local. En este caso, el servidor se ha configurado en la IP `192.168.0.23` en el puerto `1234`.

*(Nota: Puedes verificar que el servidor funciona correctamente abriendo la ruta `http://192.168.0.23:1234/v1/models` en tu navegador, lo cual devolverá un JSON con la lista de modelos activos).*

---

## 📁 Paso 2: Configurar `opencode.json`

OpenCode utiliza un sistema de proveedores compatible con el SDK de IA. Como LM Studio expone una API compatible con OpenAI, usamos la configuración `@ai-sdk/openai-compatible`.

El archivo `opencode.json` que está en este repositorio se configura de la siguiente manera:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://192.168.0.23:1234/v1",
        "apiKey": "lm-studio"
      },
      "models": {
        "qwen/qwen3.5-9b": {
          "name": "Qwen3.5 9B (local)"
        }
      }
    }
  },
  "model": "lmstudio/qwen/qwen3.5-9b"
}
```

### Detalles de la configuración:
- `baseURL`: Apunta a la dirección donde tu LM Studio está sirviendo la API (en este caso, la IP local).
- `apiKey`: Se envía un valor falso ("lm-studio") porque algunos clientes de OpenAI exigen que el campo no esté vacío, aunque el servidor local lo ignore.
- `models`: Aquí se detalla el ID exacto del modelo que reporta LM Studio (ej. `qwen/qwen3.5-9b`).

### 💡 ¿Por qué el nombre del modelo lleva "lmstudio/" al principio?
En la configuración `"model": "lmstudio/qwen/qwen3.5-9b"`, OpenCode utiliza un formato **`proveedor/modelo`**.
- **`lmstudio/`**: Le indica a OpenCode qué bloque de proveedor debe utilizar (el que hemos definido en el JSON como `"lmstudio": { ... }`), el cual contiene nuestra IP local.
- **`qwen/qwen3.5-9b`**: Le indica a ese proveedor qué modelo en específico debe ejecutar.
Si omitiéramos "lmstudio/", OpenCode intentaría buscar el modelo en un proveedor por defecto y la conexión fallaría.

---

## 💻 Paso 3: Uso y Ejecución

Una vez que LM Studio está ejecutando el modelo y sirviendo en red local, OpenCode al iniciarse en esta misma carpeta leerá el archivo `opencode.json` y mandará todos los *prompts* y tareas directamente a tu entorno de ejecución local, permitiendo utilizar el asistente con un modelo auto-hospedado y 100% privado.

---

## 📊 Monitoreo de Consumo y Contexto

Si quieres saber cuánto contexto has gastado durante tu sesión con el modelo local, debes tener en cuenta lo siguiente:

### 1. En la API (Por cada petición individual)
Cada vez que OpenCode hace una petición a la API local, LM Studio adjunta en su respuesta un objeto `usage` (invisible para el usuario normal, pero que OpenCode sí procesa) que indica:
- **Prompt Tokens:** Los tokens de tu historial y el mensaje enviado.
- **Completion Tokens:** Los tokens generados por la respuesta.
- **Total Tokens:** La suma de ambos.

La URL de la API (`http://192.168.0.23:1234/v1`) **no** expone un endpoint o "dashboard" público que acumule y te muestre todo el historial. Es una API sin estado, por lo que la cuenta la lleva siempre la aplicación cliente.

### 2. En la Interfaz Gráfica (Recomendado)
Para visualizar en tiempo real el consumo de contexto, la forma más sencilla es usar la propia interfaz de LM Studio:
1. Ve a la pestaña **Local Server** donde arrancaste el servidor.
2. Observa la consola de **Server Logs** (normalmente abajo o a la derecha).
3. Por cada petición que OpenCode envíe, verás líneas de log indicando cuántos tokens se procesaron, la velocidad (`tok/sec`) y lo más importante: **Context limit (ej. 1200 / 8192)**. 
Ese indicador te mostrará exactamente qué porcentaje de la memoria máxima del modelo estás ocupando actualmente en tu conversación.

---

## 🧠 Optimización de Contexto para Modelos Locales

A diferencia de los modelos en la nube (como Gemini 1.5 Pro o GPT-4), los modelos locales suelen tener una ventana de contexto más pequeña (ej. 8k, 16k o 32k tokens). Para evitar errores de "Context Overflow" o pérdida de coherencia, sigue estas estrategias:

### 1. Fragmentación de Tareas (Atomicidad)
No pidas cambios masivos en una sola instrucción. Divide tu petición en pasos pequeños:
*   **Mal:** "Crea toda la lógica de autenticación, base de datos y UI."
*   **Bien:** "Crea la interfaz del formulario de login", luego "Crea la función de validación de campos", etc.

### 2. Uso del Planning Mode
OpenCode entrará en modo planificación para tareas complejas. Esto ayuda al modelo local a "pensar" antes de actuar, generando un archivo `task.md`. Validar este plan ayuda a que el modelo no se pierda durante la ejecución.

### 3. Reinicio de Sesión (Session Flush)
Si notas que el modelo empieza a responder de forma lenta o incoherente, es probable que el contexto esté saturado.
*   **Estrategia:** Guarda tus cambios, haz un resumen de lo avanzado y **abre una nueva sesión de chat**. Al estar los archivos actualizados en el disco, el modelo podrá retomar el hilo leyendo la nueva versión del código sin cargar con todo el historial previo.

### 4. Configuración de Contexto en LM Studio
En la pestaña de configuración del modelo en LM Studio (Panel derecho -> Context Length), asegúrate de tener asignado un valor equilibrado (ej. 2048 o 4096 para Qwen 9B) según tu memoria VRAM. Si el modelo soporta más y tu GPU lo permite, puedes subirlo, pero recuerda que a mayor contexto, mayor será el consumo de memoria y menor la velocidad.

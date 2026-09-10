# Configurador OpenCode + LMStudio

Dos scripts que configuran **OpenCode** para usar **LMStudio** de forma automática:

| Script | Sistema operativo |
| --- | --- |
| `configurar-opencode.sh` | Linux / macOS |
| `wconfigurar-opencode.ps1` | Windows (PowerShell) |

Ambos hacen lo mismo: detectan los modelos disponibles en una instancia de
LMStudio y generan (o actualizan) el archivo `opencode.jsonc`, dejando OpenCode
listo para chatear con los modelos locales.

---

## ¿Qué hacen exactamente?

1. **Se conectan a LMStudio** y consultan la lista de modelos de chat disponibles
   (excluyen los modelos de *embedding*).
2. **Detectan el contexto y el límite de tokens** de cada modelo a partir de la
   API nativa de LMStudio (si está disponible; si no, usan valores por defecto).
3. **Generan `opencode.jsonc`** con un `provider` apuntando a la máquina
   seleccionada y con todos los modelos detectados.
4. **Guardan una copia de seguridad** del `opencode.jsonc` anterior en
   `opencode.jsonc.bak` antes de sobrescribirlo.

Al terminar, el primer modelo de la lista queda como **modelo por defecto**.
Puedes cambiar de modelo desde OpenCode con el comando `/models`.

---

## Requisitos

### `configurar-opencode.sh` (Linux / macOS)

- `curl`
- `python3`

### `wconfigurar-opencode.ps1` (Windows)

- PowerShell 5.1 o superior (incluido por defecto en Windows)

Y, en todos los casos:

- Una instancia de **LMStudio** corriendo y accesible desde tu máquina.

---

## Uso básico

### Linux / macOS

```bash
./configurar-opencode.sh
```

### Windows (PowerShell)

```powershell
.\wconfigurar-opencode.ps1
```

Al ejecutarlo sin opciones, si hay varios proveedores configurados te mostrará
un menú para elegir a qué máquina conectarte:

```
1. ¿A qué máquina de desarrollo quieres conectarte?

   1) Local  (http://localhost:1234)
   2) ScacNet  (http://scacnet.cacsa.eu:1234)

Elige un número [1-2]:
```

---

## Opciones

Ambos scripts comparten las mismas opciones:

| Opción | PowerShell | Descripción |
| --- | --- | --- |
| `-p, --provider <N\|nombre>` | `-p, -Proveedor` | Elige el proveedor por índice o nombre, saltándose el menú |
| `-u, --url <URL>` | `-u, -Url` | Usa una URL directa, ignorando la lista de proveedores |
| `-l, --list` | `-l, -Listar` | Muestra los proveedores configurados y sale |
| `-h, --help` | `-h, -Ayuda` | Muestra la ayuda |

### Ejemplos

```bash
# Linux / macOS
./configurar-opencode.sh -l                    # lista proveedores
./configurar-opencode.sh -p 2                  # elige el proveedor 2
./configurar-opencode.sh -p ScacNet            # elige por nombre
./configurar-opencode.sh -u http://192.168.1.60:1234   # URL directa
```

```powershell
# Windows (PowerShell)
.\wconfigurar-opencode.ps1 -Listar
.\wconfigurar-opencode.ps1 -Proveedor 2
.\wconfigurar-opencode.ps1 -Proveedor ScacNet
.\wconfigurar-opencode.ps1 -Url http://192.168.1.60:1234
```

---

## Configurar los proveedores

Un "proveedor" es cada máquina de desarrollo donde corre LMStudio. Se definen
como pares `Nombre|URL` en una lista al inicio de cada script:

```bash
# configurar-opencode.sh
PROVIDERS=(
    "Local|http://localhost:1234"
    "ScacNet|http://scacnet.cacsa.eu:1234"
    # "Portatil|http://192.168.1.60:1234"
)
```

```powershell
# wconfigurar-opencode.ps1
$Proveedores = @(
    "Local|http://localhost:1234"
    "ScacNet|http://scacnet.cacsa.eu:1234"
    # "Portatil|http://192.168.1.60:1234"
)
```

### Añadir proveedores sin tocar el script

También puedes mantener una lista adicional en el archivo
`~/.config/opencode/providers.conf`, con una línea `Nombre|URL` por proveedor.
Si existe, sus entradas se añaden automáticamente a las del script:

```
Oficina|http://192.168.1.20:1234
Casa|http://192.168.1.10:1234
```

> Las líneas vacías y las que empiezan por `#` se ignoran.

---

## Prioridad al elegir la máquina

El script decide a qué URL conectarse siguiendo este orden:

1. La variable de entorno `LMSTUDIO_URL` (si está definida).
2. La opción `-u` / `-Url`.
3. Si solo hay un proveedor configurado, se usa ese sin preguntar.
4. La opción `-p` / `-Proveedor` (por índice o nombre).
5. El menú interactivo.

---

## Qué genera

El script escribe un archivo `opencode.jsonc` con este aspecto:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (Local)",
      "options": {
        "baseURL": "http://localhost:1234/v1"
      },
      "models": {
        "modelo/ejemplo": {
          "name": "ejemplo",
          "limit": {
            "context": 32768,
            "output": 8192
          }
        }
      }
    }
  },
  "model": "local/modelo/ejemplo"
}
```

La clave del proveedor (`local`, `scacnet`, etc.) se genera automáticamente a
partir del nombre de la máquina (en minúsculas y sin espacios ni símbolos).

---

## Solución de problemas

- **"No se pudo conectar a LMStudio"**: comprueba que LMStudio está abierto y
  que su servidor local está activo, y que la URL del proveedor es correcta.
- **"No se encontraron modelos de chat"**: asegúrate de tener al menos un modelo
  de chat cargado en LMStudio (los modelos de *embedding* se ignoran).
- **Mensaje de valores por defecto**: es normal si la versión de LMStudio no
  expone la API nativa; se usan `context: 32768` y `output: 8192`.

# Trask 🚀

Herramienta de línea de comandos (CLI) para la gestión rápida de tareas, diseñada para ser simple y eficiente.

## 🛠 Instalación

Para instalar `trask` de forma global en tu sistema, clona el repositorio y ejecuta:

```bash
pipx install .
```

Si prefieres instalarlo en modo desarrollo (para que los cambios en el código se apliquen instantáneamente):

```bash
pipx install -e .
```

Asegúrate de que el directorio de scripts de Python esté en tu `PATH`. Una vez instalado, puedes usar el comando `trask` desde cualquier lugar.

## 📋 Funcionalidades

`trask` permite gestionar tareas con diferentes estados y ofrece soporte para tareas repetitivas.

### Comandos disponibles

| Comando                 | Descripción                                                                                                                                  |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `trask add <desc>`      | Añade una nueva tarea pendiente.                                                                                                             |
| `trask r <desc>`        | Crea una**tarea repetible**. Estas tareas no se borran al limpiar; vuelven a estado `pending` si se marcaron como `done` en días anteriores. |
| `trask s [all]`         | Muestra el resumen de tareas. Por defecto oculta las tareas en `done` o `hold`. Usa `all` para ver todo.                                     |
| `trask u <id> <estado>` | Actualiza el estado de una tarea por su ID.                                                                                                  |
| `trask d <id>`          | Elimina una tarea permanentemente por su ID.                                                                                                 |
| `trask clean`           | Limpia las tareas completadas (`done`) de días anteriores.                                                                                   |

### Estados de las tareas

Puedes actualizar una tarea a cualquiera de los siguientes estados:

- `pending` (por defecto)
- `started`
- `paused`
- `hold`
- `pr`
- `pre`
- `done`

## 💡 Ejemplos de uso

**Añadir una tarea nueva:**

```bash
trask add "Completar informe de ventas"
```

**Crear una tarea diaria (repetible):**

```bash
trask r "Revisar correo"
```

**Actualizar el estado de una tarea:**

```bash
trask u 5 started
```

**Ver todas las tareas incluyendo las pausadas y terminadas:**

```bash
trask s all
```

**Limpiar el tablero de tareas antiguas:**

```bash
trask clean
```

---

_Nota: Los datos se almacenan localmente en `tasks.json`._

# MFQ All 6 · App para móvil y ordenador

Calculadora de **Física, Química y Matemáticas** con interfaz gráfica moderna
(Material 3, modo claro/oscuro), hecha en Python con [Flet](https://flet.dev).
Es la evolución de `MFQ_all v5.py` (versión de consola).

## Qué incluye

| Sección | Contenido |
|---|---|
| **FyQ** | 29 fórmulas en 9 categorías (cinemática, tiro parabólico, dinámica, energía, gravitación, fluidos, electricidad, ondas, química). En cada una eliges **qué variable despejar** y la app pide solo los datos necesarios. Buscador sin tildes ni mayúsculas. |
| **Conversor** | Longitud, masa, volumen, tiempo, velocidad, presión, energía y temperatura. |
| **Mates** | Ecuación de 2º grado (con raíces complejas, vértice y gráfica), representar hasta 3 funciones, MCD/MCM/factores primos, texto↔binario y cambio de base, círculo, π con hasta 5000 decimales, dados. |
| **Historial** | Se guarda en el dispositivo. Mantén pulsado un resultado para copiarlo. |

## Usarlo en el móvil

**Opción A – Instalar el APK (recomendada)**
1. En GitHub ve a **Actions → «Tests y APK»** y abre la última ejecución en verde.
2. Descarga el artefacto **MFQ_All-apk** (es un .zip con el `.apk` dentro).
3. Pásalo al móvil, ábrelo y acepta «instalar apps de origen desconocido».

Si publicas una *Release* en GitHub, el APK se adjunta automáticamente a ella.

**Opción B – Probarlo sin instalar nada (desarrollo)**
1. Instala la app **Flet** desde Google Play.
2. En el ordenador: `pip install "flet[all]==1.1.3"` y luego `flet run --android app/src/main.py`.
3. Escanea el QR con el móvil (misma red Wi‑Fi).

## Usarlo en el ordenador

```bash
cd app
pip install "flet[all]==1.1.3"
flet run src/main.py          # ventana de escritorio
flet run --web src/main.py    # en el navegador
```

## Compilar el APK tú mismo

Necesitas Java 17 y el SDK de Android (Flet descarga Flutter automáticamente):

```bash
cd app
flet build apk
```

## Tests

```bash
cd app
pip install pytest "flet==1.1.3"
python -m pytest -q
```

Cada fórmula se comprueba despejando **todas** sus variables y verificando que
se recupera el valor original, además de valores reales conocidos
(g en la Tierra ≈ 9,82 m/s², velocidad de escape ≈ 11,2 km/s, 1 mol a 0 °C ≈ 1 atm).

## Estructura

```
app/
├── pyproject.toml          configuración de Flet / APK
├── src/
│   ├── main.py             punto de entrada y navegación
│   └── mfq/
│       ├── core/           lógica pura, sin interfaz (testeable)
│       │   ├── physics.py  catálogo declarativo de fórmulas
│       │   ├── maths.py    ecuaciones, funciones, MCD/MCM, π, binario…
│       │   ├── units.py    conversor de unidades
│       │   └── numbers.py  lectura de números («3,5», «6.67e-11») y formato
│       └── ui/             pantallas Flet
└── tests/
```

### Añadir una fórmula nueva

Basta con añadir un bloque `Formula(...)` en `src/mfq/core/physics.py`
indicando sus variables y cómo despejar cada una. La pantalla se genera sola.

## Cambios respecto a la v5

- **Errores corregidos**: la ley de los gases ideales multiplicaba por el número
  de Avogadro (resultados 10²³ veces mayores); las funciones de tiro parabólico
  usaban variables antes de pedirlas y se llamaban a sí mismas; la «ley de Ohm»
  calculaba «potencia» en lugar de tensión; menús recursivos que acababan
  desbordando la pila.
- Validación de datos con mensajes claros (división entre cero, raíces negativas…).
- Se quitan dependencias solo de Windows (`keyboard`, rutas `C:\\…`, `turtle`).
- Se elimina el descargador de YouTube: `pytube` ya no funciona y descargar
  vídeos va contra las condiciones de YouTube (además, Google Play no lo permite).

# MFQ All 6 · App para móvil y ordenador

<img src="src/assets/icon.png" width="96" align="right" alt="Icono">

Calculadora de **Física, Química y Matemáticas** con interfaz gráfica moderna
(Material 3, modo claro/oscuro), hecha en Python con [Flet](https://flet.dev).
Es la evolución de `MFQ_all v5.py` (versión de consola).

## Qué incluye

| Pestaña | Contenido |
|---|---|
| **Física** | 29 fórmulas en 9 categorías (cinemática, tiro parabólico, dinámica, energía, gravitación, fluidos, electricidad, ondas, química). En cada una eliges **qué variable despejar**, la app pide solo los datos necesarios y muestra el desarrollo *Datos → Fórmula → Resultado*, como en un examen. Buscador, **favoritas** (★), **conversor de unidades** (8 magnitudes, con tabla de equivalencias) y **constantes físicas**. |
| **Química** | **Masa molar** de cualquier fórmula (paréntesis, corchetes, hidratos como `CuSO4·5H2O`) con composición en %, paso de gramos a moles y moléculas, y **tabla periódica** de los 118 elementos con buscador. |
| **Mates** | Calculadora científica (DEG/RAD, `Ans`), porcentajes y regla de tres, fracciones, ecuación de 2º grado con gráfica, sistemas 2×2 y 3×3 (Gauss), representar hasta 3 funciones, resolver triángulos (seno/coseno, caso ambiguo), círculo, MCD/MCM/factores primos, binario y bases, π con hasta 5000 decimales, estadística (media, mediana, moda, cuartiles, desviación típica) y dados. |
| **Historial** | Se guarda en el dispositivo, agrupado por días y con buscador. Toca un resultado para copiarlo o cópialo todo de una vez. |
| **Ajustes** | Tema claro / oscuro / del sistema y número de cifras significativas (3–12). |

## Usarlo en el móvil

**Opción A – Instalar el APK (recomendada)**
1. Abre en el móvil este enlace de descarga directa:
   **https://github.com/ToxBox8/MFQ_all-GitHub/releases/latest/download/MFQ_All.apk**
   (o la página de la release: https://github.com/ToxBox8/MFQ_all-GitHub/releases/latest)
2. Abre el archivo descargado.
3. Acepta «instalar apps de origen desconocido» si Android te lo pide.

Cada vez que se sube código, GitHub Actions pasa los tests, compila el APK y
reemplaza el de esa release, así que el enlace siempre tiene la última versión.
También queda como artefacto en **Actions → «Tests y APK»**.

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

Hay 98 tests. Cada fórmula se comprueba despejando **todas** sus variables y verificando que
se recupera el valor original, además de valores reales conocidos
(g en la Tierra ≈ 9,82 m/s², velocidad de escape ≈ 11,2 km/s, 1 mol a 0 °C ≈ 1 atm).

## Estructura

```
app/
├── pyproject.toml          configuración de Flet / APK
├── src/
│   ├── main.py             punto de entrada y navegación
│   └── mfq/
│       ├── core/              lógica pura, sin interfaz (testeable)
│       │   ├── physics.py     catálogo declarativo de fórmulas
│       │   ├── chemistry.py   tabla periódica y masas molares
│       │   ├── constants.py   constantes físicas
│       │   ├── maths.py       ecuaciones, funciones, MCD/MCM, π, binario…
│       │   ├── maths_extra.py calculadora, estadística, sistemas, triángulos…
│       │   ├── units.py       conversor de unidades
│       │   └── numbers.py     lectura de números («3,5», «6.67e-11») y formato
│       └── ui/                pantallas Flet (una por pestaña + compartidos)
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

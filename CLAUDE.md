# Notas para Claude · MFQ All

## Estilo de interfaz preferido por ToxBox8: «GUI estilo Android»

A ToxBox8 le ha gustado mucho el diseño de la app MFQ All 6 (carpeta `app/`).
Úsalo como referencia por defecto para cualquier interfaz nueva, en este u otros proyectos.

**Tecnología:** Python + [Flet](https://flet.dev) (Material 3). Un mismo código sirve para
APK de Android, escritorio y web. El APK se compila en GitHub Actions y se publica en una
release fija con enlace de descarga directa.

**Rasgos del diseño:**
- Material 3 con color semilla `#3B6FE0` (azul) y tema claro / oscuro / del sistema.
- Barra de navegación inferior con 3–4 pestañas (icono relleno al seleccionar, contorno si no).
- AppBar arriba con icono a la izquierda y acciones (ajustes) a la derecha.
- Listas con `ListTile` (icono, título, subtítulo y chevron `>`), agrupadas con títulos de
  sección pequeños en color primario.
- Buscador redondeado (`border_radius=28`, relleno) arriba de las listas.
- Pantallas secundarias como vistas apiladas con flecha atrás (funciona el gesto atrás de Android).
- Tarjeta de resultado grande con fondo `PRIMARY_CONTAINER`, número en grande y negrita,
  botón de copiar, y versión roja (`ERROR_CONTAINER`) para errores con mensaje claro.
- Campos de texto con bordes redondeados (12), unidad en la etiqueta, valores por defecto útiles.
- Botón principal `FilledButton` ancho con icono + `OutlinedButton` secundario («Limpiar»).
- Tarjetas `FILLED` para cabeceras (p. ej. la ecuación) y `OUTLINED` para menús de herramientas.
- Accesos rápidos en «chips» o contenedores `SECONDARY_CONTAINER` redondeados.
- Estados vacíos con icono grande gris + título + texto explicativo.
- Avisos breves con `SnackBar` («Copiado al portapapeles»).
- Ancho máximo de contenido ~720 px para que en tablet/escritorio no se estire.

**Arquitectura que acompaña al estilo:** lógica pura en `core/` (con tests de pytest) separada de
la interfaz en `ui/`; textos y mensajes de error en español y pensados para el usuario.

## Preferencias de trabajo
- Responder en español y empezar con «Hola Toxbox».
- Discutir las ideas si hay una opción mejor, sin dar la razón siempre.

"""Utilidades numéricas: lectura tolerante de números y formato legible."""

from __future__ import annotations

import math


# Cifras significativas por defecto (la app lo cambia desde Ajustes)
SETTINGS = {"sig": 6}


class CalcError(ValueError):
    """Error de cálculo con un mensaje pensado para mostrarse al usuario."""


def parse_number(text: str, name: str = "valor") -> float:
    """Convierte el texto del usuario en float.

    Acepta coma decimal ("3,5"), notación científica ("6.67e-11"),
    "x10^" ("6.67x10^-11") y el símbolo de potencia "^".
    """
    if text is None:
        raise CalcError(f"Falta el {name}.")
    s = str(text).strip().replace(" ", "").replace(",", ".")
    if not s:
        raise CalcError(f"Falta el {name}.")
    for token in ("x10^", "×10^", "*10^", "*10**"):
        if token in s:
            base, exp = s.split(token, 1)
            s = f"{base or '1'}e{exp}"
            break
    try:
        value = float(s)
    except ValueError:
        raise CalcError(f"«{text}» no es un número válido para {name}.") from None
    if not math.isfinite(value):
        raise CalcError(f"El {name} debe ser un número finito.")
    return value


def fmt(value: float, sig: int | None = None) -> str:
    """Formatea un número con `sig` cifras significativas.

    Usa notación científica (×10ⁿ) para valores muy grandes o muy pequeños.
    """
    sig = sig or SETTINGS["sig"]
    if isinstance(value, complex):
        re, im = value.real, value.imag
        if abs(im) < 1e-15:
            return fmt(re, sig)
        sign = "+" if im >= 0 else "−"
        return f"{fmt(re, sig)} {sign} {fmt(abs(im), sig)}i"
    if value == 0:
        return "0"
    if not math.isfinite(value):
        return "∞" if value > 0 else "−∞"
    a = abs(value)
    if 1e-4 <= a < 1e7:
        text = f"{value:.{sig}g}"
        if "e" in text:  # .g puede pasar a científica en los bordes
            text = f"{value:.{sig}f}".rstrip("0").rstrip(".")
        return text.replace("-", "−")
    mantissa, exp = f"{value:.{sig - 1}e}".split("e")
    mantissa = mantissa.rstrip("0").rstrip(".")
    return f"{mantissa}×10^{int(exp)}".replace("-", "−")


def safe_div(a: float, b: float, what: str = "divisor") -> float:
    if b == 0:
        raise CalcError(f"El {what} no puede ser 0.")
    return a / b


def safe_sqrt(x: float, what: str = "radicando") -> float:
    if x < 0:
        raise CalcError(f"No hay solución real: el {what} es negativo.")
    return math.sqrt(x)

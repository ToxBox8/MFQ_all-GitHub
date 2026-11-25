"""Conversor de unidades (factores respecto a la unidad base de cada magnitud)."""

from __future__ import annotations

from .numbers import CalcError

# magnitud -> {unidad: factor a la unidad base}
LINEAR_UNITS: dict[str, dict[str, float]] = {
    "Longitud": {"km": 1e3, "hm": 1e2, "dam": 10, "m": 1, "dm": 0.1, "cm": 0.01,
                 "mm": 1e-3, "µm": 1e-6, "mi": 1609.344, "yd": 0.9144, "ft": 0.3048,
                 "in": 0.0254},
    "Masa": {"t": 1e6, "kg": 1e3, "hg": 100, "dag": 10, "g": 1, "dg": 0.1, "cg": 0.01,
             "mg": 1e-3, "lb": 453.59237, "oz": 28.349523125},
    "Volumen": {"m³": 1e3, "kL": 1e3, "hL": 100, "daL": 10, "L": 1, "dL": 0.1,
                "cL": 0.01, "mL": 1e-3, "cm³": 1e-3},
    "Tiempo": {"día": 86400, "h": 3600, "min": 60, "s": 1, "ms": 1e-3, "µs": 1e-6,
               "ns": 1e-9},
    "Velocidad": {"m/s": 1, "km/h": 1 / 3.6, "mi/h": 0.44704, "nudo": 1852 / 3600},
    "Presión": {"Pa": 1, "hPa": 100, "kPa": 1e3, "bar": 1e5, "atm": 101325,
                "mmHg": 133.322387415},
    "Energía": {"J": 1, "kJ": 1e3, "cal": 4.184, "kcal": 4184, "kWh": 3.6e6,
                "eV": 1.602176634e-19},
}

TEMPERATURE_UNITS = ["°C", "K", "°F"]


def quantities() -> list[str]:
    return [*LINEAR_UNITS, "Temperatura"]


def units_of(quantity: str) -> list[str]:
    if quantity == "Temperatura":
        return list(TEMPERATURE_UNITS)
    try:
        return list(LINEAR_UNITS[quantity])
    except KeyError:
        raise CalcError(f"Magnitud desconocida: {quantity}") from None


def convert(value: float, quantity: str, src: str, dst: str) -> float:
    if quantity == "Temperatura":
        return _convert_temperature(value, src, dst)
    table = LINEAR_UNITS.get(quantity)
    if table is None or src not in table or dst not in table:
        raise CalcError("Unidad no válida para esta magnitud.")
    return value * table[src] / table[dst]


def _convert_temperature(value: float, src: str, dst: str) -> float:
    to_k = {"°C": lambda v: v + 273.15, "K": lambda v: v,
            "°F": lambda v: (v - 32) * 5 / 9 + 273.15}
    from_k = {"°C": lambda k: k - 273.15, "K": lambda k: k,
              "°F": lambda k: (k - 273.15) * 9 / 5 + 32}
    if src not in to_k or dst not in from_k:
        raise CalcError("Unidad de temperatura no válida.")
    kelvin = to_k[src](value)
    if kelvin < 0:
        raise CalcError("Temperatura por debajo del cero absoluto.")
    return from_k[dst](kelvin)

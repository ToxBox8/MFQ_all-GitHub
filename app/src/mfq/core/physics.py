"""Catálogo declarativo de fórmulas de Física y Química.

Cada fórmula declara sus variables y, para cada una, cómo despejarla.
La interfaz se genera automáticamente a partir de estos datos, así que
añadir una fórmula nueva es añadir un bloque `Formula(...)` aquí.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

from .numbers import CalcError, safe_div as div, safe_sqrt as sqrt

# Constantes físicas (CODATA 2018)
G = 6.67430e-11          # N·m²/kg²
C = 299_792_458.0        # m/s
K_E = 8.9875517923e9     # N·m²/C²
R_GAS = 8.314462618      # J/(mol·K)
G0 = 9.80665             # m/s²


@dataclass(frozen=True)
class Var:
    label: str
    unit: str = ""
    default: float | None = None   # valor sugerido (p. ej. g = 9,81)
    positive: bool = False         # rechaza valores <= 0


@dataclass(frozen=True)
class Formula:
    id: str
    category: str
    name: str
    equation: str
    variables: dict[str, Var]
    solvers: dict[str, Callable[..., float]]
    note: str = ""
    describe: Callable[[float, dict], str] | None = None  # interpretación extra
    tags: tuple[str, ...] = field(default=())

    def inputs_for(self, unknown: str) -> list[str]:
        return [s for s in self.variables if s != unknown]

    def solve(self, unknown: str, values: dict[str, float]) -> float:
        if unknown not in self.solvers:
            raise CalcError(f"No se puede despejar {unknown} en esta fórmula.")
        for sym in self.inputs_for(unknown):
            if sym not in values:
                raise CalcError(f"Falta el valor de {sym}.")
            v = self.variables[sym]
            if v.positive and values[sym] <= 0:
                raise CalcError(f"{v.label} ({sym}) debe ser mayor que 0.")
        try:
            result = self.solvers[unknown](**{k: values[k] for k in self.inputs_for(unknown)})
        except ZeroDivisionError:
            raise CalcError("División entre cero: revisa los datos.") from None
        except (ValueError, OverflowError) as exc:
            if isinstance(exc, CalcError):
                raise
            raise CalcError("Los datos no tienen solución real.") from None
        if isinstance(result, complex) or not math.isfinite(result):
            raise CalcError("El resultado no es un número real finito.")
        return result


def _t_from_position(x, x0, v0, a):
    """Despeja t (>= 0) de x = x0 + v0·t + ½·a·t²."""
    if a == 0:
        t = div(x - x0, v0, "valor de v₀ (con a = 0)")
    else:
        disc = v0 * v0 + 2 * a * (x - x0)
        r = sqrt(disc, "discriminante")
        roots = [(-v0 + r) / a, (-v0 - r) / a]
        valid = [t for t in roots if t >= 0]
        if not valid:
            raise CalcError("No existe un tiempo positivo que cumpla la ecuación.")
        t = min(valid)
    if t < 0:
        raise CalcError("El tiempo resultante es negativo.")
    return t


def _reynolds_regime(re: float, _values: dict) -> str:
    if re < 2000:
        return "Régimen laminar (Re < 2000)"
    if re <= 4000:
        return "Régimen de transición (2000 ≤ Re ≤ 4000)"
    return "Régimen turbulento (Re > 4000)"


def _mach_regime(m: float, _values: dict) -> str:
    if m < 0.8:
        return "Subsónico"
    if m < 1.2:
        return "Transónico"
    if m < 5:
        return "Supersónico"
    return "Hipersónico"


def _angle_for_range(R, v0, g):
    s = div(g * R, v0 * v0, "valor de v₀")
    if not -1 <= s <= 1:
        raise CalcError("Alcance imposible con esa velocidad inicial.")
    return math.degrees(math.asin(s) / 2)


FORMULAS: list[Formula] = [
    # ---------------- Cinemática ----------------
    Formula(
        "mru", "Cinemática", "MRU", "x = x₀ + v·t",
        {"x": Var("Posición final", "m"), "x0": Var("Posición inicial", "m", 0.0),
         "v": Var("Velocidad", "m/s"), "t": Var("Tiempo", "s")},
        {"x": lambda x0, v, t: x0 + v * t,
         "x0": lambda x, v, t: x - v * t,
         "v": lambda x, x0, t: div(x - x0, t, "tiempo"),
         "t": lambda x, x0, v: div(x - x0, v, "velocidad")},
        tags=("movimiento rectilíneo uniforme",),
    ),
    Formula(
        "mrua_v", "Cinemática", "MRUA · velocidad", "v = v₀ + a·t",
        {"v": Var("Velocidad final", "m/s"), "v0": Var("Velocidad inicial", "m/s", 0.0),
         "a": Var("Aceleración", "m/s²"), "t": Var("Tiempo", "s")},
        {"v": lambda v0, a, t: v0 + a * t,
         "v0": lambda v, a, t: v - a * t,
         "a": lambda v, v0, t: div(v - v0, t, "tiempo"),
         "t": lambda v, v0, a: div(v - v0, a, "aceleración")},
        tags=("acelerado",),
    ),
    Formula(
        "mrua_x", "Cinemática", "MRUA · posición", "x = x₀ + v₀·t + ½·a·t²",
        {"x": Var("Posición final", "m"), "x0": Var("Posición inicial", "m", 0.0),
         "v0": Var("Velocidad inicial", "m/s"), "a": Var("Aceleración", "m/s²"),
         "t": Var("Tiempo", "s")},
        {"x": lambda x0, v0, a, t: x0 + v0 * t + 0.5 * a * t * t,
         "x0": lambda x, v0, a, t: x - v0 * t - 0.5 * a * t * t,
         "v0": lambda x, x0, a, t: div(x - x0 - 0.5 * a * t * t, t, "tiempo"),
         "a": lambda x, x0, v0, t: div(2 * (x - x0 - v0 * t), t * t, "tiempo"),
         "t": _t_from_position},
        tags=("acelerado",),
    ),
    Formula(
        "mrua_sin_t", "Cinemática", "MRUA · sin tiempo", "v² = v₀² + 2·a·Δx",
        {"v": Var("Velocidad final", "m/s"), "v0": Var("Velocidad inicial", "m/s", 0.0),
         "a": Var("Aceleración", "m/s²"), "dx": Var("Desplazamiento", "m")},
        {"v": lambda v0, a, dx: sqrt(v0 * v0 + 2 * a * dx, "valor de v²"),
         "v0": lambda v, a, dx: sqrt(v * v - 2 * a * dx, "valor de v₀²"),
         "a": lambda v, v0, dx: div(v * v - v0 * v0, 2 * dx, "desplazamiento"),
         "dx": lambda v, v0, a: div(v * v - v0 * v0, 2 * a, "aceleración")},
    ),
    Formula(
        "tiro_alcance", "Tiro parabólico", "Alcance horizontal", "R = v₀²·sin(2θ) / g",
        {"R": Var("Alcance", "m"), "v0": Var("Velocidad inicial", "m/s", positive=True),
         "theta": Var("Ángulo", "°"), "g": Var("Gravedad", "m/s²", G0, positive=True)},
        {"R": lambda v0, theta, g: v0 * v0 * math.sin(math.radians(2 * theta)) / g,
         "v0": lambda R, theta, g: sqrt(div(R * g, math.sin(math.radians(2 * theta)), "sin(2θ)"), "valor de v₀²"),
         "theta": _angle_for_range},
        note="Para el ángulo se da la solución baja (θ ≤ 45°); la alta es 90° − θ.",
        tags=("proyectil",),
    ),
    Formula(
        "tiro_altura", "Tiro parabólico", "Altura máxima", "H = v₀²·sin²θ / (2g)",
        {"H": Var("Altura máxima", "m"), "v0": Var("Velocidad inicial", "m/s", positive=True),
         "theta": Var("Ángulo", "°"), "g": Var("Gravedad", "m/s²", G0, positive=True)},
        {"H": lambda v0, theta, g: (v0 * math.sin(math.radians(theta))) ** 2 / (2 * g),
         "v0": lambda H, theta, g: div(sqrt(2 * g * H, "valor de 2gH"), math.sin(math.radians(theta)), "sin θ")},
        tags=("proyectil",),
    ),
    Formula(
        "tiro_tiempo", "Tiro parabólico", "Tiempo de vuelo", "T = 2·v₀·sinθ / g",
        {"T": Var("Tiempo de vuelo", "s"), "v0": Var("Velocidad inicial", "m/s", positive=True),
         "theta": Var("Ángulo", "°"), "g": Var("Gravedad", "m/s²", G0, positive=True)},
        {"T": lambda v0, theta, g: 2 * v0 * math.sin(math.radians(theta)) / g,
         "v0": lambda T, theta, g: div(T * g, 2 * math.sin(math.radians(theta)), "sin θ")},
        tags=("proyectil",),
    ),
    # ---------------- Dinámica ----------------
    Formula(
        "newton2", "Dinámica", "Segunda ley de Newton", "F = m·a",
        {"F": Var("Fuerza", "N"), "m": Var("Masa", "kg"), "a": Var("Aceleración", "m/s²")},
        {"F": lambda m, a: m * a,
         "m": lambda F, a: div(F, a, "aceleración"),
         "a": lambda F, m: div(F, m, "masa")},
    ),
    Formula(
        "peso", "Dinámica", "Peso", "P = m·g",
        {"P": Var("Peso", "N"), "m": Var("Masa", "kg"), "g": Var("Gravedad", "m/s²", G0)},
        {"P": lambda m, g: m * g,
         "m": lambda P, g: div(P, g, "gravedad"),
         "g": lambda P, m: div(P, m, "masa")},
    ),
    Formula(
        "rozamiento", "Dinámica", "Fuerza de rozamiento", "Fr = μ·N",
        {"Fr": Var("Fuerza de rozamiento", "N"), "mu": Var("Coeficiente de rozamiento (μ)"),
         "N": Var("Fuerza normal", "N")},
        {"Fr": lambda mu, N: mu * N,
         "mu": lambda Fr, N: div(Fr, N, "valor de la normal"),
         "N": lambda Fr, mu: div(Fr, mu, "coeficiente")},
    ),
    Formula(
        "hooke", "Dinámica", "Ley de Hooke", "F = k·x",
        {"F": Var("Fuerza elástica", "N"), "k": Var("Constante elástica", "N/m"),
         "x": Var("Elongación", "m")},
        {"F": lambda k, x: k * x,
         "k": lambda F, x: div(F, x, "elongación"),
         "x": lambda F, k: div(F, k, "valor de k")},
        tags=("muelle", "resorte"),
    ),
    # ---------------- Energía ----------------
    Formula(
        "ec", "Energía", "Energía cinética", "Ec = ½·m·v²",
        {"Ec": Var("Energía cinética", "J"), "m": Var("Masa", "kg"), "v": Var("Velocidad", "m/s")},
        {"Ec": lambda m, v: 0.5 * m * v * v,
         "m": lambda Ec, v: div(2 * Ec, v * v, "valor de v"),
         "v": lambda Ec, m: sqrt(div(2 * Ec, m, "masa"), "valor de 2Ec/m")},
    ),
    Formula(
        "ep", "Energía", "Energía potencial gravitatoria", "Ep = m·g·h",
        {"Ep": Var("Energía potencial", "J"), "m": Var("Masa", "kg"),
         "g": Var("Gravedad", "m/s²", G0), "h": Var("Altura", "m")},
        {"Ep": lambda m, g, h: m * g * h,
         "m": lambda Ep, g, h: div(Ep, g * h, "producto g·h"),
         "g": lambda Ep, m, h: div(Ep, m * h, "producto m·h"),
         "h": lambda Ep, m, g: div(Ep, m * g, "producto m·g")},
    ),
    Formula(
        "einstein", "Energía", "Relatividad especial", "E = m·c²",
        {"E": Var("Energía", "J"), "m": Var("Masa", "kg")},
        {"E": lambda m: m * C * C, "m": lambda E: E / (C * C)},
        note="c = 299 792 458 m/s",
    ),
    # ---------------- Gravitación ----------------
    Formula(
        "gravitacion", "Gravitación", "Ley de gravitación universal", "F = G·m₁·m₂ / r²",
        {"F": Var("Fuerza gravitatoria", "N"), "m1": Var("Masa 1", "kg"),
         "m2": Var("Masa 2", "kg"), "r": Var("Distancia", "m", positive=True)},
        {"F": lambda m1, m2, r: G * m1 * m2 / (r * r),
         "m1": lambda F, m2, r: div(F * r * r, G * m2, "valor de m₂"),
         "m2": lambda F, m1, r: div(F * r * r, G * m1, "valor de m₁"),
         "r": lambda F, m1, m2: sqrt(div(G * m1 * m2, F, "valor de F"), "valor de r²")},
        note="G = 6,6743×10⁻¹¹ N·m²/kg²",
    ),
    Formula(
        "v_escape", "Gravitación", "Velocidad de escape", "v = √(2·G·M / r)",
        {"v": Var("Velocidad de escape", "m/s"), "M": Var("Masa del astro", "kg"),
         "r": Var("Radio / distancia", "m", positive=True)},
        {"v": lambda M, r: sqrt(2 * G * M / r, "valor de 2GM/r"),
         "M": lambda v, r: v * v * r / (2 * G),
         "r": lambda v, M: div(2 * G * M, v * v, "valor de v")},
    ),
    Formula(
        "schwarzschild", "Gravitación", "Agujero negro (radio de Schwarzschild)", "r = 2·G·M / c²",
        {"r": Var("Radio de Schwarzschild", "m"), "M": Var("Masa", "kg")},
        {"r": lambda M: 2 * G * M / (C * C), "M": lambda r: r * C * C / (2 * G)},
    ),
    # ---------------- Fluidos ----------------
    Formula(
        "densidad", "Fluidos", "Densidad", "ρ = m / V",
        {"rho": Var("Densidad", "kg/m³"), "m": Var("Masa", "kg"), "V": Var("Volumen", "m³")},
        {"rho": lambda m, V: div(m, V, "volumen"),
         "m": lambda rho, V: rho * V,
         "V": lambda rho, m: div(m, rho, "valor de la densidad")},
    ),
    Formula(
        "pascal", "Fluidos", "Presión (Pascal)", "P = F / A",
        {"P": Var("Presión", "Pa"), "F": Var("Fuerza", "N"), "A": Var("Superficie", "m²")},
        {"P": lambda F, A: div(F, A, "área"),
         "F": lambda P, A: P * A,
         "A": lambda P, F: div(F, P, "valor de la presión")},
    ),
    Formula(
        "sustentacion", "Fluidos", "Sustentación", "L = ½·ρ·v²·S·C_L",
        {"L": Var("Fuerza de sustentación", "N"), "rho": Var("Densidad del fluido", "kg/m³", 1.225),
         "v": Var("Velocidad", "m/s"), "S": Var("Superficie alar", "m²"),
         "CL": Var("Coeficiente de sustentación")},
        {"L": lambda rho, v, S, CL: 0.5 * rho * v * v * S * CL,
         "rho": lambda L, v, S, CL: div(2 * L, v * v * S * CL, "producto v²·S·C_L"),
         "v": lambda L, rho, S, CL: sqrt(div(2 * L, rho * S * CL, "producto ρ·S·C_L"), "valor de v²"),
         "S": lambda L, rho, v, CL: div(2 * L, rho * v * v * CL, "producto ρ·v²·C_L"),
         "CL": lambda L, rho, v, S: div(2 * L, rho * v * v * S, "producto ρ·v²·S")},
        note="Densidad del aire a nivel del mar: 1,225 kg/m³",
        tags=("avión", "ala"),
    ),
    Formula(
        "presion_dinamica", "Fluidos", "Presión dinámica", "q = ½·ρ·v²",
        {"q": Var("Presión dinámica", "Pa"), "rho": Var("Densidad", "kg/m³", 1.225),
         "v": Var("Velocidad", "m/s")},
        {"q": lambda rho, v: 0.5 * rho * v * v,
         "rho": lambda q, v: div(2 * q, v * v, "valor de v"),
         "v": lambda q, rho: sqrt(div(2 * q, rho, "densidad"), "valor de v²")},
    ),
    Formula(
        "reynolds", "Fluidos", "Número de Reynolds (tipo de flujo)", "Re = ρ·v·L / μ",
        {"Re": Var("Número de Reynolds"), "rho": Var("Densidad", "kg/m³"),
         "v": Var("Velocidad", "m/s"), "L": Var("Longitud característica", "m"),
         "mu": Var("Viscosidad dinámica", "Pa·s")},
        {"Re": lambda rho, v, L, mu: div(rho * v * L, mu, "viscosidad"),
         "rho": lambda Re, v, L, mu: div(Re * mu, v * L, "producto v·L"),
         "v": lambda Re, rho, L, mu: div(Re * mu, rho * L, "producto ρ·L"),
         "L": lambda Re, rho, v, mu: div(Re * mu, rho * v, "producto ρ·v"),
         "mu": lambda Re, rho, v, L: div(rho * v * L, Re, "número de Reynolds")},
        describe=lambda value, values: _reynolds_regime(values.get("Re", value), values),
        tags=("laminar", "turbulento", "flujo"),
    ),
    Formula(
        "mach", "Fluidos", "Número de Mach", "M = v / a",
        {"M": Var("Número de Mach"), "v": Var("Velocidad del objeto", "m/s"),
         "a": Var("Velocidad del sonido", "m/s", 343.0)},
        {"M": lambda v, a: div(v, a, "velocidad del sonido"),
         "v": lambda M, a: M * a,
         "a": lambda M, v: div(v, M, "número de Mach")},
        describe=lambda value, values: _mach_regime(values.get("M", value), values),
    ),
    # ---------------- Electricidad ----------------
    Formula(
        "coulomb", "Electricidad", "Ley de Coulomb", "F = k·q₁·q₂ / r²",
        {"F": Var("Fuerza eléctrica", "N"), "q1": Var("Carga 1", "C"),
         "q2": Var("Carga 2", "C"), "r": Var("Distancia", "m", positive=True)},
        {"F": lambda q1, q2, r: K_E * q1 * q2 / (r * r),
         "q1": lambda F, q2, r: div(F * r * r, K_E * q2, "valor de q₂"),
         "q2": lambda F, q1, r: div(F * r * r, K_E * q1, "valor de q₁"),
         "r": lambda F, q1, q2: sqrt(div(K_E * q1 * q2, F, "valor de F"), "valor de r²")},
        note="k = 8,9875×10⁹ N·m²/C². F > 0 repulsiva, F < 0 atractiva.",
        tags=("fuerza eléctrica", "cargas"),
    ),
    Formula(
        "ohm", "Electricidad", "Ley de Ohm", "V = I·R",
        {"V": Var("Tensión", "V"), "I": Var("Intensidad", "A"), "R": Var("Resistencia", "Ω")},
        {"V": lambda I, R: I * R,
         "I": lambda V, R: div(V, R, "resistencia"),
         "R": lambda V, I: div(V, I, "intensidad")},
    ),
    Formula(
        "potencia_electrica", "Electricidad", "Potencia eléctrica", "P = V·I",
        {"P": Var("Potencia", "W"), "V": Var("Tensión", "V"), "I": Var("Intensidad", "A")},
        {"P": lambda V, I: V * I,
         "V": lambda P, I: div(P, I, "intensidad"),
         "I": lambda P, V: div(P, V, "tensión")},
    ),
    # ---------------- Ondas ----------------
    Formula(
        "ondas", "Ondas", "Ecuación de ondas", "v = λ·f",
        {"v": Var("Velocidad de propagación", "m/s"), "lam": Var("Longitud de onda (λ)", "m"),
         "f": Var("Frecuencia", "Hz")},
        {"v": lambda lam, f: lam * f,
         "lam": lambda v, f: div(v, f, "frecuencia"),
         "f": lambda v, lam: div(v, lam, "longitud de onda")},
    ),
    # ---------------- Química ----------------
    Formula(
        "gases_ideales", "Química", "Ley de los gases ideales", "P·V = n·R·T",
        {"P": Var("Presión", "Pa"), "V": Var("Volumen", "m³"), "n": Var("Moles", "mol"),
         "T": Var("Temperatura", "K")},
        {"P": lambda V, n, T: div(n * R_GAS * T, V, "volumen"),
         "V": lambda P, n, T: div(n * R_GAS * T, P, "valor de la presión"),
         "n": lambda P, V, T: div(P * V, R_GAS * T, "valor de la temperatura"),
         "T": lambda P, V, n: div(P * V, n * R_GAS, "número de moles")},
        note="R = 8,314 J/(mol·K). Usa unidades SI: Pa, m³ y K (1 atm = 101 325 Pa, 1 L = 0,001 m³).",
    ),
    Formula(
        "molaridad", "Química", "Molaridad", "M = n / V",
        {"M": Var("Molaridad", "mol/L"), "n": Var("Moles de soluto", "mol"),
         "V": Var("Volumen de disolución", "L")},
        {"M": lambda n, V: div(n, V, "volumen"),
         "n": lambda M, V: M * V,
         "V": lambda M, n: div(n, M, "valor de la molaridad")},
    ),
]

FORMULAS_BY_ID: dict[str, Formula] = {f.id: f for f in FORMULAS}


def categories() -> list[str]:
    seen: list[str] = []
    for f in FORMULAS:
        if f.category not in seen:
            seen.append(f.category)
    return seen


def search(query: str) -> list[Formula]:
    """Búsqueda sin distinguir mayúsculas ni tildes."""
    q = _norm(query)
    if not q:
        return list(FORMULAS)
    return [f for f in FORMULAS
            if q in _norm(" ".join((f.name, f.category, f.equation, *f.tags)))]


def _norm(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn").strip()

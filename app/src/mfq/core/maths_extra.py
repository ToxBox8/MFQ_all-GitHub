"""Más herramientas de matemáticas: estadística, sistemas, triángulos, fracciones…"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from fractions import Fraction

from .maths import compile_function
from .numbers import CalcError, parse_number


# ------------------------------------------------------- Calculadora general
def evaluate(expr: str, degrees: bool = False) -> float:
    """Evalúa una expresión numérica (sin x). Trigonometría en grados si `degrees`."""
    if "x" in expr.lower().replace("exp", ""):
        raise CalcError("Aquí no se usa x. Para funciones, usa «Representar funciones».")
    try:
        value = compile_function(expr, degrees=degrees)(0.0)
    except ZeroDivisionError:
        raise CalcError("División entre cero.") from None
    except (ValueError, OverflowError):
        raise CalcError("Operación fuera de dominio o número demasiado grande.") from None
    if isinstance(value, complex) or not math.isfinite(value):
        raise CalcError("El resultado no es un número real.")
    return value


# ---------------------------------------------------------------- Estadística
@dataclass
class Stats:
    n: int
    total: float
    mean: float
    median: float
    modes: list[float]
    minimum: float
    maximum: float
    rng: float
    var_pop: float
    std_pop: float
    var_sample: float | None
    std_sample: float | None
    q1: float
    q3: float


def parse_data(text: str) -> list[float]:
    import re
    parts = [p for p in re.split(r"[\s;]+", text.strip()) if p]
    # se aceptan comas decimales si se separa con espacios o «;»
    if len(parts) == 1 and "," in parts[0]:
        parts = [p for p in parts[0].split(",") if p]
    values = [parse_number(p, "dato") for p in parts]
    if not values:
        raise CalcError("Introduce los datos separados por espacios o «;».")
    return values


def describe(data: list[float]) -> Stats:
    if not data:
        raise CalcError("No hay datos.")
    s = sorted(data)
    n = len(s)
    counts: dict[float, int] = {}
    for v in s:
        counts[v] = counts.get(v, 0) + 1
    top = max(counts.values())
    modes = [] if top == 1 and n > 1 else [v for v, c in counts.items() if c == top]
    if n >= 2:
        q = statistics.quantiles(s, n=4, method="inclusive")
        q1, q3 = q[0], q[2]
    else:
        q1 = q3 = s[0]
    return Stats(
        n=n, total=sum(s), mean=statistics.fmean(s), median=statistics.median(s),
        modes=modes, minimum=s[0], maximum=s[-1], rng=s[-1] - s[0],
        var_pop=statistics.pvariance(s), std_pop=statistics.pstdev(s),
        var_sample=statistics.variance(s) if n > 1 else None,
        std_sample=statistics.stdev(s) if n > 1 else None,
        q1=q1, q3=q3,
    )


# ------------------------------------------------------ Sistemas lineales
def solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Gauss con pivoteo parcial. Lanza CalcError si no hay solución única."""
    n = len(matrix)
    a = [list(map(float, row)) + [float(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[piv][col]) < 1e-12:
            # distingue incompatible de indeterminado
            raise CalcError(_classify_singular(matrix, rhs))
        a[col], a[piv] = a[piv], a[col]
        for r in range(n):
            if r != col:
                f = a[r][col] / a[col][col]
                for c in range(col, n + 1):
                    a[r][c] -= f * a[col][c]
    return [a[i][n] / a[i][i] + 0.0 for i in range(n)]


def _rank(rows: list[list[float]]) -> int:
    m = [list(r) for r in rows]
    rank, cols = 0, len(m[0]) if m else 0
    for c in range(cols):
        piv = next((r for r in range(rank, len(m)) if abs(m[r][c]) > 1e-12), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for r in range(len(m)):
            if r != rank and abs(m[r][c]) > 1e-12:
                f = m[r][c] / m[rank][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[rank])]
        rank += 1
    return rank


def _classify_singular(matrix, rhs) -> str:
    r_a = _rank(matrix)
    r_ab = _rank([list(row) + [b] for row, b in zip(matrix, rhs)])
    if r_a < r_ab:
        return "Sistema incompatible: no tiene solución."
    return "Sistema compatible indeterminado: infinitas soluciones."


# ---------------------------------------------------------------- Triángulos
@dataclass
class Triangle:
    a: float
    b: float
    c: float
    A: float   # grados, opuesto a a
    B: float
    C: float

    @property
    def perimeter(self) -> float:
        return self.a + self.b + self.c

    @property
    def area(self) -> float:
        return 0.5 * self.b * self.c * math.sin(math.radians(self.A))

    @property
    def kind(self) -> str:
        sides = {round(self.a, 9), round(self.b, 9), round(self.c, 9)}
        by_sides = {1: "equilátero", 2: "isósceles"}.get(len(sides), "escaleno")
        big = max(self.A, self.B, self.C)
        by_angle = ("rectángulo" if abs(big - 90) < 1e-7 else
                    "obtusángulo" if big > 90 else "acutángulo")
        return f"{by_sides}, {by_angle}"


def solve_triangle(a=None, b=None, c=None, A=None, B=None, C=None) -> list[Triangle]:
    """Resuelve un triángulo con 3 datos (al menos un lado). Ángulos en grados.

    Devuelve una lista porque el caso ambiguo (LLA) puede tener 2 soluciones.
    """
    sides = {"a": a, "b": b, "c": c}
    angles = {"A": A, "B": B, "C": C}
    given = sum(v is not None for v in (*sides.values(), *angles.values()))
    if given != 3:
        raise CalcError("Introduce exactamente 3 datos (al menos un lado).")
    if all(v is None for v in sides.values()):
        raise CalcError("Con solo ángulos hay infinitos triángulos: da al menos un lado.")
    for k, v in sides.items():
        if v is not None and v <= 0:
            raise CalcError(f"El lado {k} debe ser positivo.")
    for k, v in angles.items():
        if v is not None and not 0 < v < 180:
            raise CalcError(f"El ángulo {k} debe estar entre 0° y 180°.")

    known_angles = [k for k, v in angles.items() if v is not None]
    if len(known_angles) >= 2:  # ALA / LAA
        if sum(angles[k] for k in known_angles) >= 180:
            raise CalcError("Los ángulos suman 180° o más.")
        missing = next(k for k in "ABC" if angles[k] is None)
        angles[missing] = 180 - sum(angles[k] for k in known_angles)
        side_k = next(k for k in "abc" if sides[k] is not None)
        ratio = sides[side_k] / _sin(angles[side_k.upper()])
        for k in "abc":
            sides[k] = ratio * _sin(angles[k.upper()])
        return [_make(sides, angles)]

    if len(known_angles) == 0:  # LLL
        x, y, z = sides["a"], sides["b"], sides["c"]
        if x + y <= z or x + z <= y or y + z <= x:
            raise CalcError("Esos lados no forman un triángulo (desigualdad triangular).")
        angles["A"] = _acos((y * y + z * z - x * x) / (2 * y * z))
        angles["B"] = _acos((x * x + z * z - y * y) / (2 * x * z))
        angles["C"] = 180 - angles["A"] - angles["B"]
        return [_make(sides, angles)]

    # un ángulo y dos lados
    ang = known_angles[0]
    opp = ang.lower()
    if sides[opp] is None:  # LAL: el ángulo está entre los dos lados
        s1, s2 = [sides[k] for k in "abc" if k != opp]
        sides[opp] = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(math.radians(angles[ang])))
        return solve_triangle(a=sides["a"], b=sides["b"], c=sides["c"])
    # LLA (caso ambiguo)
    other = next(k for k in "abc" if k != opp and sides[k] is not None)
    s = sides[other] * _sin(angles[ang]) / sides[opp]
    if s > 1 + 1e-12:
        raise CalcError("No existe ningún triángulo con esos datos.")
    s = min(s, 1.0)
    sols = []
    for cand in {round(math.degrees(math.asin(s)), 12), round(180 - math.degrees(math.asin(s)), 12)}:
        if angles[ang] + cand < 180 - 1e-9:
            new_angles = dict(angles)
            new_angles[other.upper()] = cand
            third = next(k for k in "ABC" if new_angles[k] is None)
            new_angles[third] = 180 - angles[ang] - cand
            ratio = sides[opp] / _sin(angles[ang])
            new_sides = {k: ratio * _sin(new_angles[k.upper()]) for k in "abc"}
            sols.append(_make(new_sides, new_angles))
    if not sols:
        raise CalcError("No existe ningún triángulo con esos datos.")
    return sorted(sols, key=lambda t: t.A + 10 * t.B)


def _sin(deg: float) -> float:
    return math.sin(math.radians(deg))


def _acos(x: float) -> float:
    return math.degrees(math.acos(max(-1.0, min(1.0, x))))


def _make(s, a) -> Triangle:
    return Triangle(s["a"], s["b"], s["c"], a["A"], a["B"], a["C"])


# ----------------------------------------------------------------- Fracciones
def parse_fraction(text: str) -> Fraction:
    t = text.strip().replace(" ", "").replace(",", ".")
    if not t:
        raise CalcError("Falta una fracción.")
    try:
        f = Fraction(t)
    except (ValueError, ZeroDivisionError):
        raise CalcError(f"«{text}» no es una fracción válida (p. ej. 3/4 o 0.25).") from None
    return f


def fraction_op(a: str, op: str, b: str) -> Fraction:
    x, y = parse_fraction(a), parse_fraction(b)
    if op == "+":
        return x + y
    if op == "−" or op == "-":
        return x - y
    if op == "×" or op == "*":
        return x * y
    if op == "÷" or op == "/":
        if y == 0:
            raise CalcError("No se puede dividir entre 0.")
        return x / y
    raise CalcError("Operación no válida.")


def mixed(f: Fraction) -> str:
    if f.denominator == 1 or abs(f) < 1:
        return str(f)
    whole = int(f)  # trunca hacia 0
    rest = abs(f - whole)
    return f"{whole} {rest.numerator}/{rest.denominator}"


# ------------------------------------------------------- Porcentajes y reglas
def percent_of(p: float, total: float) -> float:
    return p / 100 * total


def what_percent(part: float, total: float) -> float:
    if total == 0:
        raise CalcError("El total no puede ser 0.")
    return part / total * 100


def percent_change(old: float, new: float) -> float:
    if old == 0:
        raise CalcError("El valor inicial no puede ser 0.")
    return (new - old) / old * 100


def rule_of_three(a: float, b: float, c: float, inverse: bool = False) -> float:
    """Directa: a → b, c → x ⇒ x = b·c/a.  Inversa: x = a·b/c."""
    if inverse:
        if c == 0:
            raise CalcError("El tercer valor no puede ser 0.")
        return a * b / c
    if a == 0:
        raise CalcError("El primer valor no puede ser 0.")
    return b * c / a

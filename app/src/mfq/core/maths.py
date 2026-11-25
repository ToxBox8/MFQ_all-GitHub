"""Herramientas de matemáticas."""

from __future__ import annotations

import ast
import cmath
import math
import operator
import random
from dataclasses import dataclass
from functools import reduce
from typing import Callable

from .numbers import CalcError


# ---------------------------------------------------------------- Ecuaciones
@dataclass
class QuadraticResult:
    roots: list[complex | float]
    discriminant: float | None
    vertex: tuple[float, float] | None
    kind: str


def solve_quadratic(a: float, b: float, c: float) -> QuadraticResult:
    """Resuelve a·x² + b·x + c = 0 (también los casos degenerados)."""
    if a == 0:
        if b == 0:
            kind = "Identidad: infinitas soluciones" if c == 0 else "Sin solución"
            return QuadraticResult([], None, None, kind)
        return QuadraticResult([-c / b], None, None, "Ecuación de primer grado")
    d = b * b - 4 * a * c
    vertex = (-b / (2 * a), c - b * b / (4 * a))
    if d > 0:
        r = math.sqrt(d)
        roots = sorted([(-b - r) / (2 * a), (-b + r) / (2 * a)])
        kind = "Dos soluciones reales distintas"
    elif d == 0:
        roots = [-b / (2 * a)]
        kind = "Una solución real doble"
    else:
        r = cmath.sqrt(d)
        roots = [(-b + r) / (2 * a), (-b - r) / (2 * a)]
        kind = "Dos soluciones complejas conjugadas"
    return QuadraticResult(roots, d, vertex, kind)


# ---------------------------------------------------- Expresiones seguras f(x)
_FUNCS: dict[str, Callable] = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin,
    "acos": math.acos, "atan": math.atan, "sqrt": math.sqrt, "raiz": math.sqrt,
    "log": math.log10, "ln": math.log, "exp": math.exp, "abs": abs,
    "sen": math.sin,
}
_FUNCS_DEG: dict[str, Callable] = {
    **_FUNCS,
    "sin": lambda v: math.sin(math.radians(v)), "sen": lambda v: math.sin(math.radians(v)),
    "cos": lambda v: math.cos(math.radians(v)), "tan": lambda v: math.tan(math.radians(v)),
    "asin": lambda v: math.degrees(math.asin(v)), "acos": lambda v: math.degrees(math.acos(v)),
    "atan": lambda v: math.degrees(math.atan(v)),
}
_CONSTS = {"pi": math.pi, "e": math.e, "π": math.pi}
_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
_UNOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def compile_function(expr: str, degrees: bool = False) -> Callable[[float], float]:
    """Compila una expresión en x de forma segura (sin eval).

    Admite: + − * / ^ %, paréntesis, constantes pi y e, y las funciones
    sin/sen, cos, tan, asin, acos, atan, sqrt/raiz, log (base 10), ln, exp, abs.
    También multiplicación implícita sencilla como «2x» o «3(x+1)».
    """
    src = _preprocess(expr)
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError:
        raise CalcError("La expresión no es válida.") from None
    _validate(tree.body)

    funcs = _FUNCS_DEG if degrees else _FUNCS

    def f(x: float) -> float:
        return _eval(tree.body, x, funcs)

    return f


def _preprocess(expr: str) -> str:
    import re
    s = expr.strip().lower().replace(" ", "").replace("^", "**").replace("×", "*").replace("·", "*")
    s = s.replace(",", ".").replace("−", "-").replace("÷", "/").replace("π", "pi")
    s = re.sub(r"√(\d+(?:\.\d+)?|pi|e|x)", r"sqrt(\1)", s).replace("√", "sqrt")
    if s.startswith("y="):
        s = s[2:]
    if s.startswith("f(x)="):
        s = s[5:]
    if not s:
        raise CalcError("Escribe una función, por ejemplo: x^2 - 3x + 2")
    # 2x -> 2*x, 2( -> 2*(, )x -> )*x, )( -> )*(, x( -> x*(
    s = re.sub(r"(\d)(?!e[+-]?\d)([a-z(])", r"\1*\2", s)  # respeta 1e-5
    s = re.sub(r"\)\s*([a-z0-9(])", r")*\1", s)
    s = re.sub(r"\bx\s*\(", "x*(", s)
    return s


def _validate(node: ast.AST) -> None:
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        _validate(node.left), _validate(node.right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _UNOPS:
        _validate(node.operand)
    elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        pass
    elif isinstance(node, ast.Name) and (node.id == "x" or node.id in _CONSTS):
        pass
    elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
          and node.func.id in _FUNCS and len(node.args) == 1 and not node.keywords):
        _validate(node.args[0])
    else:
        raise CalcError("La expresión contiene elementos no permitidos.")


def _eval(node: ast.AST, x: float, funcs: dict[str, Callable]) -> float:
    if isinstance(node, ast.BinOp):
        left, right = _eval(node.left, x, funcs), _eval(node.right, x, funcs)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise OverflowError
        return _BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp):
        return _UNOPS[type(node.op)](_eval(node.operand, x, funcs))
    if isinstance(node, ast.Constant):
        return float(node.value)
    if isinstance(node, ast.Name):
        return x if node.id == "x" else _CONSTS[node.id]
    if isinstance(node, ast.Call):
        return funcs[node.func.id](_eval(node.args[0], x, funcs))
    raise CalcError("Expresión no soportada.")


def sample_function(f: Callable[[float], float], x_min: float, x_max: float,
                    n: int = 400) -> list[tuple[float, float | None]]:
    """Muestrea f en [x_min, x_max]; None donde no está definida."""
    if x_max <= x_min:
        raise CalcError("El intervalo debe cumplir x mín < x máx.")
    pts: list[tuple[float, float | None]] = []
    for i in range(n + 1):
        x = x_min + (x_max - x_min) * i / n
        try:
            y = f(x)
            if isinstance(y, complex) or not math.isfinite(y):
                y = None
        except (ValueError, ZeroDivisionError, OverflowError):
            y = None
        pts.append((x, y))
    return pts


# ------------------------------------------------------------- Aritmética
def gcd_many(nums: list[int]) -> int:
    _check_ints(nums)
    return reduce(math.gcd, nums)


def lcm_many(nums: list[int]) -> int:
    _check_ints(nums)
    if any(n == 0 for n in nums):
        return 0
    return reduce(lambda a, b: abs(a * b) // math.gcd(a, b), nums)


def parse_int_list(text: str) -> list[int]:
    parts = [p for p in text.replace(";", " ").replace(",", " ").split() if p]
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        raise CalcError("Introduce números enteros separados por espacios o comas.") from None
    _check_ints(nums)
    return nums


def _check_ints(nums: list[int]) -> None:
    if len(nums) < 2:
        raise CalcError("Introduce al menos dos números enteros.")


def prime_factors(n: int) -> list[int]:
    if n < 2:
        raise CalcError("Introduce un entero mayor que 1.")
    if n > 10**15:
        raise CalcError("Número demasiado grande (máximo 10^15).")
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


# ---------------------------------------------------------------- Geometría
def circle(radius: float) -> dict[str, float]:
    if radius < 0:
        raise CalcError("El radio no puede ser negativo.")
    return {"area": math.pi * radius ** 2, "perimetro": 2 * math.pi * radius,
            "diametro": 2 * radius}


# --------------------------------------------------------------------- Pi
def pi_digits(decimals: int) -> str:
    """π con `decimals` decimales exactos (fórmula de Machin, aritmética entera)."""
    if not 1 <= decimals <= 5000:
        raise CalcError("Elige entre 1 y 5000 decimales.")
    guard = 10
    scale = 10 ** (decimals + guard)

    def arctan_inv(x: int) -> int:
        total = term = scale // x
        x2, n, sign = x * x, 1, -1
        while term:
            term //= x2
            n += 2
            total += sign * (term // n)
            sign = -sign
        return total

    pi = 4 * (4 * arctan_inv(5) - arctan_inv(239))
    s = str(pi // 10 ** guard)
    return f"{s[0]}.{s[1:]}"


# ------------------------------------------------------------------ Binario
def text_to_binary(text: str) -> str:
    return " ".join(f"{b:08b}" for b in text.encode("utf-8"))


def binary_to_text(binary: str) -> str:
    cleaned = binary.replace(",", " ").replace("\xa0", " ").split()
    if not cleaned:
        raise CalcError("Introduce bytes en binario, p. ej. 01001000 01101001")
    if len(cleaned) == 1 and len(cleaned[0]) > 8 and len(cleaned[0]) % 8 == 0:
        cleaned = [cleaned[0][i:i + 8] for i in range(0, len(cleaned[0]), 8)]
    try:
        data = bytes(int(b, 2) for b in cleaned if len(b) <= 8 and set(b) <= {"0", "1"})
    except ValueError:
        raise CalcError("Hay bytes no válidos.") from None
    if len(data) != len(cleaned):
        raise CalcError("Cada byte debe tener hasta 8 bits (solo 0 y 1).")
    return data.decode("utf-8", errors="replace")


def int_to_bases(n: int) -> dict[str, str]:
    sign = "-" if n < 0 else ""
    n = abs(n)
    return {"Binario": sign + bin(n)[2:], "Octal": sign + oct(n)[2:],
            "Decimal": sign + str(n), "Hexadecimal": sign + hex(n)[2:].upper()}


# --------------------------------------------------------------------- Dado
def roll_dice(count: int = 1, faces: int = 6, rng: random.Random | None = None) -> list[int]:
    if not 1 <= count <= 100:
        raise CalcError("Puedes lanzar entre 1 y 100 dados.")
    if not 2 <= faces <= 1000:
        raise CalcError("Un dado debe tener entre 2 y 1000 caras.")
    rng = rng or random.SystemRandom()
    return [rng.randint(1, faces) for _ in range(count)]

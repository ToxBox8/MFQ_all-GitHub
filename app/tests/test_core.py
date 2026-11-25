import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mfq.core import maths, physics, units  # noqa: E402
from mfq.core.numbers import CalcError, fmt, parse_number  # noqa: E402


# ------------------------------------------------------------------ números
@pytest.mark.parametrize("text,expected", [
    ("3,5", 3.5), ("6.67e-11", 6.67e-11), ("6.67x10^-11", 6.67e-11),
    (" -2 ", -2.0), ("1×10^3", 1000.0),
])
def test_parse_number(text, expected):
    assert parse_number(text) == pytest.approx(expected)


@pytest.mark.parametrize("bad", ["", "abc", "nan", "inf"])
def test_parse_number_rejects(bad):
    with pytest.raises(CalcError):
        parse_number(bad)


def test_fmt():
    assert fmt(9.80665) == "9.80665"
    assert fmt(0) == "0"
    assert fmt(6.6743e-11) == "6.6743×10^−11"
    assert fmt(1.5e9) == "1.5×10^9"


# ------------------------------------------------------------------- física
def _roundtrip(formula, values):
    """Para cada variable: despejarla a partir del resto debe devolver su valor."""
    for unknown in formula.solvers:
        inputs = {k: v for k, v in values.items() if k != unknown}
        got = formula.solve(unknown, inputs)
        assert got == pytest.approx(values[unknown], rel=1e-9), (formula.id, unknown)


CASES = {
    "mru": {"x0": 2, "v": 3, "t": 4, "x": 14},
    "mrua_v": {"v0": 2, "a": 3, "t": 4, "v": 14},
    "mrua_x": {"x0": 1, "v0": 2, "a": 3, "t": 4, "x": 1 + 8 + 24},
    "mrua_sin_t": {"v0": 3, "a": 2, "dx": 4, "v": 5},
    "newton2": {"m": 2, "a": 3, "F": 6},
    "peso": {"m": 10, "g": 9.8, "P": 98},
    "rozamiento": {"mu": 0.3, "N": 100, "Fr": 30},
    "hooke": {"k": 200, "x": 0.1, "F": 20},
    "ec": {"m": 2, "v": 3, "Ec": 9},
    "ep": {"m": 2, "g": 10, "h": 5, "Ep": 100},
    "einstein": {"m": 1, "E": physics.C ** 2},
    "gravitacion": {"m1": 5.972e24, "m2": 70, "r": 6.371e6},
    "v_escape": {"M": 5.972e24, "r": 6.371e6},
    "schwarzschild": {"M": 1.989e30},
    "densidad": {"m": 10, "V": 2, "rho": 5},
    "pascal": {"F": 100, "A": 4, "P": 25},
    "sustentacion": {"rho": 1.225, "v": 70, "S": 16, "CL": 0.5},
    "presion_dinamica": {"rho": 1.225, "v": 100},
    "reynolds": {"rho": 1000, "v": 2, "L": 0.05, "mu": 0.001},
    "mach": {"v": 686, "a": 343, "M": 2},
    "coulomb": {"q1": 1e-6, "q2": 2e-6, "r": 0.1},
    "ohm": {"I": 2, "R": 5, "V": 10},
    "potencia_electrica": {"V": 230, "I": 2, "P": 460},
    "ondas": {"lam": 2, "f": 170, "v": 340},
    "gases_ideales": {"V": 0.0224, "n": 1, "T": 273.15},
    "molaridad": {"n": 0.5, "V": 2, "M": 0.25},
    "tiro_alcance": {"v0": 20, "theta": 30, "g": 9.8},
    "tiro_altura": {"v0": 20, "theta": 30, "g": 9.8},
    "tiro_tiempo": {"v0": 20, "theta": 30, "g": 9.8},
}


@pytest.mark.parametrize("fid", list(CASES))
def test_formula_roundtrip(fid):
    f = physics.FORMULAS_BY_ID[fid]
    values = dict(CASES[fid])
    # completar la variable resultado si no se dio
    target = next(iter(f.variables))
    if target not in values:
        values[target] = f.solve(target, values)
    _roundtrip(f, values)


def test_every_formula_has_a_case():
    assert set(CASES) == set(physics.FORMULAS_BY_ID)


def test_known_values():
    grav = physics.FORMULAS_BY_ID["gravitacion"]
    F = grav.solve("F", {"m1": 5.972e24, "m2": 1, "r": 6.371e6})
    assert F == pytest.approx(9.82, rel=1e-2)            # g en la superficie
    ve = physics.FORMULAS_BY_ID["v_escape"].solve("v", {"M": 5.972e24, "r": 6.371e6})
    assert ve == pytest.approx(11186, rel=1e-3)
    P = physics.FORMULAS_BY_ID["gases_ideales"].solve("P", {"V": 0.022414, "n": 1, "T": 273.15})
    assert P == pytest.approx(101325, rel=1e-3)          # 1 atm (corrige el bug de v5)


def test_errors_are_friendly():
    f = physics.FORMULAS_BY_ID["newton2"]
    with pytest.raises(CalcError):
        f.solve("a", {"F": 10, "m": 0})
    with pytest.raises(CalcError):
        physics.FORMULAS_BY_ID["gravitacion"].solve("F", {"m1": 1, "m2": 1, "r": 0})
    with pytest.raises(CalcError):
        physics.FORMULAS_BY_ID["tiro_alcance"].solve("theta", {"R": 1000, "v0": 10, "g": 9.8})


def test_describe_and_search():
    re = physics.FORMULAS_BY_ID["reynolds"]
    assert "laminar" in re.describe(1500, {}).lower()
    assert "turbulento" in re.describe(1e5, {}).lower()
    assert any(f.id == "reynolds" for f in physics.search("turbulento"))
    assert any(f.id == "gravitacion" for f in physics.search("GRAVITACION"))  # sin tilde


# -------------------------------------------------------------------- mates
def test_quadratic():
    r = maths.solve_quadratic(1, -3, 2)
    assert r.roots == [1, 2] and r.discriminant == 1
    r = maths.solve_quadratic(1, 2, 5)
    assert all(isinstance(z, complex) for z in r.roots)
    assert maths.solve_quadratic(0, 2, -4).roots == [2]
    assert maths.solve_quadratic(0, 0, 0).roots == []


@pytest.mark.parametrize("expr,x,y", [
    ("x^2 - 3x + 2", 1, 0), ("2(x+1)", 2, 6), ("sin(pi/2)", 0, 1),
    ("y = sqrt(x)", 9, 3), ("ln(e)", 0, 1), ("-x^2", 3, -9),
])
def test_compile_function(expr, x, y):
    assert maths.compile_function(expr)(x) == pytest.approx(y)


@pytest.mark.parametrize("bad", ["__import__('os')", "x.real", "open(1)", "", "[x]"])
def test_compile_function_rejects(bad):
    with pytest.raises(CalcError):
        maths.compile_function(bad)


def test_sample_function_handles_domain():
    pts = maths.sample_function(maths.compile_function("sqrt(x)"), -1, 1, 10)
    assert pts[0][1] is None and pts[-1][1] == pytest.approx(1)


def test_gcd_lcm_factors():
    assert maths.gcd_many([12, 18, 24]) == 6
    assert maths.lcm_many([4, 6, 10]) == 60
    assert maths.parse_int_list("4, 6;10") == [4, 6, 10]
    assert maths.prime_factors(360) == [2, 2, 2, 3, 3, 5]


def test_pi():
    assert maths.pi_digits(30) == "3.141592653589793238462643383279"
    assert maths.pi_digits(1000).startswith(str(math.pi)[:15])


def test_binary_roundtrip():
    for text in ["Hola", "Ñandú ⚛"]:
        assert maths.binary_to_text(maths.text_to_binary(text)) == text
    assert maths.binary_to_text("0100100001101001") == "Hi"
    assert maths.int_to_bases(255)["Hexadecimal"] == "FF"


def test_dice():
    rolls = maths.roll_dice(50, 6, random.Random(1))
    assert len(rolls) == 50 and all(1 <= r <= 6 for r in rolls)
    with pytest.raises(CalcError):
        maths.roll_dice(0, 6)


# ------------------------------------------------------------------ unidades
def test_units():
    assert units.convert(1, "Longitud", "km", "m") == 1000
    assert units.convert(36, "Velocidad", "km/h", "m/s") == pytest.approx(10)
    assert units.convert(1, "Presión", "atm", "Pa") == 101325
    assert units.convert(100, "Temperatura", "°C", "°F") == pytest.approx(212)
    assert units.convert(0, "Temperatura", "K", "°C") == pytest.approx(-273.15)
    with pytest.raises(CalcError):
        units.convert(-300, "Temperatura", "°C", "K")
    for q in units.quantities():
        assert units.units_of(q)

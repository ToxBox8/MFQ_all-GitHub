"""Química: tabla periódica y cálculo de masas molares a partir de fórmulas."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .numbers import CalcError


@dataclass(frozen=True)
class Element:
    z: int
    symbol: str
    name: str
    mass: float      # masa atómica estándar (u); entre paréntesis en la tabla si es radiactivo
    group: str       # familia química


# Familias abreviadas
AM, AT, MT, MP, SM, NM, HA, GN, LA, AC = (
    "Metal alcalino", "Alcalinotérreo", "Metal de transición", "Metal del bloque p",
    "Semimetal", "No metal", "Halógeno", "Gas noble", "Lantánido", "Actínido")

_DATA = [
    (1, "H", "Hidrógeno", 1.008, NM), (2, "He", "Helio", 4.0026, GN),
    (3, "Li", "Litio", 6.94, AM), (4, "Be", "Berilio", 9.0122, AT),
    (5, "B", "Boro", 10.81, SM), (6, "C", "Carbono", 12.011, NM),
    (7, "N", "Nitrógeno", 14.007, NM), (8, "O", "Oxígeno", 15.999, NM),
    (9, "F", "Flúor", 18.998, HA), (10, "Ne", "Neón", 20.180, GN),
    (11, "Na", "Sodio", 22.990, AM), (12, "Mg", "Magnesio", 24.305, AT),
    (13, "Al", "Aluminio", 26.982, MP), (14, "Si", "Silicio", 28.085, SM),
    (15, "P", "Fósforo", 30.974, NM), (16, "S", "Azufre", 32.06, NM),
    (17, "Cl", "Cloro", 35.45, HA), (18, "Ar", "Argón", 39.948, GN),
    (19, "K", "Potasio", 39.098, AM), (20, "Ca", "Calcio", 40.078, AT),
    (21, "Sc", "Escandio", 44.956, MT), (22, "Ti", "Titanio", 47.867, MT),
    (23, "V", "Vanadio", 50.942, MT), (24, "Cr", "Cromo", 51.996, MT),
    (25, "Mn", "Manganeso", 54.938, MT), (26, "Fe", "Hierro", 55.845, MT),
    (27, "Co", "Cobalto", 58.933, MT), (28, "Ni", "Níquel", 58.693, MT),
    (29, "Cu", "Cobre", 63.546, MT), (30, "Zn", "Zinc", 65.38, MT),
    (31, "Ga", "Galio", 69.723, MP), (32, "Ge", "Germanio", 72.630, SM),
    (33, "As", "Arsénico", 74.922, SM), (34, "Se", "Selenio", 78.971, NM),
    (35, "Br", "Bromo", 79.904, HA), (36, "Kr", "Kriptón", 83.798, GN),
    (37, "Rb", "Rubidio", 85.468, AM), (38, "Sr", "Estroncio", 87.62, AT),
    (39, "Y", "Itrio", 88.906, MT), (40, "Zr", "Circonio", 91.224, MT),
    (41, "Nb", "Niobio", 92.906, MT), (42, "Mo", "Molibdeno", 95.95, MT),
    (43, "Tc", "Tecnecio", 98.0, MT), (44, "Ru", "Rutenio", 101.07, MT),
    (45, "Rh", "Rodio", 102.91, MT), (46, "Pd", "Paladio", 106.42, MT),
    (47, "Ag", "Plata", 107.87, MT), (48, "Cd", "Cadmio", 112.41, MT),
    (49, "In", "Indio", 114.82, MP), (50, "Sn", "Estaño", 118.71, MP),
    (51, "Sb", "Antimonio", 121.76, SM), (52, "Te", "Telurio", 127.60, SM),
    (53, "I", "Yodo", 126.90, HA), (54, "Xe", "Xenón", 131.29, GN),
    (55, "Cs", "Cesio", 132.91, AM), (56, "Ba", "Bario", 137.33, AT),
    (57, "La", "Lantano", 138.91, LA), (58, "Ce", "Cerio", 140.12, LA),
    (59, "Pr", "Praseodimio", 140.91, LA), (60, "Nd", "Neodimio", 144.24, LA),
    (61, "Pm", "Prometio", 145.0, LA), (62, "Sm", "Samario", 150.36, LA),
    (63, "Eu", "Europio", 151.96, LA), (64, "Gd", "Gadolinio", 157.25, LA),
    (65, "Tb", "Terbio", 158.93, LA), (66, "Dy", "Disprosio", 162.50, LA),
    (67, "Ho", "Holmio", 164.93, LA), (68, "Er", "Erbio", 167.26, LA),
    (69, "Tm", "Tulio", 168.93, LA), (70, "Yb", "Iterbio", 173.05, LA),
    (71, "Lu", "Lutecio", 174.97, LA), (72, "Hf", "Hafnio", 178.49, MT),
    (73, "Ta", "Tántalo", 180.95, MT), (74, "W", "Wolframio", 183.84, MT),
    (75, "Re", "Renio", 186.21, MT), (76, "Os", "Osmio", 190.23, MT),
    (77, "Ir", "Iridio", 192.22, MT), (78, "Pt", "Platino", 195.08, MT),
    (79, "Au", "Oro", 196.97, MT), (80, "Hg", "Mercurio", 200.59, MT),
    (81, "Tl", "Talio", 204.38, MP), (82, "Pb", "Plomo", 207.2, MP),
    (83, "Bi", "Bismuto", 208.98, MP), (84, "Po", "Polonio", 209.0, MP),
    (85, "At", "Astato", 210.0, HA), (86, "Rn", "Radón", 222.0, GN),
    (87, "Fr", "Francio", 223.0, AM), (88, "Ra", "Radio", 226.0, AT),
    (89, "Ac", "Actinio", 227.0, AC), (90, "Th", "Torio", 232.04, AC),
    (91, "Pa", "Protactinio", 231.04, AC), (92, "U", "Uranio", 238.03, AC),
    (93, "Np", "Neptunio", 237.0, AC), (94, "Pu", "Plutonio", 244.0, AC),
    (95, "Am", "Americio", 243.0, AC), (96, "Cm", "Curio", 247.0, AC),
    (97, "Bk", "Berkelio", 247.0, AC), (98, "Cf", "Californio", 251.0, AC),
    (99, "Es", "Einstenio", 252.0, AC), (100, "Fm", "Fermio", 257.0, AC),
    (101, "Md", "Mendelevio", 258.0, AC), (102, "No", "Nobelio", 259.0, AC),
    (103, "Lr", "Lawrencio", 266.0, AC), (104, "Rf", "Rutherfordio", 267.0, MT),
    (105, "Db", "Dubnio", 268.0, MT), (106, "Sg", "Seaborgio", 269.0, MT),
    (107, "Bh", "Bohrio", 270.0, MT), (108, "Hs", "Hassio", 277.0, MT),
    (109, "Mt", "Meitnerio", 278.0, MT), (110, "Ds", "Darmstatio", 281.0, MT),
    (111, "Rg", "Roentgenio", 282.0, MT), (112, "Cn", "Copernicio", 285.0, MT),
    (113, "Nh", "Nihonio", 286.0, MP), (114, "Fl", "Flerovio", 289.0, MP),
    (115, "Mc", "Moscovio", 290.0, MP), (116, "Lv", "Livermorio", 293.0, MP),
    (117, "Ts", "Teneso", 294.0, HA), (118, "Og", "Oganesón", 294.0, GN),
]

ELEMENTS: list[Element] = [Element(*row) for row in _DATA]
BY_SYMBOL: dict[str, Element] = {e.symbol: e for e in ELEMENTS}

_SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_TOKEN = re.compile(r"([A-Z][a-z]?)|(\d+)|([(\[{])|([)\]}])|(\S)")


def parse_formula(formula: str) -> dict[str, int]:
    """Cuenta los átomos de una fórmula química.

    Admite paréntesis/corchetes anidados, subíndices Unicode e hidratos con
    «·», «*» o «.» (p. ej. «CuSO4·5H2O»).
    """
    text = formula.strip().translate(_SUB).replace(" ", "")
    if not text:
        raise CalcError("Escribe una fórmula, p. ej. H2SO4")
    total: dict[str, int] = {}
    for part in re.split(r"[·*•.]", text):
        if not part:
            raise CalcError("Fórmula mal escrita alrededor de «·».")
        m = re.match(r"^(\d+)(.*)$", part)
        mult, body = (int(m.group(1)), m.group(2)) if m else (1, part)
        for sym, n in _parse_group(body).items():
            total[sym] = total.get(sym, 0) + n * mult
    return total


def _parse_group(text: str) -> dict[str, int]:
    stack: list[dict[str, int]] = [{}]
    last: dict[str, int] | str | None = None
    pos = 0
    for m in _TOKEN.finditer(text):
        if m.start() != pos:
            raise CalcError("Fórmula no válida.")
        pos = m.end()
        sym, num, opn, cls, bad = m.groups()
        if sym:
            if sym not in BY_SYMBOL:
                raise CalcError(f"«{sym}» no es un elemento químico.")
            stack[-1][sym] = stack[-1].get(sym, 0) + 1
            last = sym
        elif num:
            n = int(num)
            if last is None or n == 0:
                raise CalcError("Número fuera de lugar en la fórmula.")
            if isinstance(last, str):
                stack[-1][last] += n - 1
            else:
                for k, v in last.items():
                    stack[-1][k] = stack[-1].get(k, 0) + v * (n - 1)
            last = None
        elif opn:
            stack.append({})
            last = None
        elif cls:
            if len(stack) == 1:
                raise CalcError("Paréntesis sin abrir.")
            group = stack.pop()
            for k, v in group.items():
                stack[-1][k] = stack[-1].get(k, 0) + v
            last = group
        else:
            raise CalcError(f"Carácter no válido: «{bad}». Recuerda las mayúsculas (Co ≠ CO).")
    if len(stack) != 1:
        raise CalcError("Falta cerrar un paréntesis.")
    if not stack[0]:
        raise CalcError("La fórmula no contiene elementos.")
    return stack[0]


@dataclass
class MolarMass:
    formula: str
    atoms: dict[str, int]
    mass: float
    composition: list[tuple[Element, int, float, float]]  # elemento, nº, masa, %


def molar_mass(formula: str) -> MolarMass:
    atoms = parse_formula(formula)
    total = sum(BY_SYMBOL[s].mass * n for s, n in atoms.items())
    comp = [(BY_SYMBOL[s], n, BY_SYMBOL[s].mass * n, 100 * BY_SYMBOL[s].mass * n / total)
            for s, n in atoms.items()]
    return MolarMass(formula, atoms, total, comp)


def pretty_formula(formula: str) -> str:
    """H2SO4 -> H₂SO₄ (los coeficientes de hidratos se dejan normales)."""
    out, prev = [], ""
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    for ch in formula.replace("*", "·"):
        if ch.isdigit() and prev and (prev.isalpha() or prev in ")]}" or prev in "₀₁₂₃₄₅₆₇₈₉"):
            ch = ch.translate(sub)
        out.append(ch)
        prev = ch
    return "".join(out)


def find_elements(query: str) -> list[Element]:
    q = _norm(query)
    if not q:
        return list(ELEMENTS)
    if q.isdigit():
        return [e for e in ELEMENTS if str(e.z) == q]
    exact = [e for e in ELEMENTS if e.symbol.lower() == q]
    rest = [e for e in ELEMENTS if e not in exact and
            (_norm(e.name).startswith(q) or q in _norm(e.group))]
    return exact + rest


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# --------------------------------------------------- Estequiometría básica
AVOGADRO = 6.02214076e23


def grams_to_moles(grams: float, molar: float) -> float:
    if molar <= 0:
        raise CalcError("La masa molar debe ser positiva.")
    return grams / molar

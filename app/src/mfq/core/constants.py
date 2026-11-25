"""Constantes físicas y químicas de referencia (CODATA 2018 / valores exactos SI)."""

from __future__ import annotations

# (nombre, símbolo, valor, unidad)
CONSTANTS: list[tuple[str, str, float, str]] = [
    ("Velocidad de la luz en el vacío", "c", 299_792_458.0, "m/s"),
    ("Constante de gravitación universal", "G", 6.67430e-11, "N·m²/kg²"),
    ("Aceleración de la gravedad estándar", "g", 9.80665, "m/s²"),
    ("Constante de Planck", "h", 6.62607015e-34, "J·s"),
    ("Carga elemental", "e", 1.602176634e-19, "C"),
    ("Masa del electrón", "mₑ", 9.1093837015e-31, "kg"),
    ("Masa del protón", "mₚ", 1.67262192369e-27, "kg"),
    ("Masa del neutrón", "mₙ", 1.67492749804e-27, "kg"),
    ("Constante de Coulomb", "k", 8.9875517923e9, "N·m²/C²"),
    ("Permitividad del vacío", "ε₀", 8.8541878128e-12, "F/m"),
    ("Permeabilidad del vacío", "μ₀", 1.25663706212e-6, "N/A²"),
    ("Número de Avogadro", "Nₐ", 6.02214076e23, "mol⁻¹"),
    ("Constante de los gases ideales", "R", 8.314462618, "J/(mol·K)"),
    ("Constante de los gases (atm·L)", "R", 0.082057366, "atm·L/(mol·K)"),
    ("Constante de Boltzmann", "k_B", 1.380649e-23, "J/K"),
    ("Constante de Stefan-Boltzmann", "σ", 5.670374419e-8, "W/(m²·K⁴)"),
    ("Unidad de masa atómica", "u", 1.66053906660e-27, "kg"),
    ("Volumen molar (0 °C, 1 atm)", "Vₘ", 22.413969, "L/mol"),
    ("Atmósfera estándar", "atm", 101325.0, "Pa"),
    ("Cero absoluto", "0 K", -273.15, "°C"),
    ("Velocidad del sonido (aire, 20 °C)", "v_s", 343.0, "m/s"),
    ("Masa de la Tierra", "M_T", 5.972e24, "kg"),
    ("Radio medio de la Tierra", "R_T", 6.371e6, "m"),
    ("Masa del Sol", "M_☉", 1.989e30, "kg"),
    ("Masa de la Luna", "M_L", 7.342e22, "kg"),
    ("Distancia Tierra-Sol (1 UA)", "UA", 1.495978707e11, "m"),
    ("Año luz", "al", 9.4607304725808e15, "m"),
]

"""Gráfica de funciones dibujada con el Canvas de Flet (sin dependencias extra)."""

from __future__ import annotations

import math

import flet as ft
import flet.canvas as cv

from ..core.numbers import fmt

PALETTE = ["#3B6FE0", "#E0563B", "#1E9E6A", "#9B4DCA"]


def _nice_step(span: float, target: int = 6) -> float:
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def build_plot(series: list[list[tuple[float, float | None]]], width: float = 340,
               height: float = 300, dark: bool = False) -> ft.Control:
    xs = [x for s in series for x, _ in s]
    ys = [y for s in series for _, y in s if y is not None]
    if not xs or not ys:
        return ft.Text("La función no está definida en ese intervalo.")
    x_min, x_max = min(xs), max(xs)
    # recorta valores extremos (asíntotas) usando percentiles
    ys_sorted = sorted(ys)
    lo, hi = ys_sorted[0], ys_sorted[-1]
    if len(ys_sorted) > 50:
        p_lo = ys_sorted[int(len(ys_sorted) * 0.02)]
        p_hi = ys_sorted[int(len(ys_sorted) * 0.98) - 1]
        if (hi - lo) > 10 * max(p_hi - p_lo, 1e-9):  # hay asíntotas: ignora los extremos
            lo, hi = p_lo, p_hi
    if hi - lo < 1e-9:
        lo, hi = lo - 1, hi + 1
    pad = (hi - lo) * 0.08
    y_min, y_max = lo - pad, hi + pad

    ml, mb, mt, mr = 44, 24, 8, 8
    pw, ph = width - ml - mr, height - mt - mb

    def px(x):
        return ml + (x - x_min) / (x_max - x_min) * pw

    def py(y):
        return mt + (y_max - y) / (y_max - y_min) * ph

    grid_c = "#33FFFFFF" if dark else "#22000000"
    axis_c = "#AAFFFFFF" if dark else "#99000000"
    text_c = "#CCFFFFFF" if dark else "#99000000"
    grid = ft.Paint(color=grid_c, stroke_width=1)
    axis = ft.Paint(color=axis_c, stroke_width=1.5)
    label_style = ft.TextStyle(size=10, color=text_c)
    shapes: list[cv.Shape] = []

    sx = _nice_step(x_max - x_min)
    x = math.ceil(x_min / sx) * sx
    while x <= x_max + 1e-12:
        shapes.append(cv.Line(px(x), mt, px(x), mt + ph, grid))
        shapes.append(cv.Text(px(x), mt + ph + 4, fmt(round(x, 10), 3), style=label_style,
                              alignment=ft.Alignment.TOP_CENTER))
        x += sx
    sy = _nice_step(y_max - y_min)
    y = math.ceil(y_min / sy) * sy
    while y <= y_max + 1e-12:
        shapes.append(cv.Line(ml, py(y), ml + pw, py(y), grid))
        shapes.append(cv.Text(ml - 4, py(y), fmt(round(y, 10), 3), style=label_style,
                              alignment=ft.Alignment.CENTER_RIGHT))
        y += sy
    if x_min <= 0 <= x_max:
        shapes.append(cv.Line(px(0), mt, px(0), mt + ph, axis))
    if y_min <= 0 <= y_max:
        shapes.append(cv.Line(ml, py(0), ml + pw, py(0), axis))

    for i, s in enumerate(series):
        elements: list[cv.Path.PathElement] = []
        pen_down = False
        prev_y = None
        for x, y in s:
            if y is None or not (y_min - (y_max - y_min) * 2 <= y <= y_max + (y_max - y_min) * 2):
                pen_down = False
                prev_y = None
                continue
            # corta el trazo en saltos bruscos (asíntotas verticales)
            if pen_down and prev_y is not None and abs(y - prev_y) > (y_max - y_min) * 1.5:
                pen_down = False
            yy = min(max(py(y), mt - 2), mt + ph + 2)
            elements.append(cv.Path.LineTo(px(x), yy) if pen_down else cv.Path.MoveTo(px(x), yy))
            pen_down, prev_y = True, y
        shapes.append(cv.Path(elements, paint=ft.Paint(
            color=PALETTE[i % len(PALETTE)], stroke_width=2.5,
            style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND,
            stroke_join=ft.StrokeJoin.ROUND)))

    return ft.Container(cv.Canvas(shapes, width=width, height=height),
                        border_radius=12, clip_behavior=ft.ClipBehavior.HARD_EDGE)

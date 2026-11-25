"""Pantallas adicionales de Matemáticas."""

from __future__ import annotations

import flet as ft

from ..core import maths_extra as mx
from ..core.numbers import CalcError, fmt, parse_number
from .context import Ctx
from .widgets import ResultPanel, card, info_text, number_field, push_page


# ------------------------------------------------------------- Calculadora
def open_calculator(ctx: Ctx) -> None:
    page = ctx.page
    display = ft.TextField(value="", text_size=26, text_align=ft.TextAlign.RIGHT,
                           border_radius=12, autofocus=False, hint_text="0",
                           keyboard_type=ft.KeyboardType.TEXT)
    preview = ft.Text("", size=18, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.RIGHT)
    mode = ft.SegmentedButton(
        segments=[ft.Segment(value="deg", label=ft.Text("DEG")),
                  ft.Segment(value="rad", label=ft.Text("RAD"))],
        selected=["deg"], show_selected_icon=False)
    tape = ft.Column(spacing=2)
    state = {"ans": 0.0, "fresh": False}  # fresh: se acaba de pulsar «=»

    def degrees() -> bool:
        return "deg" in (mode.selected or [])

    def live(_e=None) -> None:
        expr = _expand_ans(display.value or "", state["ans"])
        try:
            preview.value = "= " + fmt(mx.evaluate(expr, degrees())) if expr.strip() else ""
        except CalcError:
            preview.value = ""
        page.update()

    def press(token: str) -> None:
        v = display.value or ""
        if token == "C":
            display.value = ""
        elif token == "⌫":
            display.value = v[:-1]
        elif token == "=":
            equals()
            return
        else:
            if state["fresh"] and token not in ("+", "−", "×", "÷", "^"):
                v = ""  # tras «=», un número o función empieza una operación nueva
            display.value = v + token
        state["fresh"] = False
        live()

    def equals(_e=None) -> None:
        expr = display.value or ""
        if not expr.strip():
            return
        try:
            value = mx.evaluate(_expand_ans(expr, state["ans"]), degrees())
        except CalcError as exc:
            preview.value = str(exc)
            page.update()
            return
        state["ans"] = value
        tape.controls.insert(0, ft.Text(f"{expr} = {fmt(value)}", selectable=True,
                                        color=ft.Colors.ON_SURFACE_VARIANT))
        del tape.controls[8:]
        ctx.history.add("Calculadora", expr, fmt(value))
        display.value = fmt(value).replace("×10^", "e").replace("−", "-")
        preview.value = ""
        state["fresh"] = True
        page.update()

    def on_type(_e=None) -> None:
        state["fresh"] = False
        live()

    display.on_change = on_type
    display.on_submit = equals
    mode.on_change = live

    keys = [
        ["sin(", "cos(", "tan(", "√(", "^"],
        ["ln(", "log(", "(", ")", "π"],
        ["7", "8", "9", "÷", "⌫"],
        ["4", "5", "6", "×", "C"],
        ["1", "2", "3", "−", "Ans"],
        ["0", ".", "e", "+", "="],
    ]

    def key(t: str) -> ft.Control:
        label = t[:-1] if t.endswith("(") and len(t) > 1 else t
        primary = t == "="
        style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14),
                               padding=ft.Padding.all(0))
        btn_cls = ft.FilledButton if primary else (
            ft.FilledTonalButton if t in "÷×−+^⌫C" or t.endswith("(") or t in ("π", "Ans") else ft.OutlinedButton)
        if t == "⌫":
            return ft.Container(ft.FilledTonalButton(
                content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, size=20), on_click=lambda e: press(t),
                style=style, height=52, tooltip="Borrar"), expand=True)
        return ft.Container(btn_cls(label, on_click=lambda e: press(t), style=style, height=52),
                            expand=True)

    pad = ft.Column([ft.Row([key(t) for t in row], spacing=6) for row in keys], spacing=6)
    push_page(page, "Calculadora científica", [
        mode, display, preview, pad,
        info_text("También puedes escribir directamente: 2(3+4)^2, √2, 6.02e23, sin(30)…"),
        tape,
    ])


def _expand_ans(expr: str, ans: float) -> str:
    return expr.replace("Ans", f"({ans!r})")


# --------------------------------------------------------------- Estadística
def open_statistics(ctx: Ctx) -> None:
    page = ctx.page
    data = ft.TextField(label="Datos (separados por espacios o «;»)",
                        value="4 8 15 16 23 42", multiline=True, border_radius=12)
    result = ResultPanel()
    table = ft.Column(spacing=4)
    bars = ft.Column(spacing=2)

    def calc(_e=None) -> None:
        try:
            values = mx.parse_data(data.value or "")
            s = mx.describe(values)
        except CalcError as exc:
            result.error(str(exc))
            table.controls, bars.controls = [], []
            page.update()
            return
        result.show_value(f"Media = {fmt(s.mean)}", f"n = {s.n} datos · σ = {fmt(s.std_pop)}")
        rows = [
            ("Suma", fmt(s.total)), ("Media", fmt(s.mean)), ("Mediana", fmt(s.median)),
            ("Moda", ", ".join(fmt(m) for m in s.modes) if s.modes else "No hay (todos distintos)"),
            ("Mínimo", fmt(s.minimum)), ("Máximo", fmt(s.maximum)), ("Rango", fmt(s.rng)),
            ("Cuartiles Q1 / Q3", f"{fmt(s.q1)} / {fmt(s.q3)}"),
            ("Varianza (población)", fmt(s.var_pop)), ("Desv. típica (población) σ", fmt(s.std_pop)),
            ("Varianza (muestra)", fmt(s.var_sample) if s.var_sample is not None else "—"),
            ("Desv. típica (muestra) s", fmt(s.std_sample) if s.std_sample is not None else "—"),
        ]
        table.controls = [ft.Row([ft.Text(k, expand=True, color=ft.Colors.ON_SURFACE_VARIANT),
                                  ft.Text(v, selectable=True, weight=ft.FontWeight.W_500)])
                          for k, v in rows]
        # tabla de frecuencias (si hay pocos valores distintos)
        freq: dict[float, int] = {}
        for v in values:
            freq[v] = freq.get(v, 0) + 1
        if len(freq) <= 15 and max(freq.values()) > 1:
            top = max(freq.values())
            bars.controls = [ft.Text("Frecuencias", weight=ft.FontWeight.W_600)] + [
                ft.Row([ft.Text(fmt(k), width=70), ft.ProgressBar(value=c / top, expand=True),
                        ft.Text(str(c), width=30)]) for k, c in sorted(freq.items())]
        else:
            bars.controls = []
        ctx.history.add("Estadística", f"n = {s.n}", f"media {fmt(s.mean)}, σ {fmt(s.std_pop)}")
        page.update()

    data.on_submit = calc
    calc()
    push_page(page, "Estadística", [
        data, ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calc),
        result, card(table), bars])


# --------------------------------------------------------- Sistemas lineales
def open_systems(ctx: Ctx) -> None:
    page = ctx.page
    size = ft.SegmentedButton(segments=[ft.Segment(value="2", label=ft.Text("2 × 2")),
                                        ft.Segment(value="3", label=ft.Text("3 × 3"))],
                              selected=["2"], show_selected_icon=False)
    grid = ft.Column(spacing=8)
    result = ResultPanel()
    cells: list[list[ft.TextField]] = []
    names = ["x", "y", "z"]
    defaults = {2: [["2", "1", "5"], ["1", "-1", "1"]],
                3: [["1", "1", "1", "6"], ["2", "-1", "1", "3"], ["1", "2", "-1", "2"]]}

    def build(_e=None) -> None:
        n = int((size.selected or ["2"])[0])
        cells.clear()
        grid.controls = []
        for r in range(n):
            row_fields = []
            row: list[ft.Control] = []
            for c in range(n + 1):
                f = ft.TextField(value=defaults[n][r][c], dense=True, text_align=ft.TextAlign.CENTER,
                                 keyboard_type=ft.KeyboardType.NUMBER, border_radius=10,
                                 on_submit=solve)
                row_fields.append(f)
                row.append(ft.Container(f, expand=True))
                if c < n - 1:
                    row.append(ft.Text(f"{names[c]} +"))
                elif c == n - 1:
                    row.append(ft.Text(f"{names[c]} ="))
            cells.append(row_fields)
            grid.controls.append(ft.Row(row, spacing=4))
        result.reset()
        page.update()

    def solve(_e=None) -> None:
        n = len(cells)
        try:
            vals = [[parse_number(f.value, "coeficiente") for f in row] for row in cells]
            sol = mx.solve_linear([r[:n] for r in vals], [r[n] for r in vals])
        except CalcError as exc:
            result.error(str(exc))
        else:
            text = "   ".join(f"{names[i]} = {fmt(v)}" for i, v in enumerate(sol))
            result.show_value(text, "Sistema compatible determinado (solución única)")
            ctx.history.add(f"Sistema {n}×{n}", "; ".join(
                " ".join(f.value for f in row) for row in cells), text)
        page.update()

    size.on_change = build
    build()
    push_page(page, "Sistemas de ecuaciones", [
        size, grid, ft.FilledButton("Resolver", icon=ft.Icons.CALCULATE, on_click=solve), result,
        info_text("Método de Gauss. Detecta sistemas sin solución o con infinitas soluciones."),
    ])


# ---------------------------------------------------------------- Triángulos
def open_triangle(ctx: Ctx) -> None:
    page = ctx.page
    fields = {k: number_field(label, unit, "") for k, label, unit in [
        ("a", "Lado a", ""), ("b", "Lado b", ""), ("c", "Lado c", ""),
        ("A", "Ángulo A", "°"), ("B", "Ángulo B", "°"), ("C", "Ángulo C", "°")]}
    fields["a"].value, fields["b"].value, fields["c"].value = "3", "4", "5"
    result = ResultPanel()
    extra = ft.Column(spacing=4)

    def solve(_e=None) -> None:
        try:
            given = {k: parse_number(f.value, k) for k, f in fields.items() if (f.value or "").strip()}
            sols = mx.solve_triangle(**given)
        except CalcError as exc:
            result.error(str(exc))
            extra.controls = []
            page.update()
            return
        t = sols[0]
        result.show_value(
            f"a = {fmt(t.a)}  b = {fmt(t.b)}  c = {fmt(t.c)}",
            f"A = {fmt(t.A)}°  B = {fmt(t.B)}°  C = {fmt(t.C)}°\n"
            f"Área = {fmt(t.area)}   Perímetro = {fmt(t.perimeter)}\nTriángulo {t.kind}")
        extra.controls = []
        if len(sols) == 2:
            t2 = sols[1]
            extra.controls = [card(
                ft.Text("Caso ambiguo: hay una segunda solución", weight=ft.FontWeight.W_600),
                ft.Text(f"a = {fmt(t2.a)}  b = {fmt(t2.b)}  c = {fmt(t2.c)}"),
                ft.Text(f"A = {fmt(t2.A)}°  B = {fmt(t2.B)}°  C = {fmt(t2.C)}°"),
                ft.Text(f"Área = {fmt(t2.area)}"))]
        ctx.history.add("Triángulo", ", ".join(f"{k}={f.value}" for k, f in fields.items()
                                                if (f.value or "").strip()),
                        f"Área {fmt(t.area)}")
        page.update()

    def clear(_e) -> None:
        for f in fields.values():
            f.value = ""
        result.reset()
        extra.controls = []
        page.update()

    for f in fields.values():
        f.on_submit = solve
    push_page(page, "Resolver triángulos", [
        card(ft.Text("Escribe 3 datos (al menos un lado). El ángulo A es el opuesto al lado a.",
                     size=13)),
        ft.Row([ft.Container(fields[k], expand=True) for k in "abc"]),
        ft.Row([ft.Container(fields[k], expand=True) for k in "ABC"]),
        ft.Row([ft.FilledButton("Resolver", icon=ft.Icons.CALCULATE, on_click=solve, expand=True),
                ft.OutlinedButton("Limpiar", icon=ft.Icons.CLEAR, on_click=clear)]),
        result, extra,
        info_text("Usa el teorema del seno y del coseno. Sirve para LLL, LAL, ALA, LAA y LLA."),
    ])


# ---------------------------------------------------------------- Fracciones
def open_fractions(ctx: Ctx) -> None:
    page = ctx.page
    a = ft.TextField(label="Fracción 1", value="3/4", dense=True, border_radius=12, expand=True)
    b = ft.TextField(label="Fracción 2", value="5/6", dense=True, border_radius=12, expand=True)
    op = ft.Dropdown(value="+", width=80, options=[ft.DropdownOption(o) for o in "+−×÷"])
    result = ResultPanel()
    simp = ft.TextField(label="Simplificar / pasar a fracción", value="0.375",
                        dense=True, border_radius=12)
    simp_out = ft.Text("", selectable=True, size=16)

    def calc(_e=None) -> None:
        try:
            r = mx.fraction_op(a.value, op.value, b.value)
        except CalcError as exc:
            result.error(str(exc))
        else:
            main = str(r)
            detail = f"Decimal: {fmt(float(r))}"
            if r.denominator != 1 and abs(r) > 1:
                detail += f"\nNúmero mixto: {mx.mixed(r)}"
            result.show_value(main, detail)
            ctx.history.add("Fracciones", f"{a.value} {op.value} {b.value}", main)
        page.update()

    def simplify(_e=None) -> None:
        try:
            f = mx.parse_fraction(simp.value)
            simp_out.value = f"= {f}" + (f"  ({mx.mixed(f)})" if abs(f) > 1 and f.denominator != 1 else "")
        except CalcError as exc:
            simp_out.value = str(exc)
        page.update()

    for f in (a, b):
        f.on_submit = calc
    op.on_select = calc
    simp.on_change = simplify
    calc()
    simplify()
    push_page(page, "Fracciones", [
        ft.Row([a, op, b], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calc),
        result,
        card(ft.Text("Simplificar", weight=ft.FontWeight.W_600), simp, simp_out,
             info_text("Escribe 12/18, 0.375 o 2.5 y obtendrás la fracción irreducible.")),
    ])


# ------------------------------------------------- Porcentajes y regla de 3
def open_percent(ctx: Ctx) -> None:
    page = ctx.page

    def block(title: str, labels: list[str], defaults: list[str], fn, fmt_out) -> ft.Control:
        fs = [number_field(l, value=d) for l, d in zip(labels, defaults)]
        out = ft.Text("", size=18, weight=ft.FontWeight.W_600, selectable=True)

        def run(_e=None) -> None:
            try:
                vals = [parse_number(f.value, l) for f, l in zip(fs, labels)]
                out.value = fmt_out(fn(*vals), vals)
                out.color = None
            except CalcError as exc:
                out.value, out.color = str(exc), ft.Colors.ERROR
            try:
                page.update()
            except RuntimeError:
                pass

        for f in fs:
            f.on_change = run
        run()
        return card(ft.Text(title, weight=ft.FontWeight.W_600),
                    ft.Row([ft.Container(f, expand=True) for f in fs]), out)

    push_page(page, "Porcentajes y regla de tres", [
        block("¿Cuánto es el p % de N?", ["p (%)", "N"], ["21", "150"], mx.percent_of,
              lambda r, v: f"{fmt(v[0])} % de {fmt(v[1])} = {fmt(r)}"),
        block("¿Qué % es A de B?", ["A", "B"], ["30", "120"], mx.what_percent,
              lambda r, v: f"{fmt(v[0])} es el {fmt(r)} % de {fmt(v[1])}"),
        block("Aumento / descuento", ["Inicial", "Final"], ["80", "60"], mx.percent_change,
              lambda r, v: f"{'Aumento' if r >= 0 else 'Descuento'} del {fmt(abs(r))} %"),
        block("Precio con descuento", ["Precio", "Descuento (%)"], ["49.99", "20"],
              lambda p, d: p * (1 - d / 100),
              lambda r, v: f"Pagas {r:.2f}  (ahorras {v[0] - r:.2f})"),
        block("Regla de tres directa: si A → B, entonces C → x", ["A", "B", "C"], ["3", "4.5", "10"],
              mx.rule_of_three, lambda r, v: f"x = {fmt(r)}"),
        block("Regla de tres inversa: si A → B, entonces C → x", ["A", "B", "C"], ["4", "6", "3"],
              lambda a, b, c: mx.rule_of_three(a, b, c, inverse=True), lambda r, v: f"x = {fmt(r)}"),
    ])

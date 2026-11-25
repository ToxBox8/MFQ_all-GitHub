"""Pantallas de Matemáticas."""

from __future__ import annotations

from typing import Callable

import flet as ft

from ..core import maths
from ..core.numbers import CalcError, fmt, parse_number
from .history import History
from .plot import PALETTE, build_plot
from .widgets import ResultPanel, card, number_field, push_page


class MathsTab(ft.Column):
    def __init__(self, page: ft.Page, history: History) -> None:
        self._page = page
        self.history = history
        tools: list[tuple[str, str, ft.IconData, Callable]] = [
            ("Ecuación de 2º grado", "ax² + bx + c = 0, reales y complejas", ft.Icons.FUNCTIONS, self.quadratic),
            ("Representar funciones", "Dibuja hasta 3 funciones a la vez", ft.Icons.SHOW_CHART, self.plotter),
            ("MCD, MCM y factores primos", "De varios números enteros", ft.Icons.TAG, self.gcd_lcm),
            ("Binario y bases", "Texto a binario y cambio de base", ft.Icons.DATA_OBJECT, self.binary),
            ("Círculo", "Área, perímetro y diámetro", ft.Icons.CIRCLE_OUTLINED, self.circle),
            ("Calcular π", "Hasta 5000 decimales exactos", ft.Icons.PIE_CHART, self.pi),
            ("Dados", "Lanza dados de cualquier número de caras", ft.Icons.CASINO, self.dice),
        ]
        grid = ft.ResponsiveRow(
            [ft.Container(
                ft.Card(ft.ListTile(
                    leading=ft.Icon(icon, color=ft.Colors.PRIMARY),
                    title=ft.Text(title, weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(sub, size=12),
                    on_click=lambda e, fn=fn: fn(),
                ), variant=ft.CardVariant.OUTLINED),
                col={"xs": 12, "md": 6})
             for title, sub, icon, fn in tools],
            spacing=8, run_spacing=4,
        )
        super().__init__([ft.Container(grid, padding=12)], expand=True,
                         scroll=ft.ScrollMode.AUTO)

    # ------------------------------------------------------------ 2º grado
    def quadratic(self) -> None:
        page = self._page
        a, b, c = (number_field(n, value=v) for n, v in (("a", "1"), ("b", "-3"), ("c", "2")))
        result = ResultPanel()
        plot_box = ft.Container()

        def solve(_e=None) -> None:
            try:
                av, bv, cv = (parse_number(f.value, n) for f, n in ((a, "a"), (b, "b"), (c, "c")))
                r = maths.solve_quadratic(av, bv, cv)
            except CalcError as exc:
                result.error(str(exc))
                page.update()
                return
            if r.roots:
                names = ["x₁", "x₂"] if len(r.roots) == 2 else ["x"]
                main = "   ".join(f"{n} = {fmt(z)}" for n, z in zip(names, r.roots))
            else:
                main = r.kind
            extra = [r.kind]
            if r.discriminant is not None:
                extra.append(f"Δ = b² − 4ac = {fmt(r.discriminant)}")
            if r.vertex:
                extra.append(f"Vértice: ({fmt(r.vertex[0])}, {fmt(r.vertex[1])})")
            result.show_value(main, "\n".join(extra))
            self.history.add("Ecuación 2º grado",
                             f"{_poly(av, bv, cv)} = 0", main)
            if av != 0 and r.vertex:
                vx = r.vertex[0]
                real = [z for z in r.roots if not isinstance(z, complex)]
                span = max(2.0, *(2.5 * abs(z - vx) for z in real)) if real else 3.0
                pts = maths.sample_function(lambda x: av * x * x + bv * x + cv, vx - span, vx + span, 200)
                plot_box.content = build_plot([pts], dark=_is_dark(page))
            else:
                plot_box.content = None
            page.update()

        for f in (a, b, c):
            f.on_submit = solve
        push_page(page, "Ecuación de segundo grado", [
            card(ft.Text("ax² + bx + c = 0", size=24, text_align=ft.TextAlign.CENTER)),
            ft.Row([ft.Container(a, expand=True), ft.Container(b, expand=True),
                    ft.Container(c, expand=True)]),
            ft.FilledButton("Resolver", icon=ft.Icons.CALCULATE, on_click=solve),
            result, plot_box,
        ])

    # ------------------------------------------------------------- gráfica
    def plotter(self) -> None:
        page = self._page
        exprs = [ft.TextField(label=f"f{i + 1}(x)", value=v, dense=True, border_radius=12,
                              prefix_icon=ft.Icons.SHOW_CHART, color=PALETTE[i])
                 for i, v in enumerate(["x^2 - 2", "sin(x)", ""])]
        x_min = number_field("x mín", value="-5")
        x_max = number_field("x máx", value="5")
        status = ft.Text("", color=ft.Colors.ERROR)
        plot_box = ft.Container(alignment=ft.Alignment.CENTER)

        def draw(_e=None) -> None:
            status.value = ""
            try:
                lo, hi = parse_number(x_min.value, "x mín"), parse_number(x_max.value, "x máx")
                series = []
                for f in exprs:
                    if f.value.strip():
                        fn = maths.compile_function(f.value)
                        series.append(maths.sample_function(fn, lo, hi, 400))
                if not series:
                    raise CalcError("Escribe al menos una función.")
            except CalcError as exc:
                status.value = str(exc)
                page.update()
                return
            width = min((page.width or 380) - 40, 680)
            plot_box.content = build_plot(series, width=width, height=width * 0.8,
                                          dark=_is_dark(page))
            self.history.add("Gráfica", "; ".join(f.value for f in exprs if f.value.strip()),
                             f"x ∈ [{fmt(lo)}, {fmt(hi)}]")
            page.update()

        for f in [*exprs, x_min, x_max]:
            f.on_submit = draw
        push_page(page, "Representar funciones", [
            *exprs,
            ft.Row([ft.Container(x_min, expand=True), ft.Container(x_max, expand=True)]),
            ft.FilledButton("Dibujar", icon=ft.Icons.SHOW_CHART, on_click=draw),
            status,
            plot_box,
            ft.Text("Admite + − * / ^, paréntesis, pi, e, sin/sen, cos, tan, sqrt/raiz, "
                    "ln, log, exp, abs. Puedes escribir «2x» o «3(x+1)».",
                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
        ])
        draw()

    # ------------------------------------------------------------ MCD/MCM
    def gcd_lcm(self) -> None:
        page = self._page
        nums = ft.TextField(label="Números enteros", value="12, 18, 24", dense=True,
                            border_radius=12, keyboard_type=ft.KeyboardType.NUMBER)
        result = ResultPanel()

        def calc(_e=None) -> None:
            try:
                values = maths.parse_int_list(nums.value)
                g, l = maths.gcd_many(values), maths.lcm_many(values)
                factors = []
                for n in values:
                    if abs(n) > 1:
                        fs = maths.prime_factors(abs(n))
                        factors.append(f"{n} = {_factor_str(fs)}")
            except CalcError as exc:
                result.error(str(exc))
            else:
                main = f"MCD = {g}   MCM = {l}"
                result.show_value(main, "\n".join(factors))
                self.history.add("MCD / MCM", nums.value, main)
            page.update()

        nums.on_submit = calc
        push_page(page, "MCD, MCM y factores primos", [
            nums, ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calc), result])

    # ------------------------------------------------------------- binario
    def binary(self) -> None:
        page = self._page
        text_in = ft.TextField(label="Texto", value="Hola", multiline=True, border_radius=12)
        bin_in = ft.TextField(label="Binario", multiline=True, border_radius=12,
                              text_style=ft.TextStyle(font_family="monospace"))
        int_in = number_field("Número entero", value="255")
        bases = ft.Column(spacing=4)
        status = ft.Text("", color=ft.Colors.ERROR)

        def to_bin(_e=None) -> None:
            bin_in.value = maths.text_to_binary(text_in.value or "")
            status.value = ""
            page.update()

        def to_text(_e=None) -> None:
            try:
                text_in.value = maths.binary_to_text(bin_in.value or "")
                status.value = ""
            except CalcError as exc:
                status.value = str(exc)
            page.update()

        def to_bases(_e=None) -> None:
            try:
                n = int(parse_number(int_in.value, "número"))
                rows = maths.int_to_bases(n)
                bases.controls = [ft.Row([ft.Text(k, width=110, color=ft.Colors.ON_SURFACE_VARIANT),
                                          ft.Text(v, selectable=True, font_family="monospace")])
                                  for k, v in rows.items()]
            except (CalcError, OverflowError) as exc:
                bases.controls = [ft.Text(str(exc), color=ft.Colors.ERROR)]
            page.update()

        int_in.on_change = to_bases
        to_bin()
        to_bases()
        push_page(page, "Binario y bases", [
            card(ft.Text("Texto y binario (UTF-8)", weight=ft.FontWeight.W_600),
                 text_in,
                 ft.Row([ft.FilledTonalButton("Texto → Binario", icon=ft.Icons.SWAP_VERT, on_click=to_bin),
                         ft.FilledTonalButton("Binario → Texto", icon=ft.Icons.SWAP_VERT, on_click=to_text)],
                        wrap=True),
                 bin_in, status),
            card(ft.Text("Cambio de base", weight=ft.FontWeight.W_600), int_in, bases),
        ])

    # -------------------------------------------------------------- círculo
    def circle(self) -> None:
        page = self._page
        r = number_field("Radio", value="1")
        result = ResultPanel()

        def calc(_e=None) -> None:
            try:
                out = maths.circle(parse_number(r.value, "radio"))
            except CalcError as exc:
                result.error(str(exc))
            else:
                main = f"A = {fmt(out['area'])}"
                result.show_value(main, f"Perímetro = {fmt(out['perimetro'])}\n"
                                        f"Diámetro = {fmt(out['diametro'])}")
                self.history.add("Círculo", f"r = {r.value}", main)
            page.update()

        r.on_submit = calc
        push_page(page, "Círculo", [
            card(ft.Text("A = π·r²     P = 2·π·r", size=20, text_align=ft.TextAlign.CENTER)),
            r, ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calc), result])

    # ------------------------------------------------------------------- pi
    def pi(self) -> None:
        page = self._page
        digits = ft.Slider(min=10, max=5000, divisions=499, value=100, label="{value}")
        out = ft.Text("", selectable=True, font_family="monospace", size=14)
        count = ft.Text("100 decimales")

        def calc(_e=None) -> None:
            n = int(digits.value)
            count.value = f"{n} decimales"
            out.value = maths.pi_digits(n)
            page.update()

        digits.on_change_end = calc
        calc()
        push_page(page, "Calcular π", [
            ft.Text("Fórmula de Machin: π = 16·arctan(1/5) − 4·arctan(1/239)",
                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            count, digits, card(out)])

    # ----------------------------------------------------------------- dados
    def dice(self) -> None:
        page = self._page
        count = number_field("Número de dados", value="2")
        faces = number_field("Caras", value="6")
        faces_row = ft.Row([ft.Chip(label=ft.Text(f"d{n}"),
                                    on_click=lambda e, n=n: _set(faces, str(n), page))
                            for n in (4, 6, 8, 10, 12, 20)], wrap=True)
        result = ResultPanel()

        def roll(_e=None) -> None:
            try:
                rolls = maths.roll_dice(int(parse_number(count.value, "número de dados")),
                                        int(parse_number(faces.value, "caras")))
            except CalcError as exc:
                result.error(str(exc))
            else:
                main = "  ".join(str(r) for r in rolls) if len(rolls) <= 12 else f"Total {sum(rolls)}"
                result.show_value(main, f"Suma: {sum(rolls)}   Media: {fmt(sum(rolls) / len(rolls), 4)}")
                self.history.add("Dados", f"{len(rolls)}d{faces.value}", f"Suma {sum(rolls)}")
            page.update()

        push_page(page, "Dados", [
            ft.Row([ft.Container(count, expand=True), ft.Container(faces, expand=True)]),
            faces_row,
            ft.FilledButton("Lanzar", icon=ft.Icons.CASINO, on_click=roll),
            result])


def _poly(a: float, b: float, c: float) -> str:
    """Formatea a·x² + b·x + c de forma natural: «x² − 3x + 2»."""
    out = ""
    for coef, var in ((a, "x²"), (b, "x"), (c, "")):
        if coef == 0:
            continue
        mag = abs(coef)
        body = var if (mag == 1 and var) else f"{fmt(mag)}{var}"
        if not out:
            out = ("−" if coef < 0 else "") + body
        else:
            out += (" − " if coef < 0 else " + ") + body
    return out or "0"


def _factor_str(fs: list[int]) -> str:
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    parts = []
    for p in sorted(set(fs)):
        k = fs.count(p)
        parts.append(f"{p}{str(k).translate(sup)}" if k > 1 else str(p))
    return " · ".join(parts)


def _set(field: ft.TextField, value: str, page: ft.Page) -> None:
    field.value = value
    page.update()


def _is_dark(page: ft.Page) -> bool:
    if page.theme_mode == ft.ThemeMode.DARK:
        return True
    if page.theme_mode == ft.ThemeMode.LIGHT:
        return False
    return page.platform_brightness == ft.Brightness.DARK

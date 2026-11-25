"""Pantallas de Física: buscador, favoritos, calculadora de fórmulas, conversor y constantes."""

from __future__ import annotations

import flet as ft

from ..core import physics, units
from ..core.constants import CONSTANTS
from ..core.numbers import CalcError, fmt, parse_number
from .context import Ctx
from .widgets import (CATEGORY_ICONS, ResultPanel, card, copy_to_clipboard, info_text,
                      nav_tile, number_field, pretty, push_page, section_title, toast)


class PhysicsTab(ft.Column):
    def __init__(self, ctx: Ctx) -> None:
        self.ctx = ctx
        self.query = ""
        self.search = ft.TextField(
            hint_text="Buscar fórmula…",
            prefix_icon=ft.Icons.SEARCH, border_radius=28, dense=True, filled=True,
            on_change=self._on_search,
        )
        self.list = ft.Column(spacing=0)
        super().__init__(
            [ft.Container(self.search, padding=ft.Padding.symmetric(horizontal=16, vertical=8)),
             self.list],
            spacing=0, expand=True, scroll=ft.ScrollMode.AUTO,
        )
        ctx.store.subscribe(lambda: self._render())
        self._render()

    def _on_search(self, e) -> None:
        self.query = e.control.value or ""
        self._render()

    def _tile(self, f: physics.Formula) -> ft.Control:
        fav = self.ctx.store.is_favorite(f.id)
        return ft.ListTile(
            leading=ft.Icon(CATEGORY_ICONS.get(f.category, ft.Icons.FUNCTIONS)),
            title=ft.Text(f.name),
            subtitle=ft.Text(f.equation),
            trailing=ft.Icon(ft.Icons.STAR if fav else ft.Icons.CHEVRON_RIGHT,
                             color=ft.Colors.AMBER if fav else None),
            on_click=lambda e, f=f: open_formula(self.ctx, f),
        )

    def _render(self) -> None:
        results = physics.search(self.query)
        controls: list[ft.Control] = []
        if not self.query:
            controls.append(ft.Row([
                ft.Container(_shortcut(ft.Icons.SWAP_HORIZ, "Conversor",
                                       lambda e: open_converter(self.ctx)), expand=True),
                ft.Container(_shortcut(ft.Icons.PUSH_PIN_OUTLINED, "Constantes",
                                       lambda e: open_constants(self.ctx)), expand=True),
            ], spacing=8))
            favs = [physics.FORMULAS_BY_ID[i] for i in self.ctx.store.favorites
                    if i in physics.FORMULAS_BY_ID]
            if favs:
                controls.append(section_title("★ Favoritas"))
                controls.extend(self._tile(f) for f in favs)
        current = None
        for f in results:
            if f.category != current:
                current = f.category
                controls.append(section_title(current))
            controls.append(self._tile(f))
        if not results:
            controls.append(ft.Container(
                ft.Text("No hay fórmulas que coincidan.", color=ft.Colors.ON_SURFACE_VARIANT),
                padding=24))
        self.list.controls = [ft.Container(ft.Column(controls, spacing=0),
                                           padding=ft.Padding.symmetric(horizontal=4))]
        try:
            self.update()
        except RuntimeError:  # aún no está en la página
            pass


def _shortcut(icon: ft.IconData, label: str, on_click) -> ft.Control:
    return ft.Container(
        ft.Row([ft.Icon(icon, color=ft.Colors.ON_SECONDARY_CONTAINER),
                ft.Text(label, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SECONDARY_CONTAINER)],
               alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.SECONDARY_CONTAINER, border_radius=16, padding=14,
        margin=ft.Margin.only(left=12, right=12, top=4), on_click=on_click, ink=True,
    )


def open_formula(ctx: Ctx, formula: physics.Formula) -> None:
    page = ctx.page
    syms = list(formula.solvers)
    state = {"unknown": syms[0]}
    fields: dict[str, ft.TextField] = {}
    result = ResultPanel()
    inputs_col = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    steps = ft.Column(spacing=4, visible=False)

    def build_inputs() -> None:
        old = {k: f.value for k, f in fields.items()}
        fields.clear()
        for sym in formula.inputs_for(state["unknown"]):
            var = formula.variables[sym]
            default = "" if var.default is None else fmt(var.default)
            fields[sym] = number_field(f"{pretty(sym)} · {var.label}", var.unit,
                                       old.get(sym) or default, on_submit=calculate)
        inputs_col.controls = list(fields.values())
        result.reset()
        steps.visible = False

    def on_unknown(e) -> None:
        sel = e.control.selected
        state["unknown"] = next(iter(sel)) if sel else syms[0]
        build_inputs()
        page.update()

    def calculate(_e=None) -> None:
        unknown = state["unknown"]
        try:
            values = {s: parse_number(f.value, formula.variables[s].label)
                      for s, f in fields.items()}
            value = formula.solve(unknown, values)
        except CalcError as exc:
            result.error(str(exc))
            steps.visible = False
            page.update()
            return
        var = formula.variables[unknown]
        text = f"{pretty(unknown)} = {fmt(value)} {var.unit}".strip()
        detail = formula.describe(value, values) if formula.describe else ""
        result.show_value(text, detail, title=var.label,
                          copy_text=f"{fmt(value)} {var.unit}".strip())
        # resumen tipo «Datos / Fórmula / Resultado», como en un examen
        data_lines = [f"{pretty(s)} = {fmt(v)} {formula.variables[s].unit}".strip()
                      for s, v in values.items()]
        steps.controls = [
            ft.Text("Datos", weight=ft.FontWeight.W_600),
            *[ft.Text(f"• {line}", selectable=True) for line in data_lines],
            ft.Text("Fórmula", weight=ft.FontWeight.W_600),
            ft.Text(f"{formula.equation}   →   despejamos {pretty(unknown)}"),
            ft.Text("Resultado", weight=ft.FontWeight.W_600),
            ft.Text(text, selectable=True),
        ]
        steps.visible = True
        given = ", ".join(data_lines)
        ctx.history.add(formula.name, given, text)
        page.update()

    def clear(_e) -> None:
        for f in fields.values():
            f.value = ""
        result.reset()
        steps.visible = False
        page.update()

    def toggle_fav(e) -> None:
        on = ctx.store.toggle_favorite(formula.id)
        star.icon = ft.Icons.STAR if on else ft.Icons.STAR_BORDER
        star.icon_color = ft.Colors.AMBER if on else None
        toast(page, "Añadida a favoritas" if on else "Quitada de favoritas")
        page.update()

    is_fav = ctx.store.is_favorite(formula.id)
    star = ft.IconButton(ft.Icons.STAR if is_fav else ft.Icons.STAR_BORDER,
                         icon_color=ft.Colors.AMBER if is_fav else None,
                         tooltip="Favorita", on_click=toggle_fav)

    selector = ft.SegmentedButton(
        segments=[ft.Segment(value=s, label=ft.Text(pretty(s))) for s in syms],
        selected=[syms[0]],
        show_selected_icon=False,
        on_change=on_unknown,
    )
    build_inputs()

    legend = ", ".join(f"{pretty(s)}: {v.label.lower()}{f' ({v.unit})' if v.unit else ''}"
                       for s, v in formula.variables.items())
    header = card(
        ft.Text(formula.equation, size=24, weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER),
        info_text(legend),
        *([ft.Text(formula.note, size=13, color=ft.Colors.PRIMARY)] if formula.note else []),
    )
    push_page(page, formula.name, [
        header,
        ft.Text("¿Qué quieres calcular?", weight=ft.FontWeight.W_600),
        ft.Row([selector], scroll=ft.ScrollMode.AUTO),
        inputs_col,
        ft.Row([
            ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calculate, expand=True),
            ft.OutlinedButton("Limpiar", icon=ft.Icons.CLEAR, on_click=clear),
        ]),
        result,
        ft.Container(steps, padding=ft.Padding.symmetric(horizontal=8)),
        info_text("Consejo: puedes escribir 3,5 · 6.67e-11 · 6.67x10^-11"),
    ], subtitle=formula.category, actions=[star])


def open_converter(ctx: Ctx) -> None:
    page = ctx.page
    qty = ft.Dropdown(label="Magnitud", value="Longitud", expand=True,
                      options=[ft.DropdownOption(q) for q in units.quantities()])
    src = ft.Dropdown(label="De", expand=True)
    dst = ft.Dropdown(label="A", expand=True)
    value = number_field("Valor", value="1")
    result = ResultPanel()
    table = ft.Column(spacing=2)

    def fill_units(_e=None) -> None:
        opts = units.units_of(qty.value)
        src.options = [ft.DropdownOption(u) for u in opts]
        dst.options = [ft.DropdownOption(u) for u in opts]
        src.value, dst.value = opts[0], opts[1]
        convert()

    def swap(_e) -> None:
        src.value, dst.value = dst.value, src.value
        convert()

    def convert(_e=None, record: bool = False) -> None:
        try:
            v = parse_number(value.value, "valor")
            out = units.convert(v, qty.value, src.value, dst.value)
        except CalcError as exc:
            result.error(str(exc))
            table.controls = []
        else:
            text = f"{fmt(v)} {src.value} = {fmt(out)} {dst.value}"
            result.show_value(f"{fmt(out)} {dst.value}", text, copy_text=fmt(out))
            # equivalencias en todas las unidades de la magnitud
            rows = []
            for u in units.units_of(qty.value):
                try:
                    rows.append(ft.Row([ft.Text(u, width=70, color=ft.Colors.ON_SURFACE_VARIANT),
                                        ft.Text(fmt(units.convert(v, qty.value, src.value, u)),
                                                selectable=True)]))
                except CalcError:
                    pass
            table.controls = [ft.Text(f"{fmt(v)} {src.value} equivale a:",
                                      weight=ft.FontWeight.W_600), *rows]
            if record:
                ctx.history.add("Conversión", qty.value, text)
                toast(page, "Guardado en el historial")
        page.update()

    qty.on_select = fill_units
    src.on_select = convert
    dst.on_select = convert
    value.on_change = convert
    value.on_submit = lambda e: convert(record=True)
    fill_units()

    push_page(page, "Conversor de unidades", [
        qty,
        value,
        ft.Row([src, ft.IconButton(ft.Icons.SWAP_HORIZ, tooltip="Intercambiar", on_click=swap), dst]),
        result,
        ft.OutlinedButton("Guardar en historial", icon=ft.Icons.HISTORY,
                          on_click=lambda e: convert(record=True)),
        card(table),
    ])


def open_constants(ctx: Ctx) -> None:
    page = ctx.page
    tiles = [
        ft.ListTile(
            title=ft.Text(name),
            subtitle=ft.Text(f"{sym} = {fmt(value, 10)} {unit}", selectable=True),
            trailing=ft.Icon(ft.Icons.CONTENT_COPY, size=18),
            on_click=lambda e, v=value: page.run_task(copy_to_clipboard, page, repr(v)),
        )
        for name, sym, value, unit in CONSTANTS
    ]
    push_page(page, "Constantes", [
        info_text("Toca una constante para copiar su valor."),
        ft.Column(tiles, spacing=0),
    ])

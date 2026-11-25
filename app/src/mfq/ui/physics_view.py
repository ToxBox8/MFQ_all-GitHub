"""Pantallas de Física y Química: buscador, catálogo y calculadora de fórmulas."""

from __future__ import annotations

import flet as ft

from ..core import physics, units
from ..core.numbers import CalcError, fmt, parse_number
from .history import History
from .widgets import (CATEGORY_ICONS, ResultPanel, card, number_field, pretty,
                      push_page, section_title)


class PhysicsTab(ft.Column):
    def __init__(self, page: ft.Page, history: History) -> None:
        self._page = page
        self.history = history
        self.search = ft.TextField(
            hint_text="Buscar fórmula…",
            prefix_icon=ft.Icons.SEARCH, border_radius=28, dense=True, filled=True,
            on_change=lambda e: self._render(e.control.value),
        )
        self.list = ft.Column(spacing=0)
        super().__init__(
            [ft.Container(self.search, padding=ft.Padding.symmetric(horizontal=16, vertical=8)),
             self.list],
            spacing=0, expand=True, scroll=ft.ScrollMode.AUTO,
        )
        self._render("")

    def _render(self, query: str) -> None:
        results = physics.search(query)
        controls: list[ft.Control] = []
        if not query:
            controls.append(self._converter_tile())
        current = None
        for f in results:
            if f.category != current:
                current = f.category
                controls.append(section_title(current))
            controls.append(ft.ListTile(
                leading=ft.Icon(CATEGORY_ICONS.get(f.category, ft.Icons.FUNCTIONS)),
                title=ft.Text(f.name),
                subtitle=ft.Text(f.equation),
                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                on_click=lambda e, f=f: open_formula(self._page, f, self.history),
            ))
        if not results:
            controls.append(ft.Container(
                ft.Text("No hay fórmulas que coincidan.", color=ft.Colors.ON_SURFACE_VARIANT),
                padding=24))
        self.list.controls = controls
        try:
            self.update()
        except RuntimeError:  # aún no está en la página
            pass

    def _converter_tile(self) -> ft.Control:
        return ft.Container(
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SWAP_HORIZ),
                title=ft.Text("Conversor de unidades"),
                subtitle=ft.Text("Longitud, masa, volumen, tiempo, temperatura…"),
                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                on_click=lambda e: open_converter(self._page, self.history),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=16),
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=4),
        )


def open_formula(page: ft.Page, formula: physics.Formula, history: History) -> None:
    syms = list(formula.solvers)
    state = {"unknown": syms[0]}
    fields: dict[str, ft.TextField] = {}
    result = ResultPanel()
    inputs_col = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

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
            page.update()
            return
        var = formula.variables[unknown]
        text = f"{pretty(unknown)} = {fmt(value)} {var.unit}".strip()
        detail = formula.describe(value, values) if formula.describe else ""
        result.show_value(text, detail, title=var.label, copy_text=f"{fmt(value)} {var.unit}".strip())
        given = ", ".join(f"{pretty(s)}={fmt(v)}" for s, v in values.items())
        history.add(formula.name, given, text)
        page.update()

    def clear(_e) -> None:
        for f in fields.values():
            f.value = ""
        result.reset()
        page.update()

    selector = ft.SegmentedButton(
        segments=[ft.Segment(value=s, label=ft.Text(pretty(s))) for s in syms],
        selected=[syms[0]],
        show_selected_icon=False,
        on_change=on_unknown,
    )
    build_inputs()

    header = card(
        ft.Text(formula.equation, size=24, weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER),
        *([ft.Text(formula.note, size=13, color=ft.Colors.ON_SURFACE_VARIANT)]
          if formula.note else []),
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
    ], subtitle=formula.category)


def open_converter(page: ft.Page, history: History) -> None:
    qty = ft.Dropdown(label="Magnitud", value="Longitud", expand=True,
                      options=[ft.DropdownOption(q) for q in units.quantities()])
    src = ft.Dropdown(label="De", expand=True)
    dst = ft.Dropdown(label="A", expand=True)
    value = number_field("Valor", value="1")
    result = ResultPanel()

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
        else:
            text = f"{fmt(v)} {src.value} = {fmt(out)} {dst.value}"
            result.show_value(f"{fmt(out)} {dst.value}", text, copy_text=fmt(out))
            if record:
                history.add("Conversión", f"{qty.value}", text)
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
        ft.FilledButton("Guardar en historial", icon=ft.Icons.HISTORY,
                        on_click=lambda e: convert(record=True)),
        result,
    ])

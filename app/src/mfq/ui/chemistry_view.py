"""Pestaña de Química: masa molar, gramos↔moles y tabla periódica."""

from __future__ import annotations

import flet as ft

from ..core import chemistry as chem
from ..core import physics
from ..core.numbers import CalcError, fmt, parse_number
from .context import Ctx
from .physics_view import open_formula
from .widgets import (ResultPanel, card, info_text, nav_tile, number_field, push_page,
                      section_title)

GROUP_COLORS = {
    chem.AM: "#E57373", chem.AT: "#FFB74D", chem.MT: "#90A4AE", chem.MP: "#81C784",
    chem.SM: "#4DB6AC", chem.NM: "#64B5F6", chem.HA: "#BA68C8", chem.GN: "#F06292",
    chem.LA: "#A1887F", chem.AC: "#DCE775",
}


class ChemistryTab(ft.Column):
    def __init__(self, ctx: Ctx) -> None:
        self.ctx = ctx
        controls: list[ft.Control] = [
            section_title("Herramientas"),
            nav_tile(ft.Icons.SCALE, "Masa molar", "De cualquier fórmula: H2SO4, Ca(OH)2, CuSO4·5H2O",
                     lambda e: open_molar_mass(ctx), highlight=True),
            nav_tile(ft.Icons.GRID_VIEW, "Tabla periódica", "118 elementos con buscador",
                     lambda e: open_periodic_table(ctx)),
            section_title("Fórmulas"),
        ]
        for f in physics.FORMULAS:
            if f.category == "Química":
                controls.append(nav_tile(ft.Icons.SCIENCE, f.name, f.equation,
                                         lambda e, f=f: open_formula(ctx, f)))
        super().__init__(controls, spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)


def open_molar_mass(ctx: Ctx) -> None:
    page = ctx.page
    formula = ft.TextField(label="Fórmula química", value="H2SO4", dense=True,
                           border_radius=12, autocorrect=False,
                           capitalization=ft.TextCapitalization.NONE)
    examples = ft.Row([ft.Chip(label=ft.Text(chem.pretty_formula(x)),
                               on_click=lambda e, x=x: _set_and(formula, x, calc))
                       for x in ("H2O", "NaCl", "CO2", "C6H12O6", "Ca(OH)2", "CuSO4·5H2O")],
                      wrap=True)
    result = ResultPanel()
    table = ft.Column(spacing=0)
    grams = number_field("Masa", "g", "100")
    moles_out = ft.Text("", selectable=True)
    state: dict[str, float] = {}

    def to_moles(_e=None) -> None:
        if "M" not in state:
            return
        try:
            g = parse_number(grams.value, "masa")
            n = chem.grams_to_moles(g, state["M"])
            moles_out.value = (f"{fmt(g)} g = {fmt(n)} mol\n"
                               f"= {fmt(n * chem.AVOGADRO)} moléculas")
        except CalcError as exc:
            moles_out.value = str(exc)
        page.update()

    def calc(_e=None) -> None:
        try:
            mm = chem.molar_mass(formula.value)
        except CalcError as exc:
            result.error(str(exc))
            table.controls = []
            state.pop("M", None)
            page.update()
            return
        state["M"] = mm.mass
        pf = chem.pretty_formula(formula.value.strip())
        result.show_value(f"M = {fmt(mm.mass)} g/mol", pf, title="Masa molar",
                          copy_text=fmt(mm.mass))
        header = ft.Row([ft.Text("Elem.", width=56, weight=ft.FontWeight.W_600),
                         ft.Text("Átomos", width=60, weight=ft.FontWeight.W_600),
                         ft.Text("Masa", width=80, weight=ft.FontWeight.W_600),
                         ft.Text("%", weight=ft.FontWeight.W_600)])
        rows = [header]
        for el, n, m, pct in mm.composition:
            rows.append(ft.Row([
                ft.Text(el.symbol, width=56, tooltip=el.name),
                ft.Text(str(n), width=60),
                ft.Text(fmt(m, 5), width=80),
                ft.Column([ft.Text(f"{pct:.2f} %"),
                           ft.ProgressBar(value=pct / 100, width=90,
                                          color=GROUP_COLORS.get(el.group))], spacing=2),
            ]))
        table.controls = rows
        ctx.history.add("Masa molar", pf, f"{fmt(mm.mass)} g/mol")
        to_moles()
        page.update()

    formula.on_submit = calc
    grams.on_change = to_moles
    calc()
    push_page(page, "Masa molar", [
        formula,
        examples,
        ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=calc),
        result,
        card(ft.Text("Composición", weight=ft.FontWeight.W_600), table),
        card(ft.Text("Gramos → moles", weight=ft.FontWeight.W_600), grams, moles_out),
        info_text("Respeta mayúsculas: Co (cobalto) ≠ CO (monóxido de carbono). "
                  "Para hidratos usa «·», «*» o «.»: CuSO4·5H2O"),
    ])


def _set_and(field: ft.TextField, value: str, fn) -> None:
    field.value = value
    fn()


def open_periodic_table(ctx: Ctx) -> None:
    page = ctx.page
    listing = ft.Column(spacing=0)

    def show(el: chem.Element) -> None:
        page.show_dialog(ft.AlertDialog(
            title=ft.Row([_badge(el, 56), ft.Text(el.name)], spacing=12),
            content=ft.Column([
                ft.Text(f"Número atómico (Z): {el.z}"),
                ft.Text(f"Masa atómica: {fmt(el.mass, 6)} u"),
                ft.Text(f"Masa molar: {fmt(el.mass, 6)} g/mol"),
                ft.Text(f"Familia: {el.group}"),
            ], tight=True, spacing=6),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())],
        ))

    def render(query: str = "") -> None:
        els = chem.find_elements(query)
        listing.controls = [
            ft.ListTile(leading=_badge(el), title=ft.Text(el.name),
                        subtitle=ft.Text(f"Z = {el.z} · {fmt(el.mass, 6)} u · {el.group}"),
                        on_click=lambda e, el=el: show(el))
            for el in els
        ] or [ft.Text("Sin resultados", color=ft.Colors.ON_SURFACE_VARIANT)]
        page.update()

    search = ft.TextField(hint_text="Buscar por nombre, símbolo, Z o familia",
                          prefix_icon=ft.Icons.SEARCH, border_radius=28, dense=True,
                          filled=True, on_change=lambda e: render(e.control.value or ""))
    legend = ft.Row([ft.Container(ft.Text(g, size=11, color="#000000"), bgcolor=c,
                                  border_radius=8, padding=ft.Padding.symmetric(horizontal=6, vertical=2))
                     for g, c in GROUP_COLORS.items()], wrap=True, spacing=4, run_spacing=4)
    els = chem.find_elements("")
    listing.controls = [
        ft.ListTile(leading=_badge(el), title=ft.Text(el.name),
                    subtitle=ft.Text(f"Z = {el.z} · {fmt(el.mass, 6)} u · {el.group}"),
                    on_click=lambda e, el=el: show(el))
        for el in els
    ]
    push_page(page, "Tabla periódica", [search, legend, listing])


def _badge(el: chem.Element, size: int = 44) -> ft.Control:
    return ft.Container(
        ft.Column([ft.Text(str(el.z), size=size * 0.2, color="#000000"),
                   ft.Text(el.symbol, size=size * 0.38, weight=ft.FontWeight.BOLD, color="#000000")],
                  spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                  alignment=ft.MainAxisAlignment.CENTER),
        width=size, height=size, border_radius=8, bgcolor=GROUP_COLORS.get(el.group, "#CCCCCC"),
        alignment=ft.Alignment.CENTER,
    )

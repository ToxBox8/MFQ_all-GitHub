"""MFQ All — Física, Química y Matemáticas para el instituto.

Ejecutar en el ordenador:   flet run src/main.py
Ejecutar en el móvil:       flet run --android src/main.py  (con la app «Flet» instalada)
Generar APK:                flet build apk
"""

from __future__ import annotations

import datetime as dt

import flet as ft

from mfq import __version__
from mfq.core import physics
from mfq.ui.chemistry_view import ChemistryTab
from mfq.ui.context import Ctx
from mfq.ui.history import History
from mfq.ui.maths_view import MathsTab
from mfq.ui.physics_view import PhysicsTab
from mfq.ui.store import Store
from mfq.ui.widgets import copy_to_clipboard, empty_state, info_text, push_page, section_title

SEED = "#3B6FE0"
REPO_URL = "https://github.com/ToxBox8/MFQ_all-GitHub"
THEMES = {"system": ft.ThemeMode.SYSTEM, "light": ft.ThemeMode.LIGHT, "dark": ft.ThemeMode.DARK}


class HistoryTab(ft.Column):
    def __init__(self, ctx: Ctx) -> None:
        self.ctx = ctx
        self.query = ""
        self.items = ft.Column(spacing=0)
        self.search = ft.TextField(hint_text="Buscar en el historial…", prefix_icon=ft.Icons.SEARCH,
                                   border_radius=28, dense=True, filled=True,
                                   on_change=self._on_search)
        self.search_box = ft.Container(self.search,
                                       padding=ft.Padding.symmetric(horizontal=16, vertical=8))
        super().__init__([self.search_box, self.items], spacing=0, expand=True,
                         scroll=ft.ScrollMode.AUTO)
        ctx.history.subscribe(self.refresh)
        self.refresh()

    def _on_search(self, e) -> None:
        self.query = (e.control.value or "").lower()
        self.refresh()

    def refresh(self) -> None:
        h = self.ctx.history
        self.search_box.visible = bool(h.items)
        if not h.items:
            self.items.controls = [empty_state(ft.Icons.HISTORY, "Aún no hay cálculos",
                                               "Los resultados que obtengas aparecerán aquí.")]
        else:
            shown = [e for e in h.items
                     if not self.query or self.query in f"{e.title} {e.expression} {e.result}".lower()]
            n = len(shown)
            rows: list[ft.Control] = [ft.Row(
                [ft.Text(f"{n} cálculo{'s' if n != 1 else ''}", color=ft.Colors.ON_SURFACE_VARIANT),
                 ft.Row([
                     ft.IconButton(ft.Icons.CONTENT_COPY, tooltip="Copiar todo",
                                   on_click=self._copy_all),
                     ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Borrar todo",
                                   on_click=self._confirm_clear),
                 ], spacing=0)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]
            last_day = None
            for e in shown:
                when = dt.datetime.fromtimestamp(e.ts)
                day = _day_label(when)
                if day != last_day:
                    rows.append(section_title(day))
                    last_day = day
                rows.append(ft.ListTile(
                    title=ft.Text(e.result, weight=ft.FontWeight.W_500, selectable=True),
                    subtitle=ft.Text(f"{e.title} · {e.expression}", size=12, max_lines=2,
                                     overflow=ft.TextOverflow.ELLIPSIS),
                    trailing=ft.Text(when.strftime("%H:%M"), size=11,
                                     color=ft.Colors.ON_SURFACE_VARIANT),
                    on_click=lambda ev, t=e.result: self.ctx.page.run_task(
                        copy_to_clipboard, self.ctx.page, t),
                ))
            if not shown:
                rows.append(ft.Container(ft.Text("Nada coincide con la búsqueda.",
                                                  color=ft.Colors.ON_SURFACE_VARIANT), padding=24))
            rows.append(info_text("   Toca un resultado para copiarlo."))
            self.items.controls = [ft.Container(ft.Column(rows, spacing=0),
                                                padding=ft.Padding.symmetric(horizontal=8))]
        try:
            self.update()
        except RuntimeError:
            pass

    async def _copy_all(self, _e) -> None:
        text = "\n".join(f"[{dt.datetime.fromtimestamp(e.ts):%d/%m/%Y %H:%M}] {e.title}: "
                         f"{e.expression} → {e.result}" for e in self.ctx.history.items)
        await copy_to_clipboard(self.ctx.page, text)

    def _confirm_clear(self, _e) -> None:
        confirm_clear_history(self.ctx)


def _day_label(when: dt.datetime) -> str:
    today = dt.date.today()
    d = when.date()
    if d == today:
        return "Hoy"
    if d == today - dt.timedelta(days=1):
        return "Ayer"
    return when.strftime("%d/%m/%Y")


def confirm_clear_history(ctx: Ctx) -> None:
    page = ctx.page

    def do_clear(_e) -> None:
        page.pop_dialog()
        ctx.history.clear()

    page.show_dialog(ft.AlertDialog(
        title=ft.Text("¿Borrar el historial?"),
        content=ft.Text("Esta acción no se puede deshacer."),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                 ft.FilledButton("Borrar", on_click=do_clear)],
    ))


def open_settings(ctx: Ctx, apply_theme) -> None:
    page = ctx.page
    theme = ft.SegmentedButton(
        segments=[ft.Segment(value="system", label=ft.Text("Sistema"), icon=ft.Icon(ft.Icons.BRIGHTNESS_AUTO)),
                  ft.Segment(value="light", label=ft.Text("Claro"), icon=ft.Icon(ft.Icons.LIGHT_MODE)),
                  ft.Segment(value="dark", label=ft.Text("Oscuro"), icon=ft.Icon(ft.Icons.DARK_MODE))],
        selected=[ctx.store.theme], show_selected_icon=False,
        on_change=lambda e: apply_theme((e.control.selected or ["system"])[0]),
    )
    sig_label = ft.Text(f"Cifras significativas: {ctx.store.sig}")
    example = info_text("")

    def sig_preview() -> None:
        from mfq.core.numbers import fmt
        example.value = f"Ejemplo: π = {fmt(3.141592653589793)} · G = {fmt(6.6743e-11)}"

    def on_sig(e) -> None:
        ctx.store.set_sig(int(e.control.value))
        sig_label.value = f"Cifras significativas: {ctx.store.sig}"
        sig_preview()
        page.update()

    sig_preview()
    sig = ft.Slider(min=3, max=12, divisions=9, value=ctx.store.sig, label="{value}", on_change=on_sig)

    push_page(page, "Ajustes", [
        section_title("Apariencia"), theme,
        section_title("Resultados"), sig_label, sig, example,
        section_title("Datos"),
        ft.OutlinedButton("Borrar historial", icon=ft.Icons.DELETE_OUTLINE,
                          on_click=lambda e: confirm_clear_history(ctx)),
        section_title("Acerca de"),
        ft.ListTile(leading=ft.Icon(ft.Icons.INFO_OUTLINE), title=ft.Text(f"MFQ All {__version__}"),
                    subtitle=ft.Text(f"{len(physics.FORMULAS)} fórmulas · Física, Química y Matemáticas")),
        ft.ListTile(leading=ft.Icon(ft.Icons.CODE), title=ft.Text("Código fuente en GitHub"),
                    subtitle=ft.Text("ToxBox8/MFQ_all-GitHub"), url=REPO_URL),
        info_text("Proyecto de ToxBox8. Hecho con Python y Flet."),
    ])


async def main(page: ft.Page) -> None:
    page.title = "MFQ All"
    page.theme = ft.Theme(color_scheme_seed=SEED, use_material3=True)
    page.dark_theme = ft.Theme(color_scheme_seed=SEED, use_material3=True)
    page.padding = 0

    store = Store(page)
    history = History(page)
    ctx = Ctx(page, history, store)
    await store.load()
    page.theme_mode = THEMES.get(store.theme, ft.ThemeMode.SYSTEM)

    tabs = [PhysicsTab(ctx), ChemistryTab(ctx), MathsTab(ctx), HistoryTab(ctx)]
    titles = ["Física", "Química", "Matemáticas", "Historial"]
    body = ft.Container(tabs[0], expand=True)
    title = ft.Text(titles[0])

    def apply_theme(mode: str) -> None:
        store.set_theme(mode)
        page.theme_mode = THEMES.get(mode, ft.ThemeMode.SYSTEM)
        page.update()

    def on_nav(e) -> None:
        i = e.control.selected_index
        body.content = tabs[i]
        title.value = titles[i]
        page.update()

    def on_view_pop(e) -> None:
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = on_view_pop
    page.views[0].appbar = ft.AppBar(
        title=title,
        leading=ft.Container(ft.Icon(ft.Icons.SCIENCE, color=ft.Colors.PRIMARY),
                             padding=ft.Padding.only(left=12)),
        actions=[ft.IconButton(ft.Icons.SETTINGS_OUTLINED, tooltip="Ajustes",
                               on_click=lambda e: open_settings(ctx, apply_theme))],
    )
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SPEED_OUTLINED, selected_icon=ft.Icons.SPEED,
                                        label="Física"),
            ft.NavigationBarDestination(icon=ft.Icons.SCIENCE_OUTLINED, selected_icon=ft.Icons.SCIENCE,
                                        label="Química"),
            ft.NavigationBarDestination(icon=ft.Icons.CALCULATE_OUTLINED,
                                        selected_icon=ft.Icons.CALCULATE, label="Mates"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY_OUTLINED,
                                        selected_icon=ft.Icons.HISTORY, label="Historial"),
        ],
    )
    page.add(ft.SafeArea(body, expand=True))
    await history.load()


if __name__ == "__main__":
    ft.run(main)

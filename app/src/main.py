"""MFQ All — Física, Química y Matemáticas para el instituto.

Ejecutar en el ordenador:   flet run src/main.py
Ejecutar en el móvil:       flet run --android src/main.py  (con la app «Flet» instalada)
Generar APK:                flet build apk
"""

from __future__ import annotations

import datetime as dt

import flet as ft

from mfq import __version__
from mfq.ui.history import History
from mfq.ui.maths_view import MathsTab
from mfq.ui.physics_view import PhysicsTab
from mfq.ui.widgets import copy_to_clipboard

SEED = "#3B6FE0"
THEME_KEY = "mfq.theme"


class HistoryTab(ft.Column):
    def __init__(self, page: ft.Page, history: History) -> None:
        self._page = page
        self.history = history
        self.items = ft.Column(spacing=0)
        super().__init__([self.items], expand=True, scroll=ft.ScrollMode.AUTO)
        history.subscribe(self.refresh)
        self.refresh()

    def refresh(self) -> None:
        if not self.history.items:
            self.items.controls = [ft.Container(
                ft.Column([
                    ft.Icon(ft.Icons.HISTORY, size=64, color=ft.Colors.OUTLINE),
                    ft.Text("Aún no hay cálculos", size=16, weight=ft.FontWeight.W_500),
                    ft.Text("Los resultados que obtengas aparecerán aquí.",
                            color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=48, alignment=ft.Alignment.CENTER)]
        else:
            rows: list[ft.Control] = [ft.Row(
                [ft.Text(f"{len(self.history.items)} cálculo{'s' if len(self.history.items) != 1 else ''}", color=ft.Colors.ON_SURFACE_VARIANT),
                 ft.TextButton("Borrar todo", icon=ft.Icons.DELETE_OUTLINE,
                               on_click=self._confirm_clear)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]
            for e in self.history.items:
                when = dt.datetime.fromtimestamp(e.ts).strftime("%d/%m %H:%M")
                rows.append(ft.ListTile(
                    title=ft.Text(e.result, weight=ft.FontWeight.W_500, selectable=True),
                    subtitle=ft.Text(f"{e.title} · {e.expression}", size=12),
                    trailing=ft.Text(when, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                    on_long_press=lambda ev, t=e.result: self._page.run_task(
                        copy_to_clipboard, self._page, t),
                ))
            self.items.controls = [ft.Container(ft.Column(rows, spacing=0),
                                                padding=ft.Padding.symmetric(horizontal=8))]
        try:
            self.update()
        except RuntimeError:  # aún no está en la página
            pass

    def _confirm_clear(self, _e) -> None:
        def do_clear(_e) -> None:
            self._page.pop_dialog()
            self.history.clear()

        self._page.show_dialog(ft.AlertDialog(
            title=ft.Text("¿Borrar el historial?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self._page.pop_dialog()),
                     ft.FilledButton("Borrar", on_click=do_clear)],
        ))


async def main(page: ft.Page) -> None:
    page.title = "MFQ All"
    page.theme = ft.Theme(color_scheme_seed=SEED, use_material3=True)
    page.dark_theme = ft.Theme(color_scheme_seed=SEED, use_material3=True)
    page.padding = 0

    prefs = ft.SharedPreferences()
    try:
        saved = await prefs.get(THEME_KEY)
        page.theme_mode = ft.ThemeMode(saved) if saved else ft.ThemeMode.SYSTEM
    except Exception:
        page.theme_mode = ft.ThemeMode.SYSTEM

    history = History(page)
    tabs = [PhysicsTab(page, history), MathsTab(page, history), HistoryTab(page, history)]
    titles = ["Física y Química", "Matemáticas", "Historial"]
    body = ft.Container(tabs[0], expand=True)
    title = ft.Text(titles[0])

    def theme_icon() -> ft.IconData:
        return ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE

    async def toggle_theme(e) -> None:
        dark_now = (page.theme_mode == ft.ThemeMode.DARK or
                    (page.theme_mode == ft.ThemeMode.SYSTEM
                     and page.platform_brightness == ft.Brightness.DARK))
        page.theme_mode = ft.ThemeMode.LIGHT if dark_now else ft.ThemeMode.DARK
        theme_btn.icon = theme_icon()
        page.update()
        try:
            await prefs.set(THEME_KEY, page.theme_mode.value)
        except Exception:
            pass

    def about(_e) -> None:
        page.show_dialog(ft.AlertDialog(
            title=ft.Text("MFQ All"),
            content=ft.Text(
                f"Versión {__version__}\n\n"
                "Calculadora de Física, Química y Matemáticas.\n"
                "Proyecto de ToxBox8 · github.com/ToxBox8/MFQ_all-GitHub"),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())],
        ))

    theme_btn = ft.IconButton(theme_icon(), tooltip="Cambiar tema", on_click=toggle_theme)

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
        actions=[theme_btn,
                 ft.IconButton(ft.Icons.INFO_OUTLINE, tooltip="Acerca de", on_click=about)],
    )
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SCIENCE_OUTLINED,
                                        selected_icon=ft.Icons.SCIENCE, label="FyQ"),
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

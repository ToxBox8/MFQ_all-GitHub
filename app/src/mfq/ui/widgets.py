"""Componentes y utilidades de interfaz compartidos."""

from __future__ import annotations

import inspect
from typing import Callable

import flet as ft

PRETTY = {
    "x0": "x₀", "v0": "v₀", "rho": "ρ", "mu": "μ", "lam": "λ", "theta": "θ",
    "m1": "m₁", "m2": "m₂", "q1": "q₁", "q2": "q₂", "CL": "C_L", "dx": "Δx",
}

CATEGORY_ICONS = {
    "Cinemática": ft.Icons.SPEED,
    "Tiro parabólico": ft.Icons.SPORTS_BASEBALL,
    "Dinámica": ft.Icons.FITNESS_CENTER,
    "Energía": ft.Icons.BOLT,
    "Gravitación": ft.Icons.PUBLIC,
    "Fluidos": ft.Icons.WATER_DROP,
    "Electricidad": ft.Icons.ELECTRIC_BOLT,
    "Ondas": ft.Icons.WAVES,
    "Química": ft.Icons.SCIENCE,
}


def pretty(sym: str) -> str:
    return PRETTY.get(sym, sym)


def section_title(text: str) -> ft.Control:
    return ft.Container(
        ft.Text(text, size=13, weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),
        padding=ft.Padding.only(left=16, top=18, bottom=4),
    )


def card(*controls: ft.Control, padding: int = 16) -> ft.Card:
    return ft.Card(
        ft.Container(ft.Column(list(controls), spacing=12,
                               horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                     padding=padding),
        variant=ft.CardVariant.FILLED,
    )


def number_field(label: str, unit: str = "", value: str = "",
                 on_submit: Callable | None = None) -> ft.TextField:
    return ft.TextField(
        label=f"{label} [{unit}]" if unit else label,
        value=value,
        suffix=unit or None,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=12,
        dense=True,
        on_submit=on_submit,
    )


class ResultPanel(ft.Container):
    """Tarjeta de resultado con estado vacío, éxito y error, y botón copiar."""

    def __init__(self) -> None:
        self._title = ft.Text("Resultado", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self._value = ft.Text("—", size=28, weight=ft.FontWeight.BOLD, selectable=True)
        self._detail = ft.Text("", size=14, selectable=True)
        self._copy = ft.IconButton(ft.Icons.CONTENT_COPY, tooltip="Copiar",
                                   on_click=self._on_copy, visible=False)
        self._copy_text = ""
        super().__init__(
            content=ft.Row(
                [ft.Column([self._title, self._value, self._detail], spacing=4, expand=True),
                 self._copy],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=20,
            border_radius=16,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

    def show(self, value: str, detail: str = "", title: str = "Resultado",
             copy_text: str | None = None) -> None:
        self.bgcolor = ft.Colors.PRIMARY_CONTAINER
        self._title.value = title
        self._value.value = value
        self._value.color = ft.Colors.ON_PRIMARY_CONTAINER
        self._detail.value = detail
        self._detail.visible = bool(detail)
        self._copy_text = copy_text if copy_text is not None else value
        self._copy.visible = True

    def error(self, message: str) -> None:
        self.bgcolor = ft.Colors.ERROR_CONTAINER
        self._title.value = "No se puede calcular"
        self._value.value = message
        self._value.size = 16
        self._value.color = ft.Colors.ON_ERROR_CONTAINER
        self._detail.visible = False
        self._copy.visible = False

    def reset(self) -> None:
        self.bgcolor = ft.Colors.PRIMARY_CONTAINER
        self._title.value = "Resultado"
        self._value.value = "—"
        self._value.size = 28
        self._detail.visible = False
        self._copy.visible = False

    def show_value(self, value: str, *a, **kw) -> None:  # alias legible
        self._value.size = 28
        self.show(value, *a, **kw)

    async def _on_copy(self, _e) -> None:
        await copy_to_clipboard(self.page, self._copy_text)


async def copy_to_clipboard(page: ft.Page, text: str) -> None:
    result = ft.Clipboard().set(text)
    if inspect.isawaitable(result):
        await result
    toast(page, "Copiado al portapapeles")


def toast(page: ft.Page, message: str) -> None:
    page.show_dialog(ft.SnackBar(ft.Text(message), duration=ft.Duration(seconds=2)))


def push_page(page: ft.Page, title: str, controls: list[ft.Control],
              subtitle: str | None = None) -> None:
    """Abre una pantalla secundaria con botón atrás (incluido el gesto de Android)."""
    title_ctrl: ft.Control = ft.Text(title)
    if subtitle:
        title_ctrl = ft.Column([ft.Text(title, size=18),
                                ft.Text(subtitle, size=12, color=ft.Colors.ON_SURFACE_VARIANT)],
                               spacing=0)
    page.views.append(
        ft.View(
            route=f"/{len(page.views)}",
            appbar=ft.AppBar(title=title_ctrl),
            controls=[ft.SafeArea(
                ft.Container(ft.Column(controls, spacing=16,
                                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                             padding=16, max_width=720), expand=True)],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()

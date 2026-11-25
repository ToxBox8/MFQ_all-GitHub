"""Objeto de contexto compartido por todas las pantallas."""

from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from .history import History
from .store import Store


@dataclass
class Ctx:
    page: ft.Page
    history: History
    store: Store

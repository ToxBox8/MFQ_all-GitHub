"""Preferencias persistentes del usuario (favoritos, ajustes)."""

from __future__ import annotations

import json
from typing import Callable

import flet as ft

from ..core.numbers import SETTINGS

KEY = "mfq.prefs.v1"


class Store:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.favorites: list[str] = []
        self.theme: str = "system"
        self._listeners: list[Callable[[], None]] = []
        try:
            self._prefs: ft.SharedPreferences | None = ft.SharedPreferences()
        except Exception:
            self._prefs = None

    @property
    def sig(self) -> int:
        return SETTINGS["sig"]

    def set_sig(self, value: int) -> None:
        SETTINGS["sig"] = max(3, min(12, int(value)))
        self.save()

    def subscribe(self, fn: Callable[[], None]) -> None:
        self._listeners.append(fn)

    def is_favorite(self, fid: str) -> bool:
        return fid in self.favorites

    def toggle_favorite(self, fid: str) -> bool:
        if fid in self.favorites:
            self.favorites.remove(fid)
        else:
            self.favorites.append(fid)
        self.save()
        self._notify()
        return fid in self.favorites

    def set_theme(self, mode: str) -> None:
        self.theme = mode
        self.save()

    async def load(self) -> None:
        if not self._prefs:
            return
        try:
            raw = await self._prefs.get(KEY)
            data = json.loads(raw) if raw else {}
        except Exception:
            data = {}
        self.favorites = [str(f) for f in data.get("favorites", [])]
        self.theme = data.get("theme", "system")
        SETTINGS["sig"] = int(data.get("sig", 6))
        self._notify()

    def save(self) -> None:
        self.page.run_task(self._save)

    async def _save(self) -> None:
        if not self._prefs:
            return
        data = {"favorites": self.favorites, "theme": self.theme, "sig": SETTINGS["sig"]}
        try:
            await self._prefs.set(KEY, json.dumps(data))
        except Exception:
            pass

    def _notify(self) -> None:
        for fn in self._listeners:
            fn()

"""Historial de cálculos persistente (SharedPreferences en el dispositivo)."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from typing import Callable

import flet as ft

KEY = "mfq.history.v1"
MAX_ITEMS = 100


@dataclass
class Entry:
    title: str
    expression: str
    result: str
    ts: float


class History:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.items: list[Entry] = []
        self._listeners: list[Callable[[], None]] = []
        try:
            self._prefs: ft.SharedPreferences | None = ft.SharedPreferences()
        except Exception:  # p. ej. en tests sin cliente
            self._prefs = None

    def subscribe(self, fn: Callable[[], None]) -> None:
        self._listeners.append(fn)

    async def load(self) -> None:
        if not self._prefs:
            return
        try:
            raw = await self._prefs.get(KEY)
            if raw:
                self.items = [Entry(**d) for d in json.loads(raw)][:MAX_ITEMS]
        except Exception:
            self.items = []
        self._notify()

    def add(self, title: str, expression: str, result: str) -> None:
        self.items.insert(0, Entry(title, expression, result, time.time()))
        del self.items[MAX_ITEMS:]
        self._notify()
        self.page.run_task(self._save)

    def clear(self) -> None:
        self.items.clear()
        self._notify()
        self.page.run_task(self._save)

    async def _save(self) -> None:
        if not self._prefs:
            return
        try:
            await self._prefs.set(KEY, json.dumps([asdict(e) for e in self.items],
                                                  ensure_ascii=False))
        except Exception:
            pass

    def _notify(self) -> None:
        for fn in self._listeners:
            fn()

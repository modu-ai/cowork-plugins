"""Tool package — auto-imports every category module to populate the registry.

Each category module (``store.py``, ``product.py``, ...) calls
``register(Endpoint(...), ...)`` at import time, appending to the process-wide
:class:`~moai_mcp_cafe24.registry.Registry`. Importing this package loads them all.
Modules prefixed with ``_`` (like ``_dispatch``) are skipped.
"""

from __future__ import annotations

import importlib
import pkgutil


def _load_all() -> list[str]:
    loaded: list[str] = []
    for mod_info in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if mod_info.name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{mod_info.name}")
        loaded.append(mod_info.name)
    return loaded


LOADED_MODULES = _load_all()

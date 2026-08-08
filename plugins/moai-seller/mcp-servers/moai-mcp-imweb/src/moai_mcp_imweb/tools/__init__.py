"""Generated tools package — importing it registers all Imweb category tools."""
from __future__ import annotations

from . import site_info  # noqa: F401
from . import member_info  # noqa: F401
from . import community  # noqa: F401
from . import promotion  # noqa: F401
from . import product  # noqa: F401
from . import order  # noqa: F401
from . import script  # noqa: F401
from . import payment  # noqa: F401

__all__ = ["site_info", "member_info", "community", "promotion", "product", "order", "script", "payment"]

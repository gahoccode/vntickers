"""
vntickers - A Python package for fetching Vietnamese stock market data.

This package provides a unified interface to access stock price data from multiple
data sources (vnstock, vnquant, and vietfin).

Uses lazy imports to avoid loading unnecessary dependencies.
"""

from typing import TYPE_CHECKING

# Type hints for better IDE support
if TYPE_CHECKING:
    from .vnstock_loader import VnstockLoader
    from .vnquant_loader import VnquantLoader
    from .vietfin_loader import VietfinLoader, PriceDataParams
    from .loader import VNStockData

# Export all public APIs
__all__ = [
    # Focused loaders (recommended for new code)
    "VnstockLoader",
    "VnquantLoader",
    "VietfinLoader",
    "PriceDataParams",
    # Legacy facade (for backward compatibility)
    "VNStockData",
]


def __getattr__(name: str):
    """
    Lazy import loaders to avoid loading all dependencies at once.

    This allows users to import only the loader they need without
    loading dependencies for other data sources.
    """
    if name == "VnstockLoader":
        from .vnstock_loader import VnstockLoader
        return VnstockLoader
    elif name == "VnquantLoader":
        from .vnquant_loader import VnquantLoader
        return VnquantLoader
    elif name == "VietfinLoader":
        from .vietfin_loader import VietfinLoader
        return VietfinLoader
    elif name == "PriceDataParams":
        from .vietfin_loader import PriceDataParams
        return PriceDataParams
    elif name == "VNStockData":
        from .loader import VNStockData
        return VNStockData
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def main() -> None:
    """CLI entry point for vntickers."""
    print("Hello from vntickers!")

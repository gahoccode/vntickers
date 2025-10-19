# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vntickers` is a Python package for fetching Vietnamese stock market data. It provides a unified interface to access stock price data from multiple data sources (vnstock, vnquant, and vietfin).

## Package Structure

The package uses a modular architecture with focused loaders for each data source:

- **Main entry point**: `src/vntickers/__init__.py` - Exports all loaders and contains the `main()` CLI function

- **Focused data loaders** (recommended for new code):
  - `src/vntickers/vnstock_loader.py` - `VnstockLoader` class
    - `get_close_prices()` - Fetches data using vnstock library (VCI source)
  - `src/vntickers/vnquant_loader.py` - `VnquantLoader` class
    - `get_close_prices()` - Fetches adjusted close prices using vnquant library
  - `src/vntickers/vietfin_loader.py` - `VietfinLoader` class and `PriceDataParams`
    - `get_close_prices()` - Fetches historical close prices using vietfin library (DNSE or TCBS providers)
    - `PriceDataParams` - Pydantic model for validating vietfin data fetch parameters

- **Legacy facade** (for backward compatibility):
  - `src/vntickers/loader.py` - `VNStockData` class
    - Delegates to focused loaders for backward compatibility
    - Existing code using `VNStockData.get_close_prices_vns/vnq/vf()` continues to work

All loaders return wide-format pandas DataFrames with time/date as index and ticker symbols as columns.

**Recommendation**: Use focused loaders (`VnstockLoader`, `VnquantLoader`, `VietfinLoader`) for new code as they provide better separation of concerns and easier testing.

## Key Dependencies

- **vnstock**: Installed via PyPI (>=3.2.6)
- **vnquant**: Installed via PyPI
- **vietfin**: Installed via PyPI (for `get_close_prices_vf` method)
- **pydantic**: Used for parameter validation
- Managed with `uv` build system

## Common Commands

Development setup:
```bash
uv sync
```

Build and install in editable mode:
```bash
uv pip install -e .
```

Build package:
```bash
uv build
```

Publish to PyPI:
```bash
uv publish
# Or with token:
uv publish --token <your-pypi-token>
```

Run the CLI:
```bash
vntickers
```

## Development Notes

- Project uses `uv` as build backend (requires `uv_build>=0.8.22,<0.9.0`)
- Python >=3.10 required
- All data loaders return consistent DataFrame format (time/date index, ticker columns) for easy interoperability
- The vietfin method uses Python `date` objects (not strings) for start_date and end_date parameters
- The vietfin method includes parameter validation via Pydantic to ensure end_date >= start_date

### Performance Optimization

- **Lazy imports**: The package uses `__getattr__` in `__init__.py` for lazy loading
- Importing a specific loader (e.g., `VietfinLoader`) only loads that loader's dependencies
- This avoids loading vnstock when you only need vietfin, and vice versa
- Direct imports also work: `from vntickers.vietfin_loader import VietfinLoader`

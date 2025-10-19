# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vntickers` is a Python package for fetching Vietnamese stock market data. It provides a unified interface to access stock price data from multiple data sources (vnstock, vnquant, and vietfin).

## Package Structure

The package uses a modular architecture with focused loaders for each data source and parameter validation:

- **Main entry point**: `src/vntickers/__init__.py` - Exports all loaders and contains the `main()` CLI function

- **Parameter validators package**: `src/vntickers/validators/`
  - `base.py` - `StockCloseParams` base validator for common parameters (symbols, dates)
  - `vnstock.py` - `VnstockParams` extends base with vnstock-specific params (source, interval)
  - `vnquant.py` - `VnquantParams` extends base for vnquant (reserved for future enhancements)
  - `vietfin.py` - `VietfinParams` extends base with vietfin-specific params (provider, interval)

- **Focused data loaders** (recommended for new code):
  - `src/vntickers/vnstock_loader.py` - `VnstockLoader` class
    - `get_close_prices()` - Fetches data using vnstock library (VCI or TCBS source)
    - Uses `VnstockParams` for validation
  - `src/vntickers/vnquant_loader.py` - `VnquantLoader` class
    - `get_close_prices()` - Fetches adjusted close prices using vnquant library
    - Uses `VnquantParams` for validation
  - `src/vntickers/vietfin_loader.py` - `VietfinLoader` class and `PriceDataParams`
    - `get_close_prices()` - Fetches historical close prices using vietfin library (DNSE or TCBS providers)
    - Uses `VietfinParams` for validation
    - `PriceDataParams` - Vietfin library-specific internal validation (unchanged)

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

### Parameter Validation

- **Pydantic-based validation**: All loaders use Pydantic models for parameter validation
- **Base validation** (`StockCloseParams` - inherited by all loaders):
  - Symbol validation: Non-empty list, auto-uppercase (vnm → VNM), format check (2-4 alphanumeric chars)
  - Date validation: Accepts str ("2024-01-01") or date objects, validates YYYY-MM-DD format
  - Date order validation: Ensures end_date >= start_date
  - Raises clear ValueError messages for invalid inputs

- **Loader-specific validation**:
  - **VnstockParams**: Validates source (VCI/TCBS), interval format
  - **VnquantParams**: Currently no additional params (reserved for future)
  - **VietfinParams**: Validates provider (dnse/tcbs), interval support
    - **Supported intervals**:
      - **DNSE**: `1m`, `15m`, `30m`, `1h`, `1d`
        - `1m`: one minute (single symbol, max 90 days)
        - `15m`: 15 minutes (single symbol, max 90 days)
        - `30m`: 30 minutes (single symbol, max 90 days)
        - `1h`: one hour (single symbol, max 90 days)
        - `1d`: one day (multiple symbols, unlimited) [default]
      - **TCBS**: `1d` only
        - `1d`: one day (multiple symbols, unlimited) [default]
    - **DNSE Intraday Constraints**:
      - Intraday intervals (1m, 15m, 30m, 1h) limited to 90-day range
      - Intraday intervals (1m, 15m, 30m, 1h) support only single symbol per request
  - **PriceDataParams**: Vietfin library-specific internal validation (in vietfin_loader.py)

### Performance Optimization

- **Lazy imports**: The package uses `__getattr__` in `__init__.py` for lazy loading
- Importing a specific loader (e.g., `VietfinLoader`) only loads that loader's dependencies
- This avoids loading vnstock when you only need vietfin, and vice versa
- Direct imports also work: `from vntickers.vietfin_loader import VietfinLoader`
- Validators are also lazily loaded: importing `VietfinParams` doesn't load vnstock or vnquant

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vntickers` is a Python package for fetching Vietnamese stock market data. It provides a unified interface to access stock price data from multiple data sources (vnstock and vnquant).

## Package Structure

- **Main entry point**: `src/vntickers/__init__.py` - Contains the `main()` function registered as a CLI command
- **Data loader module**: `src/vntickers/loader.py` - Contains the `VNStockData` class with two static methods:
  - `get_close_prices_vns()` - Fetches data using vnstock library (VCI source)
  - `get_close_prices_vnq()` - Fetches adjusted close prices using vnquant library

Both methods return wide-format pandas DataFrames with time as index and ticker symbols as columns.

## Key Dependencies

- **vnstock**: Installed via PyPI (>=3.2.6)
- **vnquant**: Installed from git source (https://github.com/phamdinhkhanh/vnquant.git)
- Managed with `uv` build system

## Common Commands

Build and install:
```bash
uv pip install -e .
```

Run the CLI:
```bash
vntickers
```

## Development Notes

- Project uses `uv` as build backend (requires `uv_build>=0.8.22,<0.9.0`)
- Python >=3.10 required
- vnquant is installed from git source, not PyPI
- Both data loaders return consistent DataFrame format (time index, ticker columns) for easy interoperability

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-10-19

### Added
- Modular loader architecture with focused data source modules:
  - `VnstockLoader` for vnstock data source (VCI/TCBS)
  - `VnquantLoader` for vnquant data source
  - `VietfinLoader` for vietfin data source (DNSE/TCBS)
- Comprehensive parameter validation using Pydantic:
  - `StockCloseParams` base validator for common parameters (symbols, dates)
  - `VnstockParams` for vnstock-specific validation (source, interval)
  - `VnquantParams` for vnquant-specific validation
  - `VietfinParams` for vietfin-specific validation with interval constraints
- Lazy loading support for all loaders to optimize performance and reduce import overhead
- Support for intraday data intervals via VietfinLoader:
  - DNSE provider: `1m`, `15m`, `30m`, `1h`, `1d` intervals
  - TCBS provider: `1d` interval only
- Validation for DNSE API constraints:
  - 90-day maximum date range for intraday intervals (1m, 15m, 30m, 1h)
  - Single symbol requirement for intraday intervals
- Enhanced documentation:
  - Comprehensive CLAUDE.md with architecture overview and best practices
  - README updated with vietfin usage examples for daily and intraday data
- New dependencies: `vietfin`, `pydantic>=2.0.0`

### Changed
- **Breaking architectural change**: Refactored monolithic `VNStockData` class into separate focused loaders
- `VNStockData` class now serves as backward-compatible facade delegating to focused loaders
- Symbol validation now auto-normalizes to uppercase (e.g., `vnm` → `VNM`)
- Symbol format validation ensures 2-4 alphanumeric characters
- Date validation accepts both string format (`"2024-01-01"`) and Python `date` objects
- Date order validation ensures `end_date >= start_date`
- Enhanced error messages provide clear validation failure details

### Deprecated
- Direct use of `VNStockData` class methods (still supported for backward compatibility):
  - `VNStockData.get_close_prices_vns()` → Use `VnstockLoader.get_close_prices()`
  - `VNStockData.get_close_prices_vnq()` → Use `VnquantLoader.get_close_prices()`
  - `VNStockData.get_close_prices_vf()` → Use `VietfinLoader.get_close_prices()`

### Fixed
- Corrected vietfin interval support (removed unsupported `1w` and `1mo` intervals)
- Added missing `15m` and `30m` intervals for DNSE provider

## [0.1.1] - 2024-01-XX

### Added
- Vietfin data source for fetching historical close prices
- Support for DNSE and TCBS providers via vietfin
- PyPI publishing setup with uv build system

### Changed
- Updated vnquant dependency to PyPI version
- Improved package metadata and repository information
- Clarified package as unified data source in README

## [0.1.0] - 2024-01-XX

### Added
- Initial release of vntickers package
- Support for vnstock data source (VCI source)
- Support for vnquant data source
- Unified DataFrame interface with time index and ticker columns
- Support for multiple tickers and date ranges
- CLI entry point via `vntickers` command
- Comprehensive README with usage examples

### Technical Details
- Python >=3.10 required
- Built with uv build system
- Dependencies: vnstock>=3.2.6, vnquant, pandas

---

## Links

- [PyPI Package](https://pypi.org/project/vntickers/)
- [GitHub Repository](https://github.com/gahoccode/vntickers)
- [Issue Tracker](https://github.com/gahoccode/vntickers/issues)

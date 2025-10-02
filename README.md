# vntickers

A Python package for fetching Vietnamese stock market data from multiple sources.

## Installation

### From source (development)

```bash
git clone https://github.com/gahoccode/vntickers.git
cd vntickers
uv sync
```

### Add to your project

```bash
uv add vntickers
```

## Usage

### Using vnstock (VCI source)

```python
from vntickers.loader import VNStockData

stocks = ["VNM", "VCB", "HPG"]
start_date = "2024-01-01"
end_date = "2024-12-31"

df = VNStockData.get_close_prices_vns(
    symbols=stocks,
    start_date=start_date,
    end_date=end_date,
    interval="1D"
)
print(df.head())
```

### Using vnquant

```python
from vntickers.loader import VNStockData

stocks = ["VNM", "VCB", "HPG"]
start_date = "2024-01-01"
end_date = "2024-12-31"

df = VNStockData.get_close_prices_vnq(
    symbols=stocks,
    start_date=start_date,
    end_date=end_date
)
print(df.head())
```

Both methods return a pandas DataFrame with:
- Index: time (datetime)
- Columns: ticker symbols
- Values: close prices (adjusted close for vnquant)

## Requirements

- Python >=3.10
- vnstock >=3.2.6
- vnquant (from git source)

## Publishing to PyPI

### Prerequisites
1. Create a PyPI account at https://pypi.org
2. Create an API token at https://pypi.org/manage/account/token/

### Build and Publish

```bash
# Build the package
uv build

# Publish to PyPI (you'll be prompted for your API token)
uv publish

# Or use token directly
uv publish --token <your-pypi-token>
```

### Installing vnquant (optional dependency)

Since vnquant is not on PyPI, install it separately if needed:

```bash
uv pip install git+https://github.com/phamdinhkhanh/vnquant.git
```

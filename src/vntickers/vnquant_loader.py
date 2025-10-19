"""Vnquant data loader for Vietnamese stock market data."""

import pandas as pd
import vnquant.data as dt
from typing import List, Optional


class VnquantLoader:
    """Loader for fetching adjusted close stock data using vnquant library."""

    @staticmethod
    def get_close_prices(
        symbols: List[str], start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        Load adjusted close stock data for given symbols from vnquant DataLoader.

        Args:
            symbols (List[str]): List of stock symbols.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.

        Returns:
            Optional[pd.DataFrame]: Wide-format DataFrame with 'time' as index and
                ticker symbols as columns (values = adjusted close).
                Returns None if data is not available.
        """
        loader = dt.DataLoader(symbols, start_date, end_date, table_style="stack")
        data = loader.download()

        if data is not None and not data.empty:
            results = []

            for symbol in symbols:
                stock_data = data[data["code"] == symbol].copy()
                if stock_data.empty:
                    continue

                stock_data = stock_data.dropna(subset=["adjust"]).copy()
                stock_data.index = pd.to_datetime(stock_data.index, errors="coerce")
                stock_data = stock_data[stock_data.index.notna()]

                stock_data = stock_data.reset_index().rename(
                    columns={"date": "time", "code": "ticker"}
                )
                stock_data = stock_data.drop(columns=["close"], errors="ignore")
                stock_data = stock_data.rename(columns={"adjust": "close"})
                stock_data["close"] = stock_data["close"].round(2)

                stock_data["time"] = pd.to_datetime(stock_data["time"], errors="coerce")
                stock_data = stock_data[stock_data["time"].notna()]

                stock_data = stock_data[["time", "ticker", "close"]]
                results.append(stock_data)

            if results:
                final_df = pd.concat(results, ignore_index=True)
                final_df = final_df[
                    (final_df["time"] >= pd.to_datetime(start_date))
                    & (final_df["time"] <= pd.to_datetime(end_date))
                ]

                # Pivot: ticker symbols as columns, time as index
                wide_df = final_df.pivot(index="time", columns="ticker", values="close")
                wide_df.sort_index(inplace=True)

                # Reorder columns to match the input stock list
                wide_df = wide_df.reindex(columns=symbols)
                return wide_df

        return None

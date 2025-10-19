import pandas as pd
from vnstock import Vnstock
import vnquant.data as dt
from typing import List, Optional, Union
from datetime import date
from pydantic import BaseModel, Field, validator
from typing import Literal
from vietfin import vf


class VNStockData:
    @staticmethod
    def get_close_prices_vns(symbols, start_date, end_date, interval="1D"):
        """
        Fetch close prices for multiple stocks and return a DataFrame
        where each column is a ticker symbol.
        """
        all_data = {}

        for symbol in symbols:
            stock = Vnstock().stock(symbol=symbol, source="VCI")
            price = stock.quote.history(
                start=start_date, end=end_date, interval=interval, to_df=True
            )

            # Set index to 'time' (already datetime64[ns])
            price = price.set_index("time").sort_index()

            # Store the 'close' column under the stock symbol
            all_data[symbol] = price["close"]

        # Combine into one DataFrame (outer join on time index)
        df = pd.DataFrame(all_data)

        return df

    @staticmethod
    def get_close_prices_vnq(
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

    @staticmethod
    def get_close_prices_vf(
        symbols: Union[str, List[str]],
        start_date: date,
        end_date: date,
        provider: Literal["dnse", "tcbs"] = "dnse",
    ) -> pd.DataFrame:
        """
        Fetch historical close prices for one or multiple symbols using the Vietfin (vf) provider.

        Parameters
        ----------
        symbols : Union[str, List[str]]
            Stock ticker symbol or list of symbols.
        start_date : date
            Start date for fetching data.
        end_date : date
            End date for fetching data.
        provider : Literal["dnse", "tcbs"], optional
            Data provider to use ('dnse' or 'tcbs'). Default is 'dnse'.

        Returns
        -------
        pandas.DataFrame
            DataFrame with 'date' as index and columns for each symbol containing close prices.
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        all_data = []

        for symbol in symbols:
            params = PriceDataParams(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                provider=provider,
            )

            price_df = vf.equity.price.historical(
                symbol=params.symbol,
                provider=params.provider,
                start_date=params.start_date.strftime("%Y-%m-%d"),
                end_date=params.end_date.strftime("%Y-%m-%d"),
            ).to_df()

            if price_df is None or price_df.empty:
                continue

            price_df.index = pd.to_datetime(price_df.index, errors="coerce")
            price_df = price_df.sort_index()

            close_df = price_df[["close"]].copy()
            close_df = close_df.rename(columns={"close": symbol})

            all_data.append(close_df)

        if not all_data:
            return pd.DataFrame()

        combined_df = pd.concat(all_data, axis=1).sort_index()
        return combined_df


class PriceDataParams(BaseModel):
    """
    Parameters for fetching historical equity price data.
    """

    symbol: str = Field(..., description="Stock ticker symbol, e.g., 'VNM'")
    start_date: date = Field(..., description="Start date in 'YYYY-MM-DD' format")
    end_date: date = Field(..., description="End date in 'YYYY-MM-DD' format")
    provider: Literal["dnse", "tcbs"] = Field(
        "dnse", description="Data provider ('dnse' or 'tcbs')"
    )

    @validator("end_date")
    def check_date_order(cls, end_date: date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be after start_date")
        return end_date

"""Vietfin data loader for Vietnamese stock market data."""

import pandas as pd
from vietfin import vf
from typing import Union, List
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, validator


class VietfinLoader:
    """Loader for fetching historical close prices using vietfin library."""

    @staticmethod
    def get_close_prices(
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
        """Validate that end_date is after start_date."""
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be after start_date")
        return end_date

from datetime import datetime
from io import BytesIO

import pandas as pd


class PnLProcessor:
    """ """

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._format_col_types()

    @property
    def data(self) -> pd.DataFrame:
        """Read entire set of data.

        Returns:
            Getter for internal DataFrame.
        """
        return self._df

    def run(self):
        self._ensure_columns()
        self.make_statistics()
        self.get_current_positions()

    def make_statistics(self) -> None:
        """Analyze transactions and get statistics on given transactions.
        Calculate required columns, mentioned below, to be able to perform P&L on given data.
        Required columns are: Daily Net, Total Cost, Unit Cost, Removed and Added Cost, Daily Realised
        and Unrealised P&L and Total Unrealised P&L

        Returns:
            None

        Note:
            Mutation of the DataFrame.

            That's not the best approach in therms of readability and performance, but due to the
            time limitations that's the only simple way to meet requirements imposed by recruiter.
        """
        self._df["Added Cost"] = (self._df["Quantity"] * self._df["Price"]).where(
            self._df["Direction"] == "BUY", 0
        )

        for i in self._df.index:
            prev_total_cost = self._df.loc[i - 1, "Total Cost"] if i else 0
            prev_unit_cost = self._df.loc[i - 1, "Unit Cost"] if i else 0

            self._df.loc[i, "Daily Net"] = self._df.loc[:i, "Quantity"].sum()

            added_cost = self._df.loc[i, "Added Cost"]
            qty = self._df.loc[i, "Quantity"]

            # Remove Cost, Total Cost and Unit Cost
            self._df.loc[i, "Removed Cost"] = (
                prev_unit_cost * -qty if prev_unit_cost * -qty > 0 else 0
            )
            self._df.loc[i, "Total Cost"] = (
                added_cost - self._df.loc[i, "Removed Cost"] + prev_total_cost
            )
            self._df.loc[i, "Unit Cost"] = (
                self._df.loc[i, "Total Cost"] / self._df.loc[i, "Daily Net"]
                if self._df.loc[i, "Total Cost"] and self._df.loc[i, "Daily Net"]
                else self._df.loc[i - 1, "UnitCost"]
            )

            # Market Value, Daily Realised P&L, Total Unrealised P&L, Daily Unrealised P&L
            self._df.loc[i, "Market Value"] = (
                self._df.loc[i, "Daily Net"] * self._df.loc[i, "Yahoo Finance"]
            )
            self._df.loc[i, "Daily Realised P&L"] = (
                -self._df.loc[i, "Quantity"] * self._df.loc[i, "Price"]
                - self._df.loc[i, "Removed Cost"]
            )
            self._df.loc[i, "Daily Realised P&L"] = (
                0
                if self._df.loc[i, "Daily Realised P&L"] < 0
                else self._df.loc[i, "Daily Realised P&L"]
            )
            self._df.loc[i, "Total Unrealised P&L"] = (
                self._df.loc[i, "Market Value"] - self._df.loc[i, "Total Cost"]
            )
            self._df.loc[i, "Daily Unrealised P&L"] = (
                self._df.loc[i, "Total Unrealised P&L"]
                + self._df.loc[i, "Daily Realised P&L"]
                - (0 if not i else self._df.loc[i - 1, "Total Unrealised P&L"])
            )

    def _ensure_columns(self) -> None:
        """
        Ensure that all required columns for P&L calculation are in the dataframe
        by initializing them with 0.

        Returns:
            None

        Note:
            Mutation of the DataFrame.
        """
        for col in [
            "Removed Cost",
            "Total Cost",
            "Unit Cost",
            "Market Value",
            "Daily Realised P&L",
            "Total Unrealised P&L",
            "Daily Unrealised P&L",
            "Daily Net",
        ]:
            if col not in self._df.columns:
                self._df[col] = 0

    def get_current_positions(self) -> pd.DataFrame:
        """Get current positions.
        Extract required to conclude on current positions.
        Returns:
            DataFrame containing all data regarding current positions.
        """
        # Drop any rows with missing key values
        self._df = self._df.dropna(
            subset=[
                "Date",
                "Symbol",
                "Daily Net",
                "Total Cost",
                "Unit Cost",
                "Market Value",
                "Daily Realised P&L",
            ]
        )

        # Ensure Date is in datetime format and get the latest
        date = self._df["Date"].max()

        # Get the latest row
        last_row = self._df.iloc[-1]

        # Extract relevant fields
        symbol = last_row["Symbol"]
        today_qty = last_row["Daily Net"]
        total_cost = last_row["Total Cost"]
        unit_cost = last_row["Unit Cost"]
        market_value = last_row["Market Value"]
        yahoo_finance = last_row["Yahoo Finance"]

        # Calculate Total Realised P&L (sum over all rows)
        total_realised = float(self._df["Daily Realised P&L"].sum())

        # Determine direction
        if today_qty > 0:
            direction = "LONG"
        elif today_qty < 0:
            direction = "SHORT"
        else:
            direction = "FLAT"

        return pd.DataFrame(
            [
                {
                    "Date": date,
                    "Symbol": symbol,
                    "Today Qty": today_qty,
                    "Direction": direction,
                    "Total Cost": total_cost,
                    "Unit Cost": unit_cost,
                    "Market Value": market_value,
                    "Total Realised": total_realised,
                    "Yahoo Finance": yahoo_finance,
                }
            ]
        )

    def _format_col_types(self):
        """Format columns to have proper type.
        Returns:
            None
        """
        self._df["Date"] = pd.to_datetime(self._df["Date"], errors="coerce")

    @classmethod
    def from_excel(cls, file: BytesIO) -> "PnLProcessor":
        return cls(pd.read_excel(file))

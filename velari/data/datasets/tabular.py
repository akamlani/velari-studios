import pandas as pd
from   typing import List, Optional


class DatasetTabular(object):
    """Provide static utilities for loading and serialising tabular CSV datasets."""

    @staticmethod
    def load(uri: str, columns: Optional[List[str]] = None, n: Optional[int] = None, **kwargs) -> pd.DataFrame:
        """Load a CSV file into a DataFrame, optionally filtering columns and limiting rows.

        Args:
            uri: Path or URL to the CSV file.
            columns: Subset of column names to load. When None, all columns are returned.
            n: Maximum number of rows to read. When None, the full file is loaded.
            **kwargs: Additional keyword arguments forwarded to ``pd.read_csv``.

        Returns:
            DataFrame containing the requested rows and columns from the CSV source.

        Examples:
            >>> df = DatasetTabular.load("data/catalog/customers.csv")
            >>> df = DatasetTabular.load("data/catalog/sales.csv", columns=["id", "amount"], n=1000)
        """
        params = {'usecols': columns, 'nrows': n}
        params.update(kwargs)
        return pd.read_csv(uri, **{k: v for k, v in params.items() if v is not None})

    @staticmethod
    def to_json(df: pd.DataFrame, columns: List[str]) -> str:
        """Serialise selected columns of a DataFrame to a JSON string.

        Args:
            df: Source DataFrame to serialise.
            columns: Column names to include in the output; other columns are dropped.

        Returns:
            JSON string with records orientation, where each row is a separate JSON object.

        Examples:
            >>> json_str = DatasetTabular.to_json(df, columns=["id", "name", "score"])
        """
        return df[columns].to_json(orient="records")

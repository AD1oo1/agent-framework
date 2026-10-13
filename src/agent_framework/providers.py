from typing import Protocol


class FinancialDataProvider(Protocol):

    def fetch_financial_data(self, company: str) -> dict:
        ...

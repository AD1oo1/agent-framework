from agent_framework.providers import FinancialDataProvider


def test_financial_data_provider_contract():

    class FakeProvider:
        def fetch_financial_data(self, company: str) -> dict:
            return {
                "company": company,
                "revenue": 100,
            }

    provider: FinancialDataProvider = FakeProvider()

    result = provider.fetch_financial_data("Apple")

    assert result["company"] == "Apple"
    assert result["revenue"] == 100

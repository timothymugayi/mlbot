import re
import requests

from abc import abstractmethod, ABC
from typing import Type

from bs4 import BeautifulSoup


PRECISION = 100000000000


class MintLayerApiBase(ABC):
    def __init__(self, base_url: str = "https://api-server.mintlayer.org") -> None:
        self.base_url = base_url

    @abstractmethod
    def get_pool_balance(self, pool_id: str):
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_delegation_balance(self, delegation_id: str):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_coin_price(self, coin_name: str = "mintlayer") -> float:
        if not coin_name:
            raise ValueError("coin_name required param")
        response = requests.get(f"https://coinmarketcap.com/currencies/{coin_name}/")
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        price_pattern = r"\$\d+\.\d+ USD"
        float_prices = []
        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            prices = re.findall(price_pattern, paragraph_text)
            for price in prices:
                float_price = float(re.search(r"\d+\.\d+", price).group())
                float_prices.append(float_price)

        if float_prices:
            return float_prices[0]
        else:
            raise ValueError("No prices found.")


class MintLayerApiStrategy:
    def __init__(self, api_class: Type[MintLayerApiBase]):
        self.api_instance = api_class()

    def get_pool_balance(self, pool_id: str) -> float:
        if not pool_id:
            raise ValueError("pool_id required.")
        return self.api_instance.get_pool_balance(pool_id)

    def get_delegation_balance(self, delegation_id: str) -> float:
        if not delegation_id:
            raise ValueError("pool_id required.")
        return self.api_instance.get_delegation_balance(delegation_id)

    def get_coin_price(self) -> float:
        return self.api_instance.get_coin_price()


class MintLayerV1Api(MintLayerApiBase):
    def __init__(self, base_url="https://api-server.mintlayer.org"):
        super().__init__(base_url)

    def get_pool_balance(self, pool_id) -> float:
        url = f"{self.base_url}/api/v1/pool/{pool_id}"
        response = requests.get(url)
        response.raise_for_status()
        ml_balance = int(response.json()["staker_balance"].get("atoms")) / PRECISION
        return ml_balance

    def get_delegation_balance(self, delegation_id: str) -> float:
        url = f"{self.base_url}/api/v1/delegation/{delegation_id}"
        response = requests.get(url)
        response.raise_for_status()
        ml_balance = int(response.json()["balance"].get("atoms")) / PRECISION
        return ml_balance


class MintLayerV2Api(MintLayerApiBase):
    def __init__(self, base_url="https://api-server.mintlayer.org"):
        super().__init__(base_url)

    def get_pool_balance(self, pool_id: str) -> float:
        url = f"{self.base_url}/api/v2/pool/{pool_id}"
        response = requests.get(url)
        response.raise_for_status()
        ml_balance = int(response.json()["staker_balance"].get("atoms")) / PRECISION
        return ml_balance

    def get_delegation_balance(self, delegation_id: str) -> float:
        url = f"{self.base_url}/api/v2/delegation/{delegation_id}"
        response = requests.get(url)
        response.raise_for_status()
        ml_balance = int(response.json()["balance"].get("atoms")) / PRECISION
        return ml_balance

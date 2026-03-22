import bs4
from httpx import AsyncClient

from x_client_transaction import ClientTransaction
from x_client_transaction import utils


class IClientTransaction:
    home_page_response: bs4.BeautifulSoup | None = None
    client_transaction: ClientTransaction | None = None

    def __init__(self) -> None:
        pass

    async def init(self, session: AsyncClient, headers: dict[str, str]) -> None:
        # GET HOME PAGE RESPONSE
        self.home_page_response = await utils.handle_x_migration_async(session=session)

        # GET ondemand.s FILE RESPONSE
        ondemand_file_url = utils.get_ondemand_file_url(response=self.home_page_response)
        ondemand_file = await session.get(url=ondemand_file_url)
        ondemand_file_response = bs4.BeautifulSoup(ondemand_file.content, 'html.parser')

        self.client_transaction = ClientTransaction(self.home_page_response, ondemand_file_response)

    def generate_transaction_id(
        self,
        method: str,
        path: str,
    ) -> str:
        return self.client_transaction.generate_transaction_id(method, path)

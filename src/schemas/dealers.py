from pydantic import BaseModel


class Dealer(BaseModel):
    name: str

class DealerDb(Dealer):
    id: int
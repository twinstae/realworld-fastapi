from typing import Optional

from pydantic.main import BaseModel

from app.models import IDModelMixin


class BaseItem(IDModelMixin):
    name: str
    price: float
    is_offer: Optional[bool] = None


class ItemInCreate(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

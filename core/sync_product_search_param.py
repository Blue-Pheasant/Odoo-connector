from extendable_pydantic import ExtendableModelMeta

from pydantic import BaseModel


class SyncProductSearchParam(BaseModel, metaclass=ExtendableModelMeta):

    id: int = None
    name: str = None
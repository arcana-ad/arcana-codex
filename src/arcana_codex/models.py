from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class AdUnitsFetchModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: Annotated[str, Field(min_length=2)]

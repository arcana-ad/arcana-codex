from typing import Annotated, Any, Self

from pydantic import BaseModel, Field, model_validator


class Result[T: Any, E: Any](BaseModel):
    value: Annotated[T | None, Field(default=None)]
    error: Annotated[E | None, Field(default=None)]

    @model_validator(mode="after")
    def check_mutual_exclusion_of_value_and_error(self) -> Self:
        if self.value is None and self.error is None:
            raise ValueError("Either 'value' or 'error' must be set in a Result.")

        if self.value is not None and self.error is not None:
            raise ValueError(
                "Both 'value' and 'error' cannot be set in a Result simultaneously."
            )

        return self

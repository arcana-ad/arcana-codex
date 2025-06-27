from typing import Annotated, Any, Generic, Self, TypeVar

from pydantic import BaseModel, Field, model_validator

# TODO: Remove this when minimum supported version becomes >=3.12
T = TypeVar("T", bound=Any)
E = TypeVar("E", bound=Any)


# TODO: Replace class definition to 'class Result[T: Any, E: Any](BaseModel):' when minimum supported version becomes >=3.12
class Result(BaseModel, Generic[T, E]):
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

from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Result(Generic[T]):
    """
    Represents the outcome of an operation that can either succeed or fail.
    Eliminates the need for try/except at the call site and makes
    error handling explicit in the type signature.
    """

    def __init__(self, value: Optional[T] = None, error: Optional[str] = None):
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    @property
    def value(self) -> T:
        if self._error:
            raise ValueError(f"Result is a failure: {self._error}")
        return self._value # type: ignore[return-value]

    @property
    def error(self) -> str:
        return self._error or ""

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(error=error)

    def __repr__(self) -> str:
        if self.is_success:
            return f"Result.success({self._value})"
        return f"Result.failure({self._error})"

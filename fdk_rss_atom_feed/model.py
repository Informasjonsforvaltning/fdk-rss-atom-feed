from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class SearchFilter(Generic[T]):
    value: T | None = None


@dataclass
class Filters:
    openData: SearchFilter[bool] | None = None
    orgPath: SearchFilter[str] | None = None
    accessRights: SearchFilter[str] | None = None
    dataTheme: SearchFilter[List[str]] | None = None
    losTheme: SearchFilter[List[str]] | None = None
    spatial: SearchFilter[List[str]] | None = None
    provenance: SearchFilter[str] | None = None
    formats: SearchFilter[List[str]] | None = None
    uri: SearchFilter[List[str]] | None = None
    lastXDaysModified: SearchFilter[int] | None = None


@dataclass
class Sort:
    field: str = "FIRST_HARVESTED"
    direction: str = "DESC"


@dataclass
class Pagination:
    page: int = 0
    size: int = 10


@dataclass
class SearchOperation:
    query: str | None = None
    filters: Filters | None = None
    sort: Sort | None = None
    pagination: Pagination | None = None


class BadParamError(ValueError):
    """Raised when an invalid parameter is passed to the API."""

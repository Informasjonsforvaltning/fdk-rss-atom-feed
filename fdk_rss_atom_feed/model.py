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
    lastXDays: SearchFilter[int] | None = None


@dataclass
class Sort:
    field: str = "FIRST_HARVESTED"
    direction: str = "DESC"


@dataclass
class Pagination:
    page: int = 0
    size: int = 100


@dataclass
class SearchOperation:
    query: str | None = None
    filters: Filters = Filters()
    sort: Sort | None = None
    pagination: Pagination | None = Pagination(page=0, size=100)

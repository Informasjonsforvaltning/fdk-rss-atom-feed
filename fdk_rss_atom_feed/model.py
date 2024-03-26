from typing import Generic, TypeVar
from pydantic.dataclasses import dataclass

T = TypeVar("T")


@dataclass
class SearchFilter(Generic[T]):
    value: T | None = None


@dataclass
class Filters:
    openData: SearchFilter[bool] | None = None
    orgPath: SearchFilter[str] | None = None
    accessRights: SearchFilter[str] | None = None
    dataTheme: SearchFilter[list[str]] | None = None
    losTheme: SearchFilter[list[str]] | None = None
    spatial: SearchFilter[list[str]] | None = None
    provenance: SearchFilter[str] | None = None
    formats: SearchFilter[list[str]] | None = None
    uri: SearchFilter[list[str]] | None = None
    lastXDays: SearchFilter[int] | None = SearchFilter(value=1)


@dataclass
class Fields:
    title: bool = True
    description: bool = True
    keyword: bool = True


@dataclass
class Sort:
    field: str = "FIRST_HARVESTED"
    direction: str = "DESC"


@dataclass
class SearchOperation:
    query: str | None = None
    filters: Filters = Filters()
    fields: Fields = Fields()

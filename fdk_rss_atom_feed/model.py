from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SearchFilter(BaseModel, Generic[T]):
    value: T | None = None


class Filters(BaseModel):
    openData: SearchFilter[bool] | None = None
    orgPath: SearchFilter[str] | None = None
    accessRights: SearchFilter[str] | None = None
    dataTheme: SearchFilter[list[str]] | None = None
    losTheme: SearchFilter[list[str]] | None = None
    spatial: SearchFilter[list[str]] | None = None
    provenance: SearchFilter[str] | None = None
    formats: SearchFilter[list[str]] | None = None
    uri: SearchFilter[list[str]] | None = None
    lastXDays: SearchFilter[int] | None = None


class Fields(BaseModel):
    title: bool = True
    description: bool = True
    keyword: bool = True


class Sort(BaseModel):
    field: str = "FIRST_HARVESTED"
    direction: str = "DESC"


class SearchOperation(BaseModel):
    query: str | None = None
    filters: Filters = Filters()
    fields: Fields = Fields()

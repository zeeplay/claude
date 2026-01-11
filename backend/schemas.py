from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# Book Schemas
class BookBase(BaseModel):
    name: str
    author: Optional[str] = None
    downloaded: Optional[str] = None
    status: Optional[str] = "want_to_read"
    rating: Optional[float] = Field(None, ge=0, le=10)
    type: Optional[str] = None
    date_read: Optional[date] = None
    format: Optional[str] = None
    notes: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    downloaded: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    type: Optional[str] = None
    date_read: Optional[date] = None
    format: Optional[str] = None
    notes: Optional[str] = None


class BookResponse(BookBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Movie Schemas
class MovieBase(BaseModel):
    title: str
    director: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = "want_to_watch"
    rating: Optional[float] = Field(None, ge=0, le=10)
    genre: Optional[str] = None
    year: Optional[int] = None
    date_watched: Optional[date] = None
    notes: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    genre: Optional[str] = None
    year: Optional[int] = None
    date_watched: Optional[date] = None
    notes: Optional[str] = None


class MovieResponse(MovieBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Query Schema
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    results: Optional[list] = None


# General Notes Schemas
class GeneralNotesBase(BaseModel):
    content: str


class GeneralNotesCreate(GeneralNotesBase):
    pass


class GeneralNotesUpdate(BaseModel):
    content: str


class GeneralNotesResponse(GeneralNotesBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class MediaType(str, enum.Enum):
    BOOK = "book"
    MOVIE = "movie"


class Status(str, enum.Enum):
    WANT_TO_READ = "want_to_read"
    READING = "reading"
    READ = "read"
    WANT_TO_WATCH = "want_to_watch"
    WATCHING = "watching"
    WATCHED = "watched"


class BookType(str, enum.Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False, index=True)
    author = Column(String(300), index=True)
    downloaded = Column(String(100))  # Source like Kindle, Google Books, etc.
    status = Column(String(50), default="want_to_read")
    rating = Column(Float)  # Rating out of 10
    type = Column(String(50))  # Fiction or Non-fiction
    date_read = Column(Date)
    format = Column(String(50))  # Text, Audio, etc.
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    director = Column(String(300), index=True)
    source = Column(String(100))  # Netflix, Prime, etc.
    status = Column(String(50), default="want_to_watch")
    rating = Column(Float)  # Rating out of 10
    genre = Column(String(100))
    year = Column(Integer)
    date_watched = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class GeneralNotes(Base):
    __tablename__ = "general_notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

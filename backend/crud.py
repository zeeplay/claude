from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from models import Book, Movie
from schemas import BookCreate, BookUpdate, MovieCreate, MovieUpdate
from typing import Optional, List
from datetime import date


# Book CRUD operations
def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Book]:
    query = db.query(Book)

    if status:
        # Handle multiple statuses separated by comma
        statuses = [s.strip() for s in status.split(',')]
        query = query.filter(Book.status.in_(statuses))
    if type:
        query = query.filter(Book.type == type)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.name.ilike(search_term),
                Book.author.ilike(search_term),
                Book.notes.ilike(search_term),
            )
        )

    return query.order_by(Book.created_at.desc()).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    db_book = get_book(db, book_id)
    if db_book:
        update_data = book.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


# Movie CRUD operations
def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
    return db.query(Movie).filter(Movie.id == movie_id).first()


def get_movies(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Movie]:
    query = db.query(Movie)

    if status:
        # Handle multiple statuses separated by comma
        statuses = [s.strip() for s in status.split(',')]
        query = query.filter(Movie.status.in_(statuses))
    if genre:
        query = query.filter(Movie.genre == genre)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Movie.title.ilike(search_term),
                Movie.director.ilike(search_term),
                Movie.notes.ilike(search_term),
            )
        )

    return query.order_by(Movie.created_at.desc()).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: MovieCreate) -> Movie:
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie_id: int, movie: MovieUpdate) -> Optional[Movie]:
    db_movie = get_movie(db, movie_id)
    if db_movie:
        update_data = movie.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int) -> bool:
    db_movie = get_movie(db, movie_id)
    if db_movie:
        db.delete(db_movie)
        db.commit()
        return True
    return False


# Statistics and Query helpers
def get_book_stats(db: Session) -> dict:
    total = db.query(func.count(Book.id)).scalar()
    read = db.query(func.count(Book.id)).filter(Book.status == "read").scalar()
    reading = db.query(func.count(Book.id)).filter(Book.status == "reading").scalar()
    want_to_read = db.query(func.count(Book.id)).filter(Book.status == "want_to_read").scalar()
    avg_rating = db.query(func.avg(Book.rating)).filter(Book.rating.isnot(None)).scalar()
    fiction = db.query(func.count(Book.id)).filter(Book.type == "fiction").scalar()
    non_fiction = db.query(func.count(Book.id)).filter(Book.type == "non-fiction").scalar()

    return {
        "total": total,
        "read": read,
        "reading": reading,
        "want_to_read": want_to_read,
        "average_rating": round(avg_rating, 1) if avg_rating else None,
        "fiction": fiction,
        "non_fiction": non_fiction,
    }


def get_movie_stats(db: Session) -> dict:
    total = db.query(func.count(Movie.id)).scalar()
    watched = db.query(func.count(Movie.id)).filter(Movie.status == "watched").scalar()
    watching = db.query(func.count(Movie.id)).filter(Movie.status == "watching").scalar()
    want_to_watch = db.query(func.count(Movie.id)).filter(Movie.status == "want_to_watch").scalar()
    avg_rating = db.query(func.avg(Movie.rating)).filter(Movie.rating.isnot(None)).scalar()

    return {
        "total": total,
        "watched": watched,
        "watching": watching,
        "want_to_watch": want_to_watch,
        "average_rating": round(avg_rating, 1) if avg_rating else None,
    }


def get_top_rated_books(db: Session, limit: int = 5) -> List[Book]:
    return db.query(Book).filter(Book.rating.isnot(None)).order_by(Book.rating.desc()).limit(limit).all()


def get_top_rated_movies(db: Session, limit: int = 5) -> List[Movie]:
    return db.query(Movie).filter(Movie.rating.isnot(None)).order_by(Movie.rating.desc()).limit(limit).all()


def get_books_by_author(db: Session, author: str) -> List[Book]:
    return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()


def get_movies_by_director(db: Session, director: str) -> List[Movie]:
    return db.query(Movie).filter(Movie.director.ilike(f"%{director}%")).all()


def get_recent_reads(db: Session, limit: int = 10) -> List[Book]:
    return db.query(Book).filter(Book.date_read.isnot(None)).order_by(Book.date_read.desc()).limit(limit).all()


def get_recent_watches(db: Session, limit: int = 10) -> List[Movie]:
    return db.query(Movie).filter(Movie.date_watched.isnot(None)).order_by(Movie.date_watched.desc()).limit(limit).all()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db, Base
from models import Book, Movie
from schemas import (
    BookCreate,
    BookUpdate,
    BookResponse,
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    QueryRequest,
    QueryResponse,
)
import crud
from query_parser import NaturalLanguageQueryParser

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Tracker API",
    description="Track your books and movies with natural language querying",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/")
def root():
    return {"message": "Media Tracker API", "version": "1.0.0"}


# Book endpoints
@app.get("/api/books", response_model=List[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, status=status, type=type, search=search)


@app.get("/api/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/api/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.put("/api/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if not crud.delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


# Movie endpoints
@app.get("/api/movies", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_movies(db, skip=skip, limit=limit, status=status, genre=genre, search=search)


@app.get("/api/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/api/movies", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)


@app.put("/api/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    updated = crud.update_movie(db, movie_id, movie)
    if not updated:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated


@app.delete("/api/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    if not crud.delete_movie(db, movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}


# Statistics endpoints
@app.get("/api/stats/books")
def get_book_stats(db: Session = Depends(get_db)):
    return crud.get_book_stats(db)


@app.get("/api/stats/movies")
def get_movie_stats(db: Session = Depends(get_db)):
    return crud.get_movie_stats(db)


@app.get("/api/stats")
def get_all_stats(db: Session = Depends(get_db)):
    return {"books": crud.get_book_stats(db), "movies": crud.get_movie_stats(db)}


# Natural Language Query endpoint
@app.post("/api/query", response_model=QueryResponse)
def query(request: QueryRequest, db: Session = Depends(get_db)):
    parser = NaturalLanguageQueryParser(db)
    answer, results = parser.parse_and_execute(request.question)

    # Convert results to serializable format
    serialized_results = []
    for item in results:
        if isinstance(item, Book):
            serialized_results.append(
                {
                    "type": "book",
                    "id": item.id,
                    "name": item.name,
                    "author": item.author,
                    "rating": item.rating,
                    "status": item.status,
                    "book_type": item.type,
                    "date_read": str(item.date_read) if item.date_read else None,
                    "notes": item.notes,
                }
            )
        elif isinstance(item, Movie):
            serialized_results.append(
                {
                    "type": "movie",
                    "id": item.id,
                    "title": item.title,
                    "director": item.director,
                    "rating": item.rating,
                    "status": item.status,
                    "genre": item.genre,
                    "date_watched": str(item.date_watched) if item.date_watched else None,
                    "notes": item.notes,
                }
            )

    return QueryResponse(answer=answer, results=serialized_results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

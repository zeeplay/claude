"""
Seed script to populate the database with sample data.
Run this after setting up the database to add sample books and movies.
"""

from datetime import date
from database import SessionLocal, engine, Base
from models import Book, Movie

# Create tables
Base.metadata.create_all(bind=engine)

# Sample books (based on the provided Notion data)
sample_books = [
    {
        "name": "Lessons in Chemistry",
        "author": "Bonnie Garmus",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 10,
        "type": "fiction",
        "date_read": date(2023, 6, 1),
        "format": "text",
        "notes": "Absolutely loved this book! Great protagonist and witty writing."
    },
    {
        "name": "Atmosphere",
        "author": "Taylor Jenkins Reid",
        "downloaded": "Google books",
        "status": "read",
        "rating": 10,
        "type": "fiction",
        "date_read": date(2025, 12, 25),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Art as Therapy",
        "author": "Alain de Botton and John Armstrong",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2025, 11, 15),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Lola and the Mirror",
        "author": "Trent Dalton",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 9,
        "type": "fiction",
        "date_read": date(2024, 9, 29),
        "format": None,
        "notes": ""
    },
    {
        "name": "Good Material",
        "author": "Dolly Alderton",
        "downloaded": "Google books",
        "status": "read",
        "rating": 9,
        "type": "fiction",
        "date_read": date(2025, 10, 25),
        "format": "text",
        "notes": ""
    },
    {
        "name": "The Emperor of Gladness",
        "author": "Ocean Vuong",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 9,
        "type": "fiction",
        "date_read": date(2025, 9, 21),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Continuous Discovery",
        "author": "Teresa Torres",
        "downloaded": "Google books",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2023, 11, 8),
        "format": None,
        "notes": ""
    },
    {
        "name": "Lean UX",
        "author": "Jeff Gothelf & Josh Seiden",
        "downloaded": "Google books",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2023, 6, 25),
        "format": None,
        "notes": ""
    },
    {
        "name": "Good Anger",
        "author": "Sam Parker",
        "downloaded": "BorrowBox",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2025, 9, 9),
        "format": "text",
        "notes": ""
    },
    {
        "name": "The Beginning of Infinity",
        "author": "David Deutsch",
        "downloaded": "Google books",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2025, 8, 24),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Why Greatness Cannot Be Planned",
        "author": "Kenneth Stanley, Joel Lehman",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 9,
        "type": "non-fiction",
        "date_read": date(2026, 1, 1),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Never Let Me Go",
        "author": "Kazuo Ishiguro",
        "downloaded": "Spotify",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2024, 12, 24),
        "format": None,
        "notes": ""
    },
    {
        "name": "So Late in the Day",
        "author": "Claire Keegan",
        "downloaded": "Everand",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2024, 9, 3),
        "format": None,
        "notes": ""
    },
    {
        "name": "The Three-Body Problem",
        "author": "Cixin Liu",
        "downloaded": "Google books",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2024, 3, 6),
        "format": None,
        "notes": ""
    },
    {
        "name": "Exhalation: Stories",
        "author": "Ted Chiang",
        "downloaded": "Google books",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2023, 12, 23),
        "format": None,
        "notes": ""
    },
    {
        "name": "Snow Flake",
        "author": "Louise Nealon",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2021, 1, 1),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Birnam Wood",
        "author": "Eleanor Catton",
        "downloaded": "Kindle",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2024, 3, 17),
        "format": None,
        "notes": ""
    },
    {
        "name": "Eleanor Oliphant is Completely Fine",
        "author": "Gail Honeyman",
        "downloaded": "BorrowBox",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2025, 4, 7),
        "format": "text",
        "notes": ""
    },
    {
        "name": "Death's End",
        "author": "Cixin Liu",
        "downloaded": "Google books",
        "status": "read",
        "rating": 8,
        "type": "fiction",
        "date_read": date(2024, 8, 14),
        "format": None,
        "notes": ""
    },
]

# Sample movies
sample_movies = [
    {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "source": "Netflix",
        "status": "watched",
        "rating": 10,
        "genre": "Drama",
        "year": 1994,
        "date_watched": date(2024, 5, 15),
        "notes": "A masterpiece of cinema."
    },
    {
        "title": "Inception",
        "director": "Christopher Nolan",
        "source": "Prime",
        "status": "watched",
        "rating": 9,
        "genre": "Sci-Fi",
        "year": 2010,
        "date_watched": date(2024, 3, 20),
        "notes": "Mind-bending and visually stunning."
    },
    {
        "title": "Parasite",
        "director": "Bong Joon-ho",
        "source": "Cinema",
        "status": "watched",
        "rating": 9,
        "genre": "Thriller",
        "year": 2019,
        "date_watched": date(2023, 8, 10),
        "notes": ""
    },
    {
        "title": "Dune: Part Two",
        "director": "Denis Villeneuve",
        "source": "Cinema",
        "status": "want_to_watch",
        "rating": None,
        "genre": "Sci-Fi",
        "year": 2024,
        "date_watched": None,
        "notes": ""
    },
    {
        "title": "Everything Everywhere All at Once",
        "director": "Daniel Kwan, Daniel Scheinert",
        "source": "Prime",
        "status": "watched",
        "rating": 8,
        "genre": "Action/Comedy",
        "year": 2022,
        "date_watched": date(2023, 6, 5),
        "notes": "Creative and emotional."
    },
]


def seed_database():
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_books = db.query(Book).count()
        existing_movies = db.query(Movie).count()

        if existing_books > 0 or existing_movies > 0:
            print(f"Database already has {existing_books} books and {existing_movies} movies.")
            response = input("Do you want to add sample data anyway? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed data.")
                return

        # Add books
        for book_data in sample_books:
            book = Book(**book_data)
            db.add(book)

        # Add movies
        for movie_data in sample_movies:
            movie = Movie(**movie_data)
            db.add(movie)

        db.commit()
        print(f"Successfully added {len(sample_books)} books and {len(sample_movies)} movies!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

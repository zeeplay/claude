import re
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from models import Book, Movie
from typing import Tuple, List, Any
import crud


class NaturalLanguageQueryParser:
    """
    Parses natural language questions about books and movies
    and returns relevant data from the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def parse_and_execute(self, question: str) -> Tuple[str, List[Any]]:
        """
        Parse the question and return an answer with relevant results.
        """
        question_lower = question.lower().strip()

        # Check for different types of queries
        if self._is_count_query(question_lower):
            return self._handle_count_query(question_lower)
        elif self._is_rating_query(question_lower):
            return self._handle_rating_query(question_lower)
        elif self._is_recommendation_query(question_lower):
            return self._handle_recommendation_query(question_lower)
        elif self._is_author_query(question_lower):
            return self._handle_author_query(question_lower)
        elif self._is_director_query(question_lower):
            return self._handle_director_query(question_lower)
        elif self._is_status_query(question_lower):
            return self._handle_status_query(question_lower)
        elif self._is_recent_query(question_lower):
            return self._handle_recent_query(question_lower)
        elif self._is_type_query(question_lower):
            return self._handle_type_query(question_lower)
        elif self._is_stats_query(question_lower):
            return self._handle_stats_query(question_lower)
        elif self._is_search_query(question_lower):
            return self._handle_search_query(question_lower, question)
        else:
            return self._handle_general_search(question_lower, question)

    def _is_count_query(self, q: str) -> bool:
        patterns = [
            r"how many",
            r"count",
            r"number of",
            r"total",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_rating_query(self, q: str) -> bool:
        patterns = [
            r"(best|top|highest).*(rated|rating)",
            r"(worst|lowest).*(rated|rating)",
            r"rating (above|below|over|under)",
            r"rated (above|below|over|under)",
            r"what.*(rating|rated)",
            r"favorite",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_recommendation_query(self, q: str) -> bool:
        patterns = [
            r"recommend",
            r"suggest",
            r"should i (read|watch)",
            r"what.*(should|could).*(read|watch)",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_author_query(self, q: str) -> bool:
        patterns = [
            r"(by|from|written by)\s+\w+",
            r"author",
            r"books by",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_director_query(self, q: str) -> bool:
        patterns = [
            r"directed by",
            r"director",
            r"movies by",
            r"films by",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_status_query(self, q: str) -> bool:
        patterns = [
            r"(currently|now) (reading|watching)",
            r"want to (read|watch)",
            r"to (read|watch) list",
            r"finished",
            r"completed",
            r"unread",
            r"unwatched",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_recent_query(self, q: str) -> bool:
        patterns = [
            r"recent(ly)?",
            r"last",
            r"latest",
            r"this (year|month|week)",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_type_query(self, q: str) -> bool:
        patterns = [
            r"fiction",
            r"non-?fiction",
            r"genre",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_stats_query(self, q: str) -> bool:
        patterns = [
            r"statistic",
            r"summary",
            r"overview",
            r"average",
        ]
        return any(re.search(p, q) for p in patterns)

    def _is_search_query(self, q: str) -> bool:
        patterns = [
            r"(find|search|look for|where is)",
            r"do i have",
            r"have i (read|watched)",
        ]
        return any(re.search(p, q) for p in patterns)

    def _handle_count_query(self, q: str) -> Tuple[str, List[Any]]:
        is_book = "book" in q
        is_movie = "movie" in q or "film" in q

        results = []
        answers = []

        if is_book or (not is_movie):
            stats = crud.get_book_stats(self.db)
            if "read" in q and "want" not in q:
                answers.append(f"You have read {stats['read']} books.")
            elif "want" in q or "to read" in q:
                answers.append(f"You have {stats['want_to_read']} books on your want to read list.")
            elif "fiction" in q and "non" not in q:
                answers.append(f"You have {stats['fiction']} fiction books.")
            elif "non" in q and "fiction" in q:
                answers.append(f"You have {stats['non_fiction']} non-fiction books.")
            else:
                answers.append(f"You have {stats['total']} books in total ({stats['read']} read, {stats['reading']} reading, {stats['want_to_read']} want to read).")

        if is_movie or (not is_book):
            stats = crud.get_movie_stats(self.db)
            if "watch" in q and "want" not in q:
                answers.append(f"You have watched {stats['watched']} movies.")
            elif "want" in q or "to watch" in q:
                answers.append(f"You have {stats['want_to_watch']} movies on your want to watch list.")
            else:
                answers.append(f"You have {stats['total']} movies in total ({stats['watched']} watched, {stats['watching']} watching, {stats['want_to_watch']} want to watch).")

        return " ".join(answers), results

    def _handle_rating_query(self, q: str) -> Tuple[str, List[Any]]:
        is_book = "book" in q
        is_movie = "movie" in q or "film" in q

        # Check for specific rating thresholds
        threshold_match = re.search(r"(above|below|over|under|at least|higher than|lower than)\s*(\d+)", q)

        if threshold_match:
            direction = threshold_match.group(1)
            threshold = float(threshold_match.group(2))

            if direction in ["above", "over", "at least", "higher than"]:
                if is_book or not is_movie:
                    results = self.db.query(Book).filter(Book.rating >= threshold).order_by(Book.rating.desc()).all()
                    return f"Found {len(results)} books rated {threshold} or higher.", results
                else:
                    results = self.db.query(Movie).filter(Movie.rating >= threshold).order_by(Movie.rating.desc()).all()
                    return f"Found {len(results)} movies rated {threshold} or higher.", results
            else:
                if is_book or not is_movie:
                    results = self.db.query(Book).filter(Book.rating <= threshold).order_by(Book.rating.asc()).all()
                    return f"Found {len(results)} books rated {threshold} or lower.", results
                else:
                    results = self.db.query(Movie).filter(Movie.rating <= threshold).order_by(Movie.rating.asc()).all()
                    return f"Found {len(results)} movies rated {threshold} or lower.", results

        # Top/best rated
        if any(word in q for word in ["best", "top", "highest", "favorite"]):
            limit = 5
            num_match = re.search(r"(\d+)", q)
            if num_match:
                limit = int(num_match.group(1))

            answers = []
            all_results = []

            if is_book or (not is_movie):
                books = crud.get_top_rated_books(self.db, limit)
                if books:
                    book_list = ", ".join([f'"{b.name}" ({b.rating}/10)' for b in books[:3]])
                    answers.append(f"Your top rated books include: {book_list}")
                    all_results.extend(books)

            if is_movie or (not is_book):
                movies = crud.get_top_rated_movies(self.db, limit)
                if movies:
                    movie_list = ", ".join([f'"{m.title}" ({m.rating}/10)' for m in movies[:3]])
                    answers.append(f"Your top rated movies include: {movie_list}")
                    all_results.extend(movies)

            return " ".join(answers) if answers else "No rated items found.", all_results

        # Worst/lowest rated
        if any(word in q for word in ["worst", "lowest"]):
            if is_book or not is_movie:
                results = self.db.query(Book).filter(Book.rating.isnot(None)).order_by(Book.rating.asc()).limit(5).all()
                if results:
                    return f"Your lowest rated books: {', '.join([f'{b.name} ({b.rating}/10)' for b in results])}", results
            else:
                results = self.db.query(Movie).filter(Movie.rating.isnot(None)).order_by(Movie.rating.asc()).limit(5).all()
                if results:
                    return f"Your lowest rated movies: {', '.join([f'{m.title} ({m.rating}/10)' for m in results])}", results

        return "I couldn't understand the rating query. Try asking about 'top rated books' or 'movies rated above 8'.", []

    def _handle_recommendation_query(self, q: str) -> Tuple[str, List[Any]]:
        is_book = "book" in q or "read" in q
        is_movie = "movie" in q or "watch" in q or "film" in q

        if is_book:
            # Recommend from want to read list with high expected value
            books = self.db.query(Book).filter(Book.status == "want_to_read").all()
            if books:
                return f"From your reading list, you might enjoy: {', '.join([b.name for b in books[:5]])}. You have {len(books)} books waiting!", books[:5]
            return "Your reading list is empty! Add some books you want to read.", []

        if is_movie:
            movies = self.db.query(Movie).filter(Movie.status == "want_to_watch").all()
            if movies:
                return f"From your watchlist, consider: {', '.join([m.title for m in movies[:5]])}. You have {len(movies)} movies waiting!", movies[:5]
            return "Your watchlist is empty! Add some movies you want to watch.", []

        return "What would you like recommendations for - books or movies?", []

    def _handle_author_query(self, q: str) -> Tuple[str, List[Any]]:
        # Extract author name
        patterns = [
            r"(?:by|from|written by|author)\s+([a-zA-Z\s]+?)(?:\?|$|\.|\,)",
            r"books?\s+(?:by|from)\s+([a-zA-Z\s]+?)(?:\?|$|\.|\,)",
        ]

        for pattern in patterns:
            match = re.search(pattern, q)
            if match:
                author = match.group(1).strip()
                books = crud.get_books_by_author(self.db, author)
                if books:
                    return f"Found {len(books)} books by {author}: {', '.join([b.name for b in books])}", books
                return f"No books found by {author}.", []

        # List all authors
        authors = self.db.query(Book.author).filter(Book.author.isnot(None)).distinct().all()
        author_list = [a[0] for a in authors if a[0]]
        return f"Authors in your collection: {', '.join(author_list[:20])}", []

    def _handle_director_query(self, q: str) -> Tuple[str, List[Any]]:
        patterns = [
            r"(?:directed by|director|by)\s+([a-zA-Z\s]+?)(?:\?|$|\.|\,)",
            r"movies?\s+(?:by|from)\s+([a-zA-Z\s]+?)(?:\?|$|\.|\,)",
        ]

        for pattern in patterns:
            match = re.search(pattern, q)
            if match:
                director = match.group(1).strip()
                movies = crud.get_movies_by_director(self.db, director)
                if movies:
                    return f"Found {len(movies)} movies by {director}: {', '.join([m.title for m in movies])}", movies
                return f"No movies found by {director}.", []

        directors = self.db.query(Movie.director).filter(Movie.director.isnot(None)).distinct().all()
        director_list = [d[0] for d in directors if d[0]]
        return f"Directors in your collection: {', '.join(director_list[:20])}", []

    def _handle_status_query(self, q: str) -> Tuple[str, List[Any]]:
        if "currently reading" in q or "now reading" in q:
            books = self.db.query(Book).filter(Book.status == "reading").all()
            if books:
                return f"Currently reading: {', '.join([b.name for b in books])}", books
            return "You're not currently reading any books.", []

        if "currently watching" in q or "now watching" in q:
            movies = self.db.query(Movie).filter(Movie.status == "watching").all()
            if movies:
                return f"Currently watching: {', '.join([m.title for m in movies])}", movies
            return "You're not currently watching any movies.", []

        if "want to read" in q or "to read list" in q:
            books = self.db.query(Book).filter(Book.status == "want_to_read").all()
            return f"Want to read ({len(books)} books): {', '.join([b.name for b in books[:10]])}", books

        if "want to watch" in q or "to watch list" in q:
            movies = self.db.query(Movie).filter(Movie.status == "want_to_watch").all()
            return f"Want to watch ({len(movies)} movies): {', '.join([m.title for m in movies[:10]])}", movies

        return "Try asking about 'currently reading', 'want to read list', etc.", []

    def _handle_recent_query(self, q: str) -> Tuple[str, List[Any]]:
        is_book = "book" in q or "read" in q
        is_movie = "movie" in q or "watch" in q or "film" in q

        answers = []
        all_results = []

        if is_book or (not is_movie):
            books = crud.get_recent_reads(self.db, 5)
            if books:
                book_list = ", ".join([f'"{b.name}"' for b in books])
                answers.append(f"Recently read books: {book_list}")
                all_results.extend(books)

        if is_movie or (not is_book):
            movies = crud.get_recent_watches(self.db, 5)
            if movies:
                movie_list = ", ".join([f'"{m.title}"' for m in movies])
                answers.append(f"Recently watched movies: {movie_list}")
                all_results.extend(movies)

        return " ".join(answers) if answers else "No recent activity found.", all_results

    def _handle_type_query(self, q: str) -> Tuple[str, List[Any]]:
        if "non" in q and "fiction" in q:
            books = self.db.query(Book).filter(Book.type == "non-fiction").all()
            return f"Non-fiction books ({len(books)}): {', '.join([b.name for b in books[:10]])}", books

        if "fiction" in q:
            books = self.db.query(Book).filter(Book.type == "fiction").all()
            return f"Fiction books ({len(books)}): {', '.join([b.name for b in books[:10]])}", books

        # Handle movie genres
        genre_match = re.search(r"genre[:\s]+(\w+)", q)
        if genre_match:
            genre = genre_match.group(1)
            movies = self.db.query(Movie).filter(Movie.genre.ilike(f"%{genre}%")).all()
            return f"{genre.title()} movies ({len(movies)}): {', '.join([m.title for m in movies[:10]])}", movies

        return "Try asking about 'fiction books', 'non-fiction books', or movies by genre.", []

    def _handle_stats_query(self, q: str) -> Tuple[str, List[Any]]:
        book_stats = crud.get_book_stats(self.db)
        movie_stats = crud.get_movie_stats(self.db)

        answer = f"""Library Statistics:
📚 Books: {book_stats['total']} total ({book_stats['read']} read, {book_stats['reading']} reading, {book_stats['want_to_read']} to read)
   - Fiction: {book_stats['fiction']}, Non-fiction: {book_stats['non_fiction']}
   - Average rating: {book_stats['average_rating'] or 'N/A'}/10

🎬 Movies: {movie_stats['total']} total ({movie_stats['watched']} watched, {movie_stats['watching']} watching, {movie_stats['want_to_watch']} to watch)
   - Average rating: {movie_stats['average_rating'] or 'N/A'}/10"""

        return answer, []

    def _handle_search_query(self, q: str, original: str) -> Tuple[str, List[Any]]:
        # Extract search term
        patterns = [
            r"(?:find|search|look for|where is)\s+['\"]?([^'\"]+)['\"]?",
            r"do i have\s+['\"]?([^'\"]+)['\"]?",
            r"have i (?:read|watched)\s+['\"]?([^'\"]+)['\"]?",
        ]

        search_term = None
        for pattern in patterns:
            match = re.search(pattern, q)
            if match:
                search_term = match.group(1).strip()
                break

        if not search_term:
            # Use words after common keywords
            words = q.replace("?", "").split()
            keywords = ["find", "search", "for", "have", "is"]
            for i, word in enumerate(words):
                if word in keywords and i + 1 < len(words):
                    search_term = " ".join(words[i + 1 :])
                    break

        if search_term:
            return self._search_all(search_term)

        return "What would you like to search for?", []

    def _handle_general_search(self, q: str, original: str) -> Tuple[str, List[Any]]:
        # Try to extract any meaningful words and search
        # Remove common words
        stop_words = {
            "what",
            "which",
            "where",
            "when",
            "how",
            "is",
            "are",
            "the",
            "a",
            "an",
            "my",
            "i",
            "me",
            "have",
            "has",
            "do",
            "does",
            "did",
            "about",
            "can",
            "could",
            "would",
            "should",
            "tell",
            "show",
            "list",
        }

        words = re.findall(r"\b\w+\b", q.lower())
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]

        if meaningful_words:
            search_term = " ".join(meaningful_words[:3])
            return self._search_all(search_term)

        return "I'm not sure what you're looking for. Try asking about your books, movies, ratings, or search for a specific title.", []

    def _search_all(self, term: str) -> Tuple[str, List[Any]]:
        books = crud.get_books(self.db, search=term, limit=10)
        movies = crud.get_movies(self.db, search=term, limit=10)

        results = []
        answers = []

        if books:
            answers.append(f"Found {len(books)} book(s): {', '.join([b.name for b in books])}")
            results.extend(books)

        if movies:
            answers.append(f"Found {len(movies)} movie(s): {', '.join([m.title for m in movies])}")
            results.extend(movies)

        if not answers:
            return f"No results found for '{term}'.", []

        return " ".join(answers), results

# Media Tracker

A personal book and movie tracking application with a natural language query interface. Keep track of what you've read and watched, add notes, and ask questions about your library.

## Features

- **Track Books & Movies**: Store details like title, author/director, rating, status, and more
- **Notes**: Add personal notes, quotes, or thoughts to each entry
- **Natural Language Queries**: Ask questions like "What are my top rated books?" or "How many fiction books have I read?"
- **Filtering & Search**: Filter by status, type, and search across your library
- **Statistics Dashboard**: See your reading/watching stats at a glance

## Tech Stack

- **Backend**: Python FastAPI with SQLite database
- **Frontend**: React with modern CSS
- **Query Engine**: Custom natural language parser for database queries

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Seed the database with sample data:
   ```bash
   python seed_data.py
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Books
- `GET /api/books` - List all books (with optional filters)
- `GET /api/books/{id}` - Get a specific book
- `POST /api/books` - Create a new book
- `PUT /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book

### Movies
- `GET /api/movies` - List all movies (with optional filters)
- `GET /api/movies/{id}` - Get a specific movie
- `POST /api/movies` - Create a new movie
- `PUT /api/movies/{id}` - Update a movie
- `DELETE /api/movies/{id}` - Delete a movie

### Statistics
- `GET /api/stats` - Get combined statistics
- `GET /api/stats/books` - Get book statistics
- `GET /api/stats/movies` - Get movie statistics

### Natural Language Query
- `POST /api/query` - Ask a question about your library
  ```json
  {
    "question": "What are my top rated books?"
  }
  ```

## Natural Language Query Examples

The query interface understands various types of questions:

**Counting**
- "How many books have I read?"
- "How many movies are on my watchlist?"
- "How many fiction books do I have?"

**Ratings**
- "What are my top rated books?"
- "Show me movies rated above 8"
- "What's my average book rating?"

**Status**
- "What am I currently reading?"
- "Show me my want to read list"
- "What movies have I watched?"

**Authors/Directors**
- "Books by Kazuo Ishiguro"
- "Movies directed by Christopher Nolan"

**Search**
- "Do I have The Three-Body Problem?"
- "Find books about chemistry"

**Statistics**
- "Show me library statistics"
- "Give me an overview"

## Book Fields

| Field | Description |
|-------|-------------|
| name | Book title |
| author | Author name |
| downloaded | Source (Kindle, Google Books, etc.) |
| status | read, reading, want_to_read |
| rating | 0-10 rating |
| type | fiction, non-fiction |
| date_read | Date finished reading |
| format | text, audio, physical |
| notes | Personal notes or quotes |

## Movie Fields

| Field | Description |
|-------|-------------|
| title | Movie title |
| director | Director name |
| source | Where watched (Netflix, Prime, etc.) |
| status | watched, watching, want_to_watch |
| rating | 0-10 rating |
| genre | Movie genre |
| year | Release year |
| date_watched | Date watched |
| notes | Personal notes |

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build
```

## License

MIT

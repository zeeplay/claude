import React, { useState, useEffect, useCallback } from 'react';
import { booksApi, moviesApi, statsApi, queryApi, notesApi } from './api';

// Date formatting helper
const formatDate = (dateString) => {
  if (!dateString) return '-';

  const date = new Date(dateString);
  const day = date.getDate().toString().padStart(2, '0');
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const month = months[date.getMonth()];
  const year = date.getFullYear().toString().slice(-2);

  return `${day} ${month} ${year}`;
};

// Query Component
function QuerySection() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleQuery = async (q = question) => {
    if (!q.trim()) return;
    setLoading(true);
    try {
      const result = await queryApi.ask(q);
      setAnswer(result.answer);
    } catch (error) {
      setAnswer('Sorry, I had trouble understanding that question.');
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleQuery();
    }
  };

  return (
    <div className="query-section">
      <div className="query-container">
        <div className="query-input-wrapper">
          <input
            type="text"
            className="query-input"
            placeholder="Ask me anything about your books and movies..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button
            className="query-btn"
            onClick={() => handleQuery()}
            disabled={loading}
          >
            {loading ? 'Thinking...' : 'Ask'}
          </button>
        </div>

        {answer && (
          <div className="query-answer">{answer}</div>
        )}
      </div>
    </div>
  );
}

// General Notes Component
function GeneralNotesSection() {
  const [notes, setNotes] = useState('');
  const [savedNotes, setSavedNotes] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Load notes on component mount
    const loadNotes = async () => {
      try {
        const data = await notesApi.get();
        if (data && data.content) {
          setNotes(data.content);
          setSavedNotes(data.content);
        }
      } catch (error) {
        console.error('Error loading notes:', error);
      }
    };
    loadNotes();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      await notesApi.save(notes);
      setSavedNotes(notes);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      console.error('Error saving notes:', error);
    }
    setSaving(false);
  };

  const hasChanges = notes !== savedNotes;

  return (
    <div className="notes-section">
      <div className="notes-container">
        <div className="notes-header">
          <h3 className="notes-title">General Notes</h3>
          <button
            className="save-notes-btn"
            onClick={handleSave}
            disabled={saving || !hasChanges}
          >
            {saving ? 'Saving...' : saved ? 'Saved!' : 'Save Notes'}
          </button>
        </div>
        <textarea
          className="notes-textarea"
          placeholder="Add your general notes here... You can use this space for lists, reminders, or any other information you want to keep track of."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>
    </div>
  );
}

// Stats Component
function StatsCards({ stats }) {
  if (!stats) return null;

  const bookStats = stats.books || {};
  const movieStats = stats.movies || {};

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-value">{bookStats.total || 0}</div>
        <div className="stat-label">Total Books</div>
      </div>
      <div className="stat-card">
        <div className="stat-value">{bookStats.read || 0}</div>
        <div className="stat-label">Books Read</div>
      </div>
      <div className="stat-card">
        <div className="stat-value">{movieStats.total || 0}</div>
        <div className="stat-label">Total Movies</div>
      </div>
      <div className="stat-card">
        <div className="stat-value">{movieStats.watched || 0}</div>
        <div className="stat-label">Movies Watched</div>
      </div>
      <div className="stat-card">
        <div className="stat-value">{bookStats.average_rating || '-'}</div>
        <div className="stat-label">Avg Book Rating</div>
      </div>
      <div className="stat-card">
        <div className="stat-value">{movieStats.average_rating || '-'}</div>
        <div className="stat-label">Avg Movie Rating</div>
      </div>
    </div>
  );
}

// Book Modal Component
function BookModal({ book, onClose, onSave }) {
  const [formData, setFormData] = useState(book || {
    name: '',
    author: '',
    downloaded: '',
    status: 'want_to_read',
    rating: '',
    type: '',
    date_read: '',
    format: '',
    notes: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? null : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      ...formData,
      rating: formData.rating ? parseFloat(formData.rating) : null,
    };
    onSave(data);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{book ? 'Edit Book' : 'Add Book'}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label">Title *</label>
              <input
                type="text"
                name="name"
                className="form-input"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Author</label>
                <input
                  type="text"
                  name="author"
                  className="form-input"
                  value={formData.author || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Source</label>
                <input
                  type="text"
                  name="downloaded"
                  className="form-input"
                  placeholder="Kindle, Google Books, etc."
                  value={formData.downloaded || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  className="form-select"
                  value={formData.status}
                  onChange={handleChange}
                >
                  <option value="want_to_read">Want to Read</option>
                  <option value="reading">Reading</option>
                  <option value="read">Read</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Type</label>
                <select
                  name="type"
                  className="form-select"
                  value={formData.type || ''}
                  onChange={handleChange}
                >
                  <option value="">Select type</option>
                  <option value="fiction">Fiction</option>
                  <option value="non-fiction">Non-fiction</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Rating (0-10)</label>
                <input
                  type="number"
                  name="rating"
                  className="form-input"
                  min="0"
                  max="10"
                  step="0.5"
                  value={formData.rating || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Date Read</label>
                <input
                  type="date"
                  name="date_read"
                  className="form-input"
                  value={formData.date_read || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Format</label>
              <select
                name="format"
                className="form-select"
                value={formData.format || ''}
                onChange={handleChange}
              >
                <option value="">Select format</option>
                <option value="text">Text</option>
                <option value="audio">Audio</option>
                <option value="physical">Physical</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Notes</label>
              <textarea
                name="notes"
                className="form-textarea"
                placeholder="Your thoughts, quotes, or notes about this book..."
                value={formData.notes || ''}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {book ? 'Save Changes' : 'Add Book'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Movie Modal Component
function MovieModal({ movie, onClose, onSave }) {
  const [formData, setFormData] = useState(movie || {
    title: '',
    director: '',
    source: '',
    status: 'want_to_watch',
    rating: '',
    genre: '',
    year: '',
    date_watched: '',
    notes: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? null : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      ...formData,
      rating: formData.rating ? parseFloat(formData.rating) : null,
      year: formData.year ? parseInt(formData.year) : null,
    };
    onSave(data);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{movie ? 'Edit Movie' : 'Add Movie'}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label">Title *</label>
              <input
                type="text"
                name="title"
                className="form-input"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Director</label>
                <input
                  type="text"
                  name="director"
                  className="form-input"
                  value={formData.director || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Source</label>
                <input
                  type="text"
                  name="source"
                  className="form-input"
                  placeholder="Netflix, Prime, etc."
                  value={formData.source || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  className="form-select"
                  value={formData.status}
                  onChange={handleChange}
                >
                  <option value="want_to_watch">Want to Watch</option>
                  <option value="watching">Watching</option>
                  <option value="watched">Watched</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Genre</label>
                <input
                  type="text"
                  name="genre"
                  className="form-input"
                  placeholder="Drama, Comedy, etc."
                  value={formData.genre || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Rating (0-10)</label>
                <input
                  type="number"
                  name="rating"
                  className="form-input"
                  min="0"
                  max="10"
                  step="0.5"
                  value={formData.rating || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Year</label>
                <input
                  type="number"
                  name="year"
                  className="form-input"
                  min="1900"
                  max="2100"
                  value={formData.year || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Date Watched</label>
              <input
                type="date"
                name="date_watched"
                className="form-input"
                value={formData.date_watched || ''}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Notes</label>
              <textarea
                name="notes"
                className="form-textarea"
                placeholder="Your thoughts or notes about this movie..."
                value={formData.notes || ''}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {movie ? 'Save Changes' : 'Add Movie'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Rating Display Component
function RatingDisplay({ rating }) {
  if (!rating && rating !== 0) return <span className="text-secondary">-</span>;

  const percentage = (rating / 10) * 100;

  return (
    <div className="rating-cell">
      <span className="rating-value">{rating}</span>
      <div className="rating-bar-container">
        <div className="rating-bar" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

// Status Badge Component
function StatusBadge({ status }) {
  const labels = {
    read: 'Read',
    reading: 'Reading',
    want_to_read: 'Want to Read',
    watched: 'Watched',
    watching: 'Watching',
    want_to_watch: 'Want to Watch',
  };

  return (
    <span className={`status-badge status-${status}`}>
      {labels[status] || status}
    </span>
  );
}

// Books Table Component
function BooksTable({ books, onRowClick, sortColumn, sortDirection, onSort }) {
  if (books.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📚</div>
        <p className="empty-state-text">No books yet. Add your first book!</p>
      </div>
    );
  }

  const renderSortIcon = (column) => {
    if (sortColumn !== column) return <span className="sort-icon">↕</span>;
    return sortDirection === 'asc' ? <span className="sort-icon active">↑</span> : <span className="sort-icon active">↓</span>;
  };

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            <th onClick={() => onSort('name')} className="sortable-header">
              Title {renderSortIcon('name')}
            </th>
            <th onClick={() => onSort('author')} className="sortable-header">
              Author {renderSortIcon('author')}
            </th>
            <th onClick={() => onSort('downloaded')} className="sortable-header">
              Source {renderSortIcon('downloaded')}
            </th>
            <th onClick={() => onSort('status')} className="sortable-header">
              Status {renderSortIcon('status')}
            </th>
            <th onClick={() => onSort('rating')} className="sortable-header">
              Rating {renderSortIcon('rating')}
            </th>
            <th onClick={() => onSort('type')} className="sortable-header">
              Type {renderSortIcon('type')}
            </th>
            <th onClick={() => onSort('date_read')} className="sortable-header">
              Date Read {renderSortIcon('date_read')}
            </th>
          </tr>
        </thead>
        <tbody>
          {books.map(book => (
            <tr key={book.id} onClick={() => onRowClick(book)} className="clickable-row">
              <td className="title-cell">{book.name}</td>
              <td className="author-cell">{book.author || '-'}</td>
              <td className="source-cell">{book.downloaded || '-'}</td>
              <td><StatusBadge status={book.status} /></td>
              <td><RatingDisplay rating={book.rating} /></td>
              <td>
                {book.type && (
                  <span className="type-badge">{book.type}</span>
                )}
              </td>
              <td>{formatDate(book.date_read)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Movies Table Component
function MoviesTable({ movies, onRowClick, sortColumn, sortDirection, onSort }) {
  if (movies.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">🎬</div>
        <p className="empty-state-text">No movies yet. Add your first movie!</p>
      </div>
    );
  }

  const renderSortIcon = (column) => {
    if (sortColumn !== column) return <span className="sort-icon">↕</span>;
    return sortDirection === 'asc' ? <span className="sort-icon active">↑</span> : <span className="sort-icon active">↓</span>;
  };

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            <th onClick={() => onSort('title')} className="sortable-header">
              Title {renderSortIcon('title')}
            </th>
            <th onClick={() => onSort('director')} className="sortable-header">
              Director {renderSortIcon('director')}
            </th>
            <th onClick={() => onSort('source')} className="sortable-header">
              Source {renderSortIcon('source')}
            </th>
            <th onClick={() => onSort('status')} className="sortable-header">
              Status {renderSortIcon('status')}
            </th>
            <th onClick={() => onSort('rating')} className="sortable-header">
              Rating {renderSortIcon('rating')}
            </th>
            <th onClick={() => onSort('genre')} className="sortable-header">
              Genre {renderSortIcon('genre')}
            </th>
            <th onClick={() => onSort('year')} className="sortable-header">
              Year {renderSortIcon('year')}
            </th>
            <th onClick={() => onSort('date_watched')} className="sortable-header">
              Date Watched {renderSortIcon('date_watched')}
            </th>
          </tr>
        </thead>
        <tbody>
          {movies.map(movie => (
            <tr key={movie.id} onClick={() => onRowClick(movie)} className="clickable-row">
              <td className="title-cell">{movie.title}</td>
              <td className="author-cell">{movie.director || '-'}</td>
              <td className="source-cell">{movie.source || '-'}</td>
              <td><StatusBadge status={movie.status} /></td>
              <td><RatingDisplay rating={movie.rating} /></td>
              <td>
                {movie.genre && (
                  <span className="type-badge">{movie.genre}</span>
                )}
              </td>
              <td>{movie.year || '-'}</td>
              <td>{formatDate(movie.date_watched)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Book Detail View Component
function BookDetailView({ book, onClose, onEdit, onDelete }) {
  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-view" onClick={e => e.stopPropagation()}>
        <div className="detail-header">
          <button className="back-btn" onClick={onClose}>← Back to List</button>
          <div className="detail-actions">
            <button className="action-btn" onClick={() => onEdit(book)}>
              Edit
            </button>
            <button className="action-btn delete" onClick={() => onDelete(book.id)}>
              Delete
            </button>
          </div>
        </div>

        <div className="detail-content">
          <h1 className="detail-title">{book.name}</h1>

          <div className="detail-grid">
            <div className="detail-field">
              <label className="detail-label">Author</label>
              <div className="detail-value">{book.author || '-'}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Source</label>
              <div className="detail-value">{book.downloaded || '-'}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Status</label>
              <div className="detail-value"><StatusBadge status={book.status} /></div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Rating</label>
              <div className="detail-value"><RatingDisplay rating={book.rating} /></div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Type</label>
              <div className="detail-value">
                {book.type ? <span className="type-badge">{book.type}</span> : '-'}
              </div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Date Read</label>
              <div className="detail-value">{formatDate(book.date_read)}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Format</label>
              <div className="detail-value">{book.format || '-'}</div>
            </div>
          </div>

          {book.notes && (
            <div className="detail-notes">
              <label className="detail-label">Notes</label>
              <div className="notes-content">{book.notes}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Movie Detail View Component
function MovieDetailView({ movie, onClose, onEdit, onDelete }) {
  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-view" onClick={e => e.stopPropagation()}>
        <div className="detail-header">
          <button className="back-btn" onClick={onClose}>← Back to List</button>
          <div className="detail-actions">
            <button className="action-btn" onClick={() => onEdit(movie)}>
              Edit
            </button>
            <button className="action-btn delete" onClick={() => onDelete(movie.id)}>
              Delete
            </button>
          </div>
        </div>

        <div className="detail-content">
          <h1 className="detail-title">{movie.title}</h1>

          <div className="detail-grid">
            <div className="detail-field">
              <label className="detail-label">Director</label>
              <div className="detail-value">{movie.director || '-'}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Source</label>
              <div className="detail-value">{movie.source || '-'}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Status</label>
              <div className="detail-value"><StatusBadge status={movie.status} /></div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Rating</label>
              <div className="detail-value"><RatingDisplay rating={movie.rating} /></div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Genre</label>
              <div className="detail-value">
                {movie.genre ? <span className="type-badge">{movie.genre}</span> : '-'}
              </div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Year</label>
              <div className="detail-value">{movie.year || '-'}</div>
            </div>

            <div className="detail-field">
              <label className="detail-label">Date Watched</label>
              <div className="detail-value">{formatDate(movie.date_watched)}</div>
            </div>
          </div>

          {movie.notes && (
            <div className="detail-notes">
              <label className="detail-label">Notes</label>
              <div className="notes-content">{movie.notes}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Main App Component
function App() {
  const [activeTab, setActiveTab] = useState('books');
  const [books, setBooks] = useState([]);
  const [movies, setMovies] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState([]);
  const [typeFilter, setTypeFilter] = useState('');

  // Sorting state
  const [bookSortColumn, setBookSortColumn] = useState('date_read');
  const [bookSortDirection, setBookSortDirection] = useState('desc');
  const [movieSortColumn, setMovieSortColumn] = useState('date_watched');
  const [movieSortDirection, setMovieSortDirection] = useState('desc');

  // Modal state
  const [showBookModal, setShowBookModal] = useState(false);
  const [showMovieModal, setShowMovieModal] = useState(false);
  const [editingBook, setEditingBook] = useState(null);
  const [editingMovie, setEditingMovie] = useState(null);

  // Detail view state
  const [selectedBook, setSelectedBook] = useState(null);
  const [selectedMovie, setSelectedMovie] = useState(null);

  // Sorting function
  const sortData = useCallback((data, column, direction) => {
    return [...data].sort((a, b) => {
      let aVal = a[column];
      let bVal = b[column];

      // Handle null/undefined values - push them to the end
      if (aVal == null && bVal == null) return 0;
      if (aVal == null) return 1;
      if (bVal == null) return -1;

      // Convert to lowercase for string comparison
      if (typeof aVal === 'string') aVal = aVal.toLowerCase();
      if (typeof bVal === 'string') bVal = bVal.toLowerCase();

      if (aVal < bVal) return direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, []);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (statusFilter.length > 0) {
        // Only send status filter if not filtering by "no status"
        const statuses = statusFilter.filter(s => s !== 'none');
        if (statuses.length > 0) {
          params.status = statuses.join(',');
        }
      }
      if (typeFilter && activeTab === 'books') params.type = typeFilter;
      if (typeFilter && activeTab === 'movies') params.genre = typeFilter;

      const [booksData, moviesData, statsData] = await Promise.all([
        booksApi.getAll(params),
        moviesApi.getAll(params),
        statsApi.getAll(),
      ]);

      // Filter for "no status" if selected
      let filteredBooks = booksData;
      let filteredMovies = moviesData;

      if (statusFilter.includes('none')) {
        if (activeTab === 'books') {
          filteredBooks = filteredBooks.filter(book => !book.status);
        } else {
          filteredMovies = filteredMovies.filter(movie => !movie.status);
        }
      }

      // Apply sorting
      const sortedBooks = sortData(filteredBooks, bookSortColumn, bookSortDirection);
      const sortedMovies = sortData(filteredMovies, movieSortColumn, movieSortDirection);

      setBooks(sortedBooks);
      setMovies(sortedMovies);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setLoading(false);
  }, [search, statusFilter, typeFilter, activeTab, bookSortColumn, bookSortDirection, movieSortColumn, movieSortDirection, sortData]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Book handlers
  const handleSaveBook = async (book) => {
    try {
      if (editingBook) {
        await booksApi.update(editingBook.id, book);
      } else {
        await booksApi.create(book);
      }
      setShowBookModal(false);
      setEditingBook(null);
      fetchData();
    } catch (error) {
      console.error('Error saving book:', error);
    }
  };

  const handleEditBook = (book) => {
    setEditingBook(book);
    setShowBookModal(true);
  };

  const handleDeleteBook = async (id) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      try {
        await booksApi.delete(id);
        fetchData();
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    }
  };

  // Movie handlers
  const handleSaveMovie = async (movie) => {
    try {
      if (editingMovie) {
        await moviesApi.update(editingMovie.id, movie);
      } else {
        await moviesApi.create(movie);
      }
      setShowMovieModal(false);
      setEditingMovie(null);
      fetchData();
    } catch (error) {
      console.error('Error saving movie:', error);
    }
  };

  const handleEditMovie = (movie) => {
    setEditingMovie(movie);
    setShowMovieModal(true);
  };

  const handleDeleteMovie = async (id) => {
    if (window.confirm('Are you sure you want to delete this movie?')) {
      try {
        await moviesApi.delete(id);
        fetchData();
      } catch (error) {
        console.error('Error deleting movie:', error);
      }
    }
  };

  // Sorting handlers
  const handleBookSort = (column) => {
    if (bookSortColumn === column) {
      // Toggle direction if same column
      setBookSortDirection(bookSortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New column, default to ascending
      setBookSortColumn(column);
      setBookSortDirection('asc');
    }
  };

  const handleMovieSort = (column) => {
    if (movieSortColumn === column) {
      // Toggle direction if same column
      setMovieSortDirection(movieSortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New column, default to ascending
      setMovieSortColumn(column);
      setMovieSortDirection('asc');
    }
  };

  // Status filter handlers
  const handleStatusFilterToggle = (status) => {
    setStatusFilter(prev => {
      if (prev.includes(status)) {
        return prev.filter(s => s !== status);
      } else {
        return [...prev, status];
      }
    });
  };

  const bookStatusOptions = [
    { value: 'read', label: 'Read' },
    { value: 'reading', label: 'Reading' },
    { value: 'want_to_read', label: 'Want to Read' },
    { value: 'none', label: 'No Status' },
  ];

  const movieStatusOptions = [
    { value: 'watched', label: 'Watched' },
    { value: 'watching', label: 'Watching' },
    { value: 'want_to_watch', label: 'Want to Watch' },
    { value: 'none', label: 'No Status' },
  ];

  const bookTypeOptions = [
    { value: '', label: 'All Types' },
    { value: 'fiction', label: 'Fiction' },
    { value: 'non-fiction', label: 'Non-fiction' },
  ];

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">z<span>Books</span></div>
          <nav className="nav-tabs">
            <button
              className={`nav-tab ${activeTab === 'books' ? 'active' : ''}`}
              onClick={() => setActiveTab('books')}
            >
              Books
            </button>
            <button
              className={`nav-tab ${activeTab === 'movies' ? 'active' : ''}`}
              onClick={() => setActiveTab('movies')}
            >
              Movies
            </button>
          </nav>
        </div>
      </header>

      <main className="main-content">
        <QuerySection />
        <GeneralNotesSection />

        <div className="toolbar">
          <div className="filters">
            <div className="status-filter-group">
              <label className="filter-label">Status:</label>
              <div className="checkbox-group">
                {(activeTab === 'books' ? bookStatusOptions : movieStatusOptions).map(opt => (
                  <label key={opt.value} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={statusFilter.includes(opt.value)}
                      onChange={() => handleStatusFilterToggle(opt.value)}
                    />
                    <span>{opt.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {activeTab === 'books' && (
              <select
                className="filter-select"
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
              >
                {bookTypeOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            )}

            <input
              type="text"
              className="search-input"
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <button
            className="add-btn"
            onClick={() => {
              if (activeTab === 'books') {
                setEditingBook(null);
                setShowBookModal(true);
              } else {
                setEditingMovie(null);
                setShowMovieModal(true);
              }
            }}
          >
            + Add {activeTab === 'books' ? 'Book' : 'Movie'}
          </button>
        </div>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : activeTab === 'books' ? (
          <BooksTable
            books={books}
            onRowClick={setSelectedBook}
            sortColumn={bookSortColumn}
            sortDirection={bookSortDirection}
            onSort={handleBookSort}
          />
        ) : (
          <MoviesTable
            movies={movies}
            onRowClick={setSelectedMovie}
            sortColumn={movieSortColumn}
            sortDirection={movieSortDirection}
            onSort={handleMovieSort}
          />
        )}
      </main>

      {showBookModal && (
        <BookModal
          book={editingBook}
          onClose={() => {
            setShowBookModal(false);
            setEditingBook(null);
          }}
          onSave={handleSaveBook}
        />
      )}

      {showMovieModal && (
        <MovieModal
          movie={editingMovie}
          onClose={() => {
            setShowMovieModal(false);
            setEditingMovie(null);
          }}
          onSave={handleSaveMovie}
        />
      )}

      {selectedBook && (
        <BookDetailView
          book={selectedBook}
          onClose={() => setSelectedBook(null)}
          onEdit={(book) => {
            setSelectedBook(null);
            handleEditBook(book);
          }}
          onDelete={(id) => {
            setSelectedBook(null);
            handleDeleteBook(id);
          }}
        />
      )}

      {selectedMovie && (
        <MovieDetailView
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
          onEdit={(movie) => {
            setSelectedMovie(null);
            handleEditMovie(movie);
          }}
          onDelete={(id) => {
            setSelectedMovie(null);
            handleDeleteMovie(id);
          }}
        />
      )}
    </div>
  );
}

export default App;

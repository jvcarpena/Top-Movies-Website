# Top 10 Movie App

This is a Flask-based web application for managing a movie database. It allows users to add, edit, view, and delete movies. The app also integrates with an external movie API to fetch movie details and images.

## Features

- **Add Movies**: Search for a movie by title and add it to the database.
- **Edit Movies**: Update movie ratings and reviews.
- **View Movies**: See all movies in the database ranked by rating.
- **Delete Movies**: Remove a movie from the database.

## Technologies Used

- **Backend**: Flask
- **Frontend**: HTML, Bootstrap (via Flask-Bootstrap)
- **Database**: SQLAlchemy with SQLite
- **Forms**: Flask-WTF for form handling and validation
- **API Integration**: External movie API for fetching movie data

## Prerequisites

- Python 3.8+
- Pipenv or virtualenv (optional but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the following environment variables:
   ```env
   FLASK_SECRET_KEY=<your-secret-key>
   DB_URI=sqlite:///movies.db
   API_KEY=<your-api-key>
   AUTH_BEARER_TOKEN=<your-auth-bearer-token>
   URL_AUTH=<your-url-auth>
   MOVIE_SEARCH_URL=<movie-search-url>
   MOVIE_DETAILS_URL=<movie-details-url>
   IMG_DB_URL=<image-db-url>
   ```

5. Initialize the database:
   ```bash
   python app.py
   ```
   This will create the necessary tables in the SQLite database.

## Usage

1. Run the app:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Use the application to manage your movie database:
   - Add a movie by searching for its title.
   - Edit a movie's rating and review.
   - Delete a movie from the database.

## Project Structure

```
├── templates/
│   ├── index.html      # Homepage
│   ├── add.html        # Add movie form
│   ├── edit.html       # Edit movie form
│   ├── select.html     # Select movie from API results
├── static/             # Static files (e.g., CSS, JS)
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
```

## API Integration

This application uses an external movie API to:

- Search for movies based on a query string.
- Fetch detailed information about a specific movie.
- Retrieve movie poster images.

Ensure that your `.env` file contains valid API credentials for this integration to work.

## Notes

- The application uses SQLAlchemy ORM for database interactions.
- Flask-WTF is used for creating and validating forms.
- Make sure to keep your API keys and sensitive data secure in the `.env` file.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

---

Enjoy managing your movie database!


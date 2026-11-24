# Popcorn Cinema — Web Applications Project (Checkpoint 2)

Web application for cinema ticket booking developed for the **Web Applications** course at Universidad Carlos III de Madrid (UC3M).

---

## 📌 Milestone Overview (Checkpoint 2)

This milestone expands upon the initial views and models developed in Checkpoint 1, introducing complete user authentication, session-based access control, interactive seat selection, and booking management:

- **Authentication Blueprint (`cinema/auth.py`)**:
  - User registration (`/signup`) with password hashing via `werkzeug.security.generate_password_hash`.
  - User login (`/login`) with credential validation via `check_password_hash` and session handling via **Flask-Login**.
  - Secure logout (`/logout`) protected with `@flask_login.login_required`.
  - Redirection to protected views after login (`next` parameter support).

- **Interactive Seat Map & Concessions (`cinema/templates/main/seats.html`, `/showtime/<id>/seats`)**:
  - Visual seat layout with rows (A–H) and columns (1–12).
  - Dynamic status handling (available, selected, occupied).
  - Food & drink package selection alongside ticket reservations.

- **Booking Management (`cinema/templates/main/bookings.html`, `/bookings`)**:
  - Protected view accessible only to logged-in users (`@login_required`).
  - Displays pending booking summaries and past/future reservation history.

- **Refined Data Models (`cinema/model.py`)**:
  - Updated relationships and schema definitions for `User`, `Screen`, `Movie`, `Showtime`, `TicketPrice`, `FoodItem`, `Booking`, and `BookingFoodItem`.

---

## 📂 Project Structure

```text
CINEMA-PROJECT_checkpoint_2/
├── cinema/
│   ├── __init__.py           # Flask app factory, config & LoginManager initialization
│   ├── auth.py               # Authentication blueprint (signup, login, logout)
│   ├── main.py               # Main blueprint routes (catalogue, detail, seats, bookings)
│   ├── model.py              # SQLAlchemy database models & relationships
│   ├── static/
│   │   ├── cinema.css        # Responsive stylesheet with seat map & booking styles
│   │   └── posters/          # Movie poster assets
│   └── templates/
│       ├── base.html         # Base layout template with dynamic authentication links
│       ├── auth/
│       │   ├── login.html    # User login template
│       │   └── signup.html   # User registration template
│       └── main/
│           ├── index.html         # Movie catalogue (ticket cards)
│           ├── movie_detail.html  # Movie details & showtimes list
│           ├── seats.html         # Interactive seat map & snack selection
│           └── bookings.html      # User booking history & confirmation
├── Makefile                  # Build & automation shortcuts (install, run, clean)
├── requirements.txt          # Python library dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules for virtual environments, caches, DBs
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.11 / 3.12)
- Virtual environment support (`venv`)
- `make` (optional)

### 2. Quick Start with Make

```bash
# 1. Create virtual environment and install dependencies
make install

# 2. Run development server
make run
```

Then navigate to [http://localhost:5000](http://localhost:5000) or [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

### 3. Manual Setup (Without Make)

#### On macOS / Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file with your database URI
cat << 'EOF' > .env
SECRET_KEY=93220d9b340cf9a6c39bac99cce7daf220167498f91fa
SQLALCHEMY_DATABASE_URI=sqlite:///cinema.db
EOF

# Run the Flask development server
flask --debug --app=cinema run
```

#### On Windows:
```cmd
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask --debug --app=cinema run
```

---

## 🛠️ Configuration (.env)

Set up your `.env` file in the project root:

```ini
SECRET_KEY=93220d9b340cf9a6c39bac99cce7daf220167498f91fa

# Local development (SQLite):
SQLALCHEMY_DATABASE_URI=sqlite:///cinema.db

# UC3M Laboratory server (MariaDB):
# SQLALCHEMY_DATABASE_URI=mysql+pymysql://27_webapp_XX:PASSWORD@mysql/27_webapp_XXa
```

---

## 📋 Available Make Commands

- `make install`: Creates virtual environment and installs all dependencies.
- `make run`: Starts Flask in debug mode with hot reloading.
- `make clean`: Removes Python caches (`__pycache__`) and local test databases.
- `make clean-all`: Performs complete cleanup including virtual environments.
- `make help`: Shows available commands.

---

## 👥 Authors

- Web Applications — UC3M (Universidad Carlos III de Madrid)

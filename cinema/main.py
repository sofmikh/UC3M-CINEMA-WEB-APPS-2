import datetime  # <-- FALTABA

from flask import Blueprint, render_template, request, abort
from flask_login import login_required

from cinema import model

bp = Blueprint("main", __name__)


def demo_movies():
    # screens
    screen1 = model.Screen(id=1, name="Screen 1", capacity=96)
    screen2 = model.Screen(id=2, name="Screen 2 (VIP)", capacity=60)
    screen3 = model.Screen(id=3, name="Screen 3", capacity=80)

    # movies
    love = model.Movie(
        id=1,
        title="The Love Hypothesis",
        genre="Romance / Comedy",
        duration=118,
        age_rating="+12",
        synopsis="When a fake-dating experiment between two scientists turns into unexpected real feelings, chaos and romance collide in the academia lab.",
        poster_url="love_hypothesis.jpg",
    )
    bola = model.Movie(
        id=2,
        title="La Bola Negra",
        genre="Mystery / Psychological Thriller",
        duration=105,
        age_rating="+16",
        synopsis="An enigmatic black sphere appears unexpectedly, unraveling secrets, hidden desires, and paranoia within an isolated community.",
        poster_url="la_bola_negra.jpg",
    )
    barbie = model.Movie(
        id=3,
        title="Barbie in A Mermaid Tale",
        genre="Animation / Family / Adventure",
        duration=75,
        age_rating="All",
        synopsis="Merliah, a surfing champion from Malibu, discovers an astonishing family secret: she is actually a mermaid destined to save Oceana.",
        poster_url="barbie.jpg",
    )

    def today_at(hour, minute):
        return datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)

    showtimes = [
        model.Showtime(id=101, movie=love, screen=screen1, show_time=today_at(16, 30), price=8.00),
        model.Showtime(id=102, movie=love, screen=screen2, show_time=today_at(19, 15), price=10.50),
        model.Showtime(id=103, movie=love, screen=screen1, show_time=today_at(21, 45), price=8.00),
        model.Showtime(id=201, movie=bola, screen=screen1, show_time=today_at(18, 0), price=8.00),
        model.Showtime(id=202, movie=bola, screen=screen2, show_time=today_at(20, 30), price=10.50),
        model.Showtime(id=203, movie=bola, screen=screen1, show_time=today_at(22, 50), price=8.00),
        model.Showtime(id=301, movie=barbie, screen=screen3, show_time=today_at(16, 0), price=8.00),
        model.Showtime(id=302, movie=barbie, screen=screen3, show_time=today_at(17, 45), price=8.00),
    ]

    return [love, bola, barbie], showtimes

MOVIES_LIST, SHOWTIMES_LIST = demo_movies()
MOVIES = {m.id: m for m in MOVIES_LIST}
SHOWTIMES = {st.id: st for st in SHOWTIMES_LIST}

PACKAGES = [
    {"id": 1, "name": "Solo Combo", "desc": "Medium Sweet Popcorn + 500ml Soft Drink", "price": 6.50},
    {"id": 2, "name": "Duo Combo", "desc": "Large Popcorn + 2x 500ml Drinks + Sweet Candy", "price": 10.50},
]

OCCUPIED_SEATS = ["A3", "A4", "B7", "B8", "B9", "C1", "C2", "D5", "D6", "D10", "F3", "F4", "F5", "G8", "G9", "H1", "H12"]


def showtimes_for(movie_id):
    """Devuelve la lista de sesiones de una película."""
    return [st for st in SHOWTIMES.values() if st.movie.id == movie_id]


@bp.route("/")
def index():
    movies = list(MOVIES.values())
    return render_template("main/index.html", movies=movies)


@bp.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = MOVIES.get(movie_id)
    if movie is None:
        abort(404)
    return render_template(
        "main/movie_detail.html",
        movie=movie,
        showtimes=showtimes_for(movie_id),
    )


@bp.route("/showtime/<int:showtime_id>/seats")
def seats(showtime_id):
    showtime = SHOWTIMES.get(showtime_id)
    if showtime is None:
        abort(404)
    movie = showtime.movie  # el objeto ya sabe cuál es su película
    return render_template(
        "main/seats.html",
        movie=movie,
        showtime=showtime,
        packages=PACKAGES,
        rows="ABCDEFGH",
        seats_per_row=12,
        occupied=OCCUPIED_SEATS,
    )


@bp.route("/bookings")
@login_required
def bookings():
    pending = None
    chosen_seats = request.args.getlist("seats")
    showtime = SHOWTIMES.get(request.args.get("showtime_id", type=int))
    if chosen_seats and showtime:
        movie = showtime.movie
        total = len(chosen_seats) * showtime.price
        food = []
        for pkg in PACKAGES:
            qty = request.args.get(f"package_{pkg['id']}", default=0, type=int)
            if qty > 0:
                food.append(f"{qty}x {pkg['name']}")
                total += qty * pkg["price"]
        pending = {
            "movie": movie.title,
            "showtime": f"Today, {showtime.show_time.strftime('%H:%M')} - {showtime.screen.name}",
            "seats": chosen_seats,
            "food": ", ".join(food) if food else "No food",
            "total_price": total,
        }

    my_bookings = [
        {
            "id": "BK-9021",
            "movie": "The Love Hypothesis",
            "showtime": "Today, 19:15 - Screen 2 (VIP)",
            "seats": 2,
            "food": "1x Duo Combo",
            "total_price": 31.50,
            "is_future": True,
        },
        {
            "id": "BK-8412",
            "movie": "Barbie in A Mermaid Tale",
            "showtime": "Yesterday, 17:45 - Screen 1",
            "seats": 1,
            "food": "1x Solo Combo",
            "total_price": 14.50,
            "is_future": False,
        },
    ]
    return render_template("main/bookings.html", bookings=my_bookings, pending=pending)
import datetime

from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user

from cinema import db, model

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


PACKAGES = [
    {"id": 1, "name": "Solo Combo", "desc": "Medium Sweet Popcorn + 500ml Soft Drink", "price": 6.50},
    {"id": 2, "name": "Duo Combo", "desc": "Large Popcorn + 2x 500ml Drinks + Sweet Candy", "price": 10.50},
]

OCCUPIED_SEATS = []

def occupied_seats_for(showtime_id):
    taken = list(OCCUPIED_SEATS)

    query = (
        db.select(model.BookingSeat.seat)
        .join(model.Booking)
        .where(model.Booking.showtime_id == showtime_id)
    )
    for seat in db.session.execute(query).scalars().all():
        taken.append(seat)

    return taken


def showtimes_for(movie_id):
    query = (
        db.select(model.Showtime)
        .where(model.Showtime.movie_id == movie_id)
        .where(model.Showtime.show_time >= datetime.datetime.now())
        .order_by(model.Showtime.show_time)
    )
    return db.session.execute(query).scalars().all()


def booking_to_dict(b):
    showtime = b.showtime
    show_dt = showtime.show_time
    
    if show_dt.date() == datetime.date.today():
        day = "Today"
    else:
        day = show_dt.strftime("%d/%m")

    # la comida guardada en booking_food_items
    food = []
    for item in b.food_items:
        for pkg in PACKAGES:
            if pkg["id"] == item.food_item_id:
                food.append(f"{item.quantity}x {pkg['name']}")

    return {
        "id": f"BK-{b.id}",
        "movie": showtime.movie.title,
        "showtime": f"{day}, {show_dt.strftime('%H:%M')} - {showtime.screen.name}",
        "seats": b.num_seats,
        "food": ", ".join(food) if food else "No food",
        "total_price": b.total_price,
        "is_future": show_dt > datetime.datetime.now(),
    }


@bp.route("/")
def index():
    movies = db.session.execute(db.select(model.Movie)).scalars().all() 
    return render_template("main/index.html", movies=movies)


@bp.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = db.session.get(model.Movie, movie_id)
    if movie is None:
        abort(404)
    return render_template(
        "main/movie_detail.html",
        movie=movie,
        showtimes=showtimes_for(movie_id),
    )


@bp.route("/showtime/<int:showtime_id>/seats")
def seats(showtime_id):
    showtime = db.session.get(model.Showtime, showtime_id) 
    if showtime is None:
        abort(404)
    movie = showtime.movie
    return render_template(
        "main/seats.html",
        movie=movie,
        showtime=showtime,
        packages=PACKAGES,
        rows="ABCDEFGH",
        seats_per_row=12,
        occupied=occupied_seats_for(showtime_id),     
    )


@bp.route("/bookings", methods=["GET", "POST"])
@login_required
def bookings():

    if request.method == "POST":
        chosen_seats = request.form.getlist("seats")
        showtime_id = request.form.get("showtime_id", type=int)
        showtime = db.session.get(model.Showtime, showtime_id) if showtime_id else None

        if chosen_seats and showtime:
            taken = occupied_seats_for(showtime.id)
            for seat in chosen_seats:
                if seat in taken:
                    abort(400)

            # price of the seats
            total = len(chosen_seats) * showtime.price

            # foood
            food_lines = []
            for pkg in PACKAGES:
                qty = request.form.get(f"package_{pkg['id']}", default=0, type=int)
                if qty > 0:
                    food_lines.append((pkg, qty))
                    total += qty * pkg["price"]

            #booking
            booking = model.Booking(
                user_id=current_user.id,
                showtime_id=showtime.id,
                num_seats=len(chosen_seats),
                total_price=total,
                created_at=datetime.datetime.now(),
            )
            db.session.add(booking)

            # comida booking_food_items
            for pkg, qty in food_lines:
                item = model.BookingFoodItem(
                    booking=booking,
                    food_item_id=pkg["id"],
                    quantity=qty,
                    price_per_unit=pkg["price"],
                )
                db.session.add(item)

            for seat in chosen_seats:
                db.session.add(model.BookingSeat(booking=booking, seat=seat))

            # we save everything to the database
            db.session.commit()

        # redirect
        return redirect(url_for("main.bookings"))

    query = (
        db.select(model.Booking)
        .where(model.Booking.user_id == current_user.id)
        .order_by(model.Booking.created_at.desc())
    )
    user_bookings = db.session.execute(query).scalars().all()

    my_bookings = []
    for b in user_bookings:
        info = booking_to_dict(b)
        if info is not None:
            my_bookings.append(info)

    return render_template("main/bookings.html", bookings=my_bookings)
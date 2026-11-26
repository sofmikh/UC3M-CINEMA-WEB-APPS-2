import datetime

from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user

from cinema import db, model

bp = Blueprint("main", __name__)


def format_day_label(d):
    today = datetime.date.today()
    if d == today:
        return "Today"
    if d == today + datetime.timedelta(days=1):
        return "Tomorrow"
    return d.strftime("%a %d %b")


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

    def day_at(days_ahead, hour, minute):
        base = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        return base + datetime.timedelta(days=days_ahead)

    schedule = {
        love: [
            [(screen1, 16, 30, 8.00), (screen2, 19, 15, 10.50), (screen1, 21, 45, 8.00)],
            [(screen1, 15, 45, 8.00), (screen2, 18, 30, 10.50), (screen1, 21, 15, 8.00), (screen2, 23, 10, 10.50)],
            [(screen1, 16, 0, 8.00), (screen2, 19, 0, 10.50), (screen1, 22, 0, 8.00)],
            [(screen1, 17, 15, 8.00), (screen2, 20, 0, 10.50), (screen1, 22, 30, 8.00)],
            [(screen1, 16, 30, 8.00), (screen2, 19, 30, 10.50), (screen1, 21, 45, 8.00)],
        ],
        bola: [
            [(screen1, 18, 0, 8.00), (screen2, 20, 30, 10.50), (screen1, 22, 50, 8.00)],
            [(screen1, 17, 30, 8.00), (screen2, 20, 15, 10.50), (screen1, 22, 45, 8.00)],
            [(screen2, 18, 15, 10.50), (screen1, 21, 0, 8.00), (screen2, 23, 15, 10.50)],
            [(screen1, 16, 45, 8.00), (screen2, 19, 45, 10.50), (screen1, 22, 15, 8.00)],
            [(screen1, 18, 0, 8.00), (screen2, 20, 45, 10.50), (screen1, 23, 0, 8.00)],
        ],
        barbie: [
            [(screen3, 16, 0, 8.00), (screen3, 17, 45, 8.00), (screen3, 19, 30, 8.00)],
            [(screen3, 12, 0, 7.50), (screen3, 15, 30, 8.00), (screen3, 17, 30, 8.00), (screen3, 19, 30, 8.00)],
            [(screen3, 12, 15, 7.50), (screen3, 16, 0, 8.00), (screen3, 18, 15, 8.00)],
            [(screen3, 15, 45, 8.00), (screen3, 17, 45, 8.00), (screen3, 19, 45, 8.00)],
            [(screen3, 12, 0, 7.50), (screen3, 16, 15, 8.00), (screen3, 18, 30, 8.00)],
        ],
    }

    showtimes = []
    for movie, days_list in schedule.items():
        for day_offset, slots in enumerate(days_list):
            for screen, hour, minute, price in slots:
                showtimes.append(
                    model.Showtime(
                        movie=movie,
                        screen=screen,
                        show_time=day_at(day_offset, hour, minute),
                        price=price,
                    )
                )

    return [love, bola, barbie], showtimes


def demo_food_items():
    return [
        # Combos
        model.FoodItem(
            name="Solo Popcorn Combo",
            description="Medium Butter Popcorn + 500ml Soft Drink",
            price=6.50,
            category="combo",
            is_package=True,
        ),
        model.FoodItem(
            name="Duo Date Combo",
            description="Large Popcorn + 2x 500ml Drinks + Warm Churros",
            price=11.50,
            category="combo",
            is_package=True,
        ),
        model.FoodItem(
            name="Nachos & Slushie Deal",
            description="Loaded Cheddar Nachos + Blue Raspberry Slushie",
            price=8.50,
            category="combo",
            is_package=True,
        ),
        # Food
        model.FoodItem(
            name="Classic Butter Popcorn (L)",
            description="Freshly popped kernels with warm salted butter",
            price=4.50,
            category="food",
            is_package=False,
        ),
        model.FoodItem(
            name="Caramel & Sea Salt Popcorn",
            description="Crunchy glazed caramel popcorn with flaky sea salt",
            price=5.20,
            category="food",
            is_package=False,
        ),
        model.FoodItem(
            name="Loaded Cheddar Nachos",
            description="Crispy tortilla chips, warm cheddar sauce & jalapeños",
            price=6.00,
            category="food",
            is_package=False,
        ),
        model.FoodItem(
            name="Popcorn Cinema Hot Dog",
            description="Brioche bun, grilled sausage, crispy onions & mustard",
            price=5.50,
            category="food",
            is_package=False,
        ),
        model.FoodItem(
            name="Warm Churros & Chocolate",
            description="5 cinnamon sugar churros with rich dark chocolate dip",
            price=4.80,
            category="food",
            is_package=False,
        ),
        # Drinks
        model.FoodItem(
            name="Classic Cola / Zero (500ml)",
            description="Ice-cold fountain cola with fresh lemon slice",
            price=3.20,
            category="drink",
            is_package=False,
        ),
        model.FoodItem(
            name="Blue Raspberry Slushie",
            description="Frozen crushed ice with tangy blue raspberry syrup",
            price=4.00,
            category="drink",
            is_package=False,
        ),
        model.FoodItem(
            name="Sparkling Peach Iced Tea",
            description="Brewed black tea infused with white peach & mint",
            price=3.50,
            category="drink",
            is_package=False,
        ),
        model.FoodItem(
            name="Homemade Pink Lemonade",
            description="Freshly squeezed lemon, raspberry & sparkling water",
            price=3.80,
            category="drink",
            is_package=False,
        ),
        model.FoodItem(
            name="Mineral Water (500ml)",
            description="Still or sparkling chilled spring water",
            price=2.20,
            category="drink",
            is_package=False,
        ),
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
        .order_by(model.Showtime.show_time)
    )
    return db.session.execute(query).scalars().all()


def get_menu_sections():
    items = db.session.execute(
        db.select(model.FoodItem).order_by(model.FoodItem.id)
    ).scalars().all()
    combos = [i for i in items if i.category == "combo"]
    foods = [i for i in items if i.category == "food"]
    drinks = [i for i in items if i.category == "drink"]
    return combos, foods, drinks


def booking_to_dict(b):
    showtime = b.showtime
    show_dt = showtime.show_time

    day = format_day_label(show_dt.date())

    food = []
    for item in b.food_items:
        food.append(f"{item.quantity}x {item.food_item.name}")

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
    movies = db.session.execute(db.select(model.Movie).order_by(model.Movie.id)).scalars().all()
    all_showtimes = db.session.execute(
        db.select(model.Showtime).order_by(model.Showtime.show_time)
    ).scalars().all()

    available_dates = sorted({st.show_time.date() for st in all_showtimes})
    days = [
        {"iso": d.isoformat(), "label": format_day_label(d), "sub": d.strftime("%d %b")}
        for d in available_dates
    ]

    day_param = request.args.get("day")
    selected_date = None
    if day_param:
        try:
            selected_date = datetime.date.fromisoformat(day_param)
        except ValueError:
            selected_date = None

    if selected_date not in available_dates:
        selected_date = available_dates[0] if available_dates else datetime.date.today()

    showtimes_by_movie = {}
    for st in all_showtimes:
        if st.show_time.date() == selected_date:
            showtimes_by_movie.setdefault(st.movie_id, []).append(st)

    return render_template(
        "main/index.html",
        movies=movies,
        days=days,
        selected_day=selected_date.isoformat(),
        selected_day_label=format_day_label(selected_date),
        showtimes_by_movie=showtimes_by_movie,
    )


@bp.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = db.session.get(model.Movie, movie_id)
    if movie is None:
        abort(404)

    all_showtimes = showtimes_for(movie_id)
    grouped = {}
    for st in all_showtimes:
        d = st.show_time.date()
        if d not in grouped:
            grouped[d] = {
                "iso": d.isoformat(),
                "label": format_day_label(d),
                "sub": d.strftime("%d %b"),
                "showtimes": [],
            }
        grouped[d]["showtimes"].append(st)

    return render_template(
        "main/movie_detail.html",
        movie=movie,
        days_grouped=list(grouped.values()),
    )


@bp.route("/menu")
def menu():
    combos, foods, drinks = get_menu_sections()
    return render_template(
        "main/menu.html",
        combos=combos,
        foods=foods,
        drinks=drinks,
    )


@bp.route("/showtime/<int:showtime_id>/seats")
def seats(showtime_id):
    showtime = db.session.get(model.Showtime, showtime_id)
    if showtime is None:
        abort(404)
    movie = showtime.movie
    combos, foods, drinks = get_menu_sections()
    return render_template(
        "main/seats.html",
        movie=movie,
        showtime=showtime,
        day_label=format_day_label(showtime.show_time.date()),
        combos=combos,
        foods=foods,
        drinks=drinks,
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

            total = len(chosen_seats) * showtime.price

            all_food_items = db.session.execute(db.select(model.FoodItem)).scalars().all()
            food_lines = []
            for fi in all_food_items:
                qty = request.form.get(f"food_{fi.id}", default=0, type=int)
                if qty and qty > 0:
                    food_lines.append((fi, qty))
                    total += qty * fi.price

            booking = model.Booking(
                user_id=current_user.id,
                showtime_id=showtime.id,
                num_seats=len(chosen_seats),
                total_price=total,
                created_at=datetime.datetime.now(),
            )
            db.session.add(booking)

            for fi, qty in food_lines:
                item = model.BookingFoodItem(
                    booking=booking,
                    food_item_id=fi.id,
                    quantity=qty,
                    price_per_unit=fi.price,
                )
                db.session.add(item)

            for seat in chosen_seats:
                db.session.add(model.BookingSeat(booking=booking, seat=seat))

            db.session.commit()

        return redirect(url_for("main.bookings"))

    query = (
        db.select(model.Booking)
        .where(model.Booking.user_id == current_user.id)
        .order_by(model.Booking.created_at.desc())
    )
    user_bookings = db.session.execute(query).scalars().all()

    my_bookings = [booking_to_dict(b) for b in user_bookings]

    return render_template("main/bookings.html", bookings=my_bookings)

import datetime
import enum
from typing import List, Optional
import flask_login
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, LargeBinary, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from . import db


# Roles requeridos según las instrucciones
class UserRole(enum.Enum):
    customer = 1
    management_staff = 2


class User(flask_login.UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(512))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.customer)

    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")


class Screen(db.Model):
    __tablename__ = "screens"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))  # Ej: 'Sala 1', 'Sala IMAX'
    capacity: Mapped[int] = mapped_column(Integer)

    showtimes: Mapped[List["Showtime"]] = relationship(back_populates="screen")


class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    synopsis: Mapped[str] = mapped_column(String(2048))
    duration: Mapped[int] = mapped_column(Integer)  # Duración en minutos
    age_rating: Mapped[str] = mapped_column(String(16))  # Ej: '+12', '+16', 'TP'
    genre: Mapped[str] = mapped_column(String(64))
    poster_url: Mapped[Optional[str]] = mapped_column(String(256))

    showtimes: Mapped[List["Showtime"]] = relationship(back_populates="movie")


class TicketPrice(db.Model):
    __tablename__ = "ticket_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    day_of_week: Mapped[int] = mapped_column(Integer)  # 0: Lunes, ..., 2: Miércoles (espectador), 6: Domingo
    day_name: Mapped[str] = mapped_column(String(16))
    price: Mapped[float] = mapped_column(Float)


class Showtime(db.Model):
    __tablename__ = "showtimes"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    screen_id: Mapped[int] = mapped_column(ForeignKey("screens.id"))
    show_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    movie: Mapped["Movie"] = relationship(back_populates="showtimes")
    screen: Mapped["Screen"] = relationship(back_populates="showtimes")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="showtime")
    price: Mapped[float] = mapped_column(Float)


class FoodItem(db.Model):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(256), server_default="")
    price: Mapped[float] = mapped_column(Float)
    is_package: Mapped[bool] = mapped_column(default=False)  # True si es un combo con entrada


class Booking(db.Model):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id"))
    num_seats: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="bookings")
    showtime: Mapped["Showtime"] = relationship(back_populates="bookings")
    food_items: Mapped[List["BookingFoodItem"]] = relationship(back_populates="booking")


class BookingFoodItem(db.Model):
    __tablename__ = "booking_food_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    food_item_id: Mapped[int] = mapped_column(ForeignKey("food_items.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price_per_unit: Mapped[float] = mapped_column(Float)

    booking: Mapped["Booking"] = relationship(back_populates="food_items")
    food_item: Mapped["FoodItem"] = relationship()
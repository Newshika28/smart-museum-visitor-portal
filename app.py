import os
import bcrypt
from db import get_db_connection, init_db
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
import qrcode

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        print("FORM DATA:", request.form)
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        username = request.form["username"]
        password = request.form["password"]

        # FIXED INDENTATION HERE:
        if len(password) < 6:
            error = "Password must be at least 6 characters"
            return render_template("signup.html", error=error)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cur.fetchone()

        if user:
            error = "Username already exists"

        else:

            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            cur.execute(
                """
    INSERT INTO users(
        full_name,
        email,
        phone,
        username,
        password
    )
    VALUES (?, ?, ?, ?, ?)
    """,
                (full_name, email, phone, username, hashed_pw),
            )

            conn.commit()
            conn.close()

            flash("Account created successfully!", "success")

            return redirect("/login")

        conn.close()

    return render_template("signup.html", error=error)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["user_login"]
        password = request.form["user_pass"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cur.fetchone()

        if not user:
            error = "Account not found"

        elif not bcrypt.checkpw(password.encode(), user["password"]):
            error = "Incorrect password"

        else:

            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "ADMIN":
                return redirect("/admin")
            else:
                return redirect("/dashboard")

        conn.close()

    return render_template("login.html", error=error)


# ---------------- USER DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE id=?", (session["user_id"],))

    user = cur.fetchone()

    cur.execute("SELECT * FROM museums")

    museums = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", username=user["username"], museums=museums)


@app.route("/booking")
def booking():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM museums LIMIT 1")

    museum = cur.fetchone()

    conn.close()

    return render_template("booking.html", museum=museum)


# ---------------- BOOK TICKET ----------------


@app.route("/book/<int:museum_id>", methods=["POST"])
def book_ticket(museum_id):

    if "user_id" not in session:
        return redirect("/login")

    visit_date = request.form["date"]

    adults = int(request.form["adults"])
    children = int(request.form["children"])

    ADULT_PRICE = 50
    CHILD_PRICE = 25

    total_amount = (
        adults * ADULT_PRICE
    ) + (
        children * CHILD_PRICE
    )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO bookings(
            user_id,
            museum_id,
            visit_date,
            adults,
            children,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            museum_id,
            visit_date,
            adults,
            children,
            total_amount
        )
    )

    booking_id = cur.lastrowid

    # Generate QR
    qr_data = f"BOOKING_ID:{booking_id}"

    qr = qrcode.make(qr_data)

    os.makedirs("static/qrcodes", exist_ok=True)

    qr_path = f"static/qrcodes/{booking_id}.png"

    qr.save(qr_path)
    cur.execute("SELECT * FROM bookings")
    print("ALL BOOKINGS =", cur.fetchall())

    conn.commit()
    conn.close()

    flash(
        f"Ticket booked successfully! Total Amount: ₹{total_amount}",
        "success"
    )

    return redirect("/history")

# ---------------- TICKET PAGE ----------------
@app.route("/ticket/<int:booking_id>")
def ticket(booking_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT bookings.id,
               museums.name,
               bookings.visit_date,
               bookings.adults,
               bookings.children,
               bookings.total_amount,
               bookings.status

        FROM bookings

        JOIN museums
        ON bookings.museum_id = museums.id

        WHERE bookings.id = ?
        """,
        (booking_id,)
    )

    booking = cur.fetchone()

    conn.close()

    return render_template(
        "ticket.html",
        booking=booking
    )

# ---------------- USER HISTORY ----------------
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
    """
    SELECT bookings.id,
           museums.name,
           bookings.visit_date,
           bookings.adults,
           bookings.children,
           bookings.total_amount,
           bookings.status

    FROM bookings

    JOIN museums
    ON bookings.museum_id = museums.id

    WHERE bookings.user_id = ?

    ORDER BY bookings.id DESC
    """,
    (session["user_id"],)
)
    bookings = cur.fetchall()
    print("BOOKINGS =", bookings)
    conn.close()
    return render_template("history.html", bookings=bookings)


# ---------------- CANCEL BOOKING ----------------
@app.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
    UPDATE bookings
    SET status='CANCELLED'
    WHERE id=? AND user_id=?
    """,
        (booking_id, session["user_id"]),
    )

    conn.commit()
    conn.close()

    flash("Booking cancelled successfully!", "success")

    return redirect("/history")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "ADMIN":
        return redirect("/dashboard")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT bookings.id,
           users.username,
           museums.name,
           bookings.visit_date,
           bookings.tickets,
           bookings.status

    FROM bookings

    JOIN users
    ON bookings.user_id = users.id

    JOIN museums
    ON bookings.museum_id = museums.id

    ORDER BY bookings.id DESC
    """)

    bookings = cur.fetchall()

    conn.close()

    return render_template("admin.html", bookings=bookings)


# ---------------- VERIFY TICKET ----------------
@app.route("/verify/<int:booking_id>")
def verify_ticket(booking_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "ADMIN":
        return redirect("/dashboard")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))

    booking = cur.fetchone()

    conn.close()

    if booking:
        return f"Ticket Verified Successfully! Booking ID: {booking_id}"

    return "Invalid Ticket"


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

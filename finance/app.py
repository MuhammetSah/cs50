import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # First grouping all the holdings
    holdings = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    portfolio = []

    for holding in holdings:
        # Getting the current prices
        quote = lookup(holding["symbol"])
        # Calculate the total value of shares
        value = holding["total_shares"] * quote["price"]
        portfolio.append({
            "symbol": holding["symbol"],
            "name": quote["name"],
            "shares": holding["total_shares"],
            "price": quote["price"],
            "value": value
        })

    # Checking the users cash
    cash_row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash_row[0]["cash"]

    total_value = 0
    for item in portfolio:
        total_value += item["value"]
    grand_total = cash + total_value

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # POST input
    if request.method == "POST":
        # Getting input
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        quote = lookup(symbol)

        # Validating user input
        if not quote:
            return apology("Invalid Symbol", 400)
        if not shares:
            return apology("Invalid amount of shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid amount of shares", 400)
        if shares < 1:
            return apology("Invalid amount of shares", 400)

        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        cost = shares * quote["price"]

        if cash < cost:
            return apology("Can't afford it", 400)
        else:
            timestamp = datetime.now()
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], symbol, shares, quote["price"], timestamp)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
            flash("Bought!")
            return redirect("/")

    # GET Input
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Symbol does not exist", 400)
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    # Validating the given parameter
    # Username
        if not username:
            return apology("Not a valid Username", 400)
    # Password
        if not password:
            return apology("Not a valid Password", 400)
        if not confirmation:
            return apology("Couldn't confirm your input", 400)
        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Hashing the password
        password = generate_password_hash(password)

        # Inserting new user
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)
        except ValueError:
            return apology("Already registered!", 400)
        return render_template("login.html")

        # Showing the Registration Form
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid Symbol", 400)
        symbol = symbol.upper()

        shares = request.form.get("shares")
        if not shares:
            return apology("Invalid amount of shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid amount of shares", 400)
        if shares < 1:
            return apology("Invalid amount of shares", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("Invalidy Symbol", 400)

        rows = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        shares_owned = rows[0]["total_shares"]
        if shares_owned is None:
            shares_owned = 0

        if shares_owned < shares:
            return apology("Don't have enough shares", 400)

        proceeds = shares * quote["price"]
        timestamp = datetime.now()

        db.execute("INSERT INTO transactions(user_id, symbol, shares,price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, quote["price"], timestamp)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, session["user_id"])

        flash("Sold!")
        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)

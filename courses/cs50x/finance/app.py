import os

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


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    """
    display would be like this:
        TOTAL = cash + sum(stocks)
        STOCK, shares, price(each), total for stock(shares*price)
        ... 
    """

    stocks = db.execute("""
    SELECT symbol, SUM(shares) as total_shares 
    FROM history 
    WHERE user_id = ? 
    GROUP BY symbol
    HAVING total_shares > 0;
    """, session["user_id"])

    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    total_cash = user_cash
    data = []
    for stock in stocks:
        info = lookup(stock["symbol"])
        symbol = info["symbol"]
        total_shares = stock["total_shares"]
        share_price = info["price"]
        total_stock_value = share_price * total_shares

        data.append({
            "symbol": symbol, 
            "total_shares": total_shares,
            "share_price": share_price,
            "total_stock_value": total_stock_value
        })
        total_cash += total_stock_value
    return render_template("index.html", stocks=data, cash=[usd(user_cash), usd(total_cash)])



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    if request.method == "POST":
        
        quote = request.form.get("symbol")
        if not quote or quote == "":
            return apology("Must provide symbol")
        quote = lookup(quote)
        if quote is None:
            return apology("Incorrect quote symbol", 403)

        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        user_id = session["user_id"]
        symbol = quote["symbol"]
        shares_amount = request.form.get("shares")
        current_price = quote["price"]

        try:
            shares_amount = int(shares_amount)
        except ValueError:
            return apology("must be integer", 403)
        
        if shares_amount <= 0:
            return apology("You can only but a positive amount of shares", 403)
        
        new_cash = user_cash - (shares_amount * current_price)
        if new_cash < 0:
            return apology("Not enough money to buy", 403)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
        db.execute("""
        INSERT INTO history
        (user_id, symbol, shares, price)
        VALUES(?, ?, ?, ?)
        """, user_id, symbol, shares_amount, current_price)

        return redirect("/")
        
    else:
        return render_template("buy.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    user_history = db.execute("SELECT * FROM history WHERE user_id=?", session["user_id"])
    return render_template("history.html", user_history=user_history)


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
        try:
            symbol = lookup(request.form.get("symbol"))
        except:
            return apology("Enter the correct symbot")
        return redirect(f"/quoted?name={symbol['name']}&price={symbol['price']}&symbol={symbol['symbol']}")
    else:
        return render_template("quote.html")    

@app.route("/quoted", methods=["GET"])
@login_required
def quoted():
    """Display the stock quote information"""
    name = request.args.get("name")
    price = usd(float(request.args.get("price")))
    symbol = request.args.get("symbol")
    return render_template("quoted.html", name=name, price=price, symbol=symbol)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""


    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)
        
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords should be equal", 403)
        
        try:
            hash = generate_password_hash(request.form.get("password"))
            name = request.form.get("username")
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, hash)
            return redirect("/")
        except(ValueError):
            return apology("User with this login already exist", 403)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("""
    SELECT symbol, SUM(shares) as total_shares 
        FROM history 
        WHERE user_id = ? 
        GROUP BY symbol
        HAVING total_shares > 0;
    """, session["user_id"])

    symbols = [stock["symbol"] for stock in stocks]
    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    #checks required: shares inputed(>0), symbol chosen, user has this stock, user can buy



    if request.method == "POST":
        # symbol chosen
        symbol = request.form.get("symbol")
        if not symbol or symbol == "":
            return apology("Must provide symbol")
        symbol_exist = lookup(symbol)
        if symbol_exist is None:
            return apology("Incorrect quote symbol", 403)
        # user actually has this stock(no change to html to inject)
        for stock_i in stocks:
            if (symbol == stock_i["symbol"]):
                symbol = stock_i["symbol"]
                break
        else:
            return apology("Stock actually doesnt exist")
        # shares inputed
        shares_sell_amount = request.form.get("shares")
        if shares_sell_amount is None or shares_sell_amount == "":
            return apology("Provide number of shares to sell")
        if not shares_sell_amount.isdigit():
            return apology("Not an integer number of shares")
        if int(shares_sell_amount) < 1:
            return apology("Can only sell positive integer amount of shares")
        
        # can sell
        for stock in stocks:
            if stock["symbol"] == symbol:
                user_shares = int(stock["total_shares"])
                break
        else:
            return apology("wtf")
        if user_shares < int(shares_sell_amount):
            return apology("cant sell more than you have")

        price = lookup(symbol)["price"]
        new_cash = user_cash + (price * int(shares_sell_amount))
        user_id = session["user_id"]
        shares_amount = -int(shares_sell_amount)

        print(f"SELL: Inserting {shares_amount} shares of {symbol}")  # Add this before db.execute
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
        db.execute("""
        INSERT INTO history
        (user_id, symbol, shares, price)
        VALUES(?, ?, ?, ?)
        """, user_id, symbol, shares_amount, price)


        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)

@login_required
@app.route("/add_cash", methods=["GET", "POST"])
def add_cash():

    if request.method == "POST":
        cash = request.form.get("cash")
        try:
            cash = float(cash)
            if cash < 0:
                return apology("Provide positive integer(n>0)")
        except ValueError:
            return apology("Must provide a valid number")
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        new_cash = float(user_cash) + float(cash)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        return redirect("/")
    else:
        return render_template("add_cash.html")
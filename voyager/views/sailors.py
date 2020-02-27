from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE


def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors as s")

def who_sailed(conn, boat_name):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.name = '{boat_name}'")

def on_date(conn, date):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid WHERE Voyages.date_of_voyage = '{date}'")

def what_boat_color(conn, color):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.color = '{color}'")

def add_sailor(conn, name, age, experience):
    return execute(conn, f"INSERT INTO Sailors(name, age, experience) VALUES ('{name}', {age}, {experience})")





def views(bp):

    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)
    
    

    @bp.route("/sailors/who-sailed", methods=["POST", "GET"])
    def _who_sailed():
        
        if request.method == "POST":
            with get_db() as conn:
                boat_name = request.form["boat-name"]
                rows = who_sailed(conn, boat_name)
            return render_template("table.html", name=boat_name, rows=rows)
        else:
            return "Hello"

    @bp.route("/sailors/who-sailed-on-date", methods=["POST", "GET"])
    def _on_date():

        if request.method == "POST":
            with get_db() as conn:
                the_date = request.form["date"]
                rows = on_date(conn, the_date)
            return render_template("table.html", name=the_date, rows=rows)
        else:
            return "Hello"
    
    @bp.route("/sailors/who-sailed-on-boat-of-color", methods=["POST", "GET"])
    def _boat_color():

        if request.method == "POST":
            with get_db() as conn:
                boat_color = request.form["color"]
                rows = what_boat_color(conn, boat_color)
            return render_template("table.html", name=boat_color, rows=rows)
        else:
            return "Hello"
    
    @bp.route("/sailors/add")
    def addsailorspage():
        return render_template("addsailors.html")


    @bp.route("/sailors/add", methods=["POST", "GET"])
    def _add_sailor():

        if request.method == "POST":
            with get_db() as conn:
                sailors_name = request.form["sailors-name"]
                sailors_age = request.form["sailors-age"]
                sailors_exp = request.form["sailors-exp"]
                add_sailor(conn, sailors_name, sailors_age, sailors_exp)
                return "SUCCESS"
        else:
            return "FAILURE"


from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute


def getAllHouses(conn):
    return execute(conn, "SELECT * FROM HOUSE")


def getAllAgents(conn):
    return execute(conn, "SELECT a.name, a.phoneNumber, a.email FROM AGENT AS a")


def getAllUsers(conn):
    return execute(conn, "SELECT * FROM USER")


def getAllHousesByAgent(conn, name):

    return execute(conn, f"SELECT h.name, h.price, h.address FROM HOUSE AS h INNER JOIN AGENT AS a ON h.aid = a.aid WHERE a.name='{name}'")


def getAllHousesInterested(conn, userName):

    return execute(conn, f"SELECT h.name FROM HOUSE AS h INNER JOIN User AS u INNER JOIN Interests as i on u.id = i.id WHERE u.name = '{userName}'")


def addHouse(conn, name, price, address, aid, rent, status, city):

    return execute(conn, f"INSERT INTO House(name, price, address, aid, rent, status, city) VALUES ('{name}', {price}, '{address}', {aid}, {rent}, '{status}', '{city}')")


def filteredSearchForHouses(conn, maxPrice, city, aid, rent):
    if aid:
        return execute(conn, f"SELECT h.name, h.price, h.address FROM House as h WHERE h.price <=  {maxPrice}  AND h.city= '{city}' AND h.aid= {aid} AND h.rent= {rent} AND h.status= 'active'")
    else:
        return execute(conn, f"SELECT h.name, h.price, h.address FROM House as h WHERE h.price <=  {maxPrice}  AND h.city= '{city}' AND h.rent= {rent} AND h.status= 'active'")


def addInterest(conn, userid, houseid):

    return execute(conn, f"INSERT INTO Interests(uid, hid) VALUES ({userid}, {houseid})")


def getMostPopularHouse(conn):
    return execute(conn, "SELECT h.name, count(*) FROM House AS h INNER JOIN Interests AS i ON h.hid=i.hid GROUP BY h.name ORDER BY count(*) DESC")


def findAgentByName(conn, name):
    return execute(conn, f"SELECT * FROM AGENT WHERE name = '{name}'")


def findUserByName(conn, name):
    return execute(conn, f"SELECT * FROM USER WHERE name = '{name}'")


def findHouseByName(conn, name):
    return execute(conn, f"SELECT * FROM HOUSE WHERE name = '{name}'")


def currentDate(conn):
    return execute(conn, "SELECT CURRENT_TIMESTAMP")


def addPurchase(conn, uid, hid, date):
    return execute(conn, f"INSERT INTO PURCHASE(uid, hid, date_of_purchase) VALUES({uid}, {hid}, '{date}')")


def updateHouse(conn, hid):
    return execute(conn, f"UPDATE HOUSE SET status='closed' WHERE hid = {hid}")


def addUser(conn, name, number, email):
    return execute(conn, f"INSERT INTO USER(name, phoneNumber, email) VALUES('{name}', {number}, '{email}')")


def findPurchaseByUser(conn, uid):
    return execute(conn, f"SELECT p.date_of_purchase, h.name FROM PURCHASE as p INNER JOIN HOUSE as h ON h.hid = p.hid WHERE p.uid = {uid}")


def views(bp):
    @bp.route("/all-houses")
    def all_houses():
        with get_db() as conn:
            rows = getAllHouses(conn)
        return render_template("table.html", name="all houses", rows=rows)

    @bp.route("/agent-houses", methods=["POST", "GET"])
    def all_agent_houses():

        with get_db() as conn:
            agent_name = request.form['agent-name']
            rows = getAllHousesByAgent(conn, agent_name)

        return render_template("table.html", name=f"Houses by {agent_name}", rows=rows)

    @bp.route("/search-houses", methods=["POST", "GET"])
    def house_search():

        if request.method == "POST":

            with get_db() as conn:
                price = request.form['price']
                city = request.form['city']
                try:
                    agentName = request.form['agent']
                    agent_id = (findAgentByName(conn, agentName))[0]['aid']
                except:
                    agent_id = None
                if request.form.get('rent'):
                    rent = request.form.get('rent')
                else:
                    rent = 0
                row = filteredSearchForHouses(
                    conn, price, city, agent_id, rent)
                print(rent)
            return render_template("searchhouses.html", name=f"Houses you searched for", rows=row)

    @bp.route("/add-interests")
    def addInterestsPage():
        return render_template("addinterests.html")

    @bp.route("/add-interests", methods=["POST", "GET"])
    def addInterests():
        if request.method == "POST":

            with get_db() as conn:
                name = request.form['name']
                housename = request.form['house']

                house_id = (findHouseByName(conn, housename))[0]['hid']
                user_id = (findUserByName(conn, name))[0]['uid']
                addInterest(conn, user_id, house_id)

                return "SUCCESS"

    @bp.route("/all-agents")
    def all_agents():

        with get_db() as conn:
            rows = getAllAgents(conn)

        return render_template("table.html", name="List of Agents", rows=rows)

    @bp.route("/add-house")
    def add_houses_page():
        return render_template("addhouses.html")

    @bp.route("/add-house", methods=["POST", "GET"])
    def add_house():
        if request.method == "POST":

            with get_db() as conn:
                house_name = request.form['name']
                house_price = request.form['price']
                house_address = request.form['address']
                house_agent_name = request.form['agent']
                house_status = request.form['status']
                house_city = request.form['city']
                try:
                    house_rent = request.form['rent']
                except:
                    house_rent = 0

                agent_id = (findAgentByName(conn, house_agent_name))[0]['aid']
                if (len(findHouseByName(conn, house_name)) >= 1):
                    return "Choose a different name for the house"

                addHouse(conn, house_name, house_price, house_address,
                         agent_id, house_rent, house_status, house_city)
                return "SUCCESS"

    @bp.route("/most-popular-houses", methods=["POST", "GET"])
    def pop_houses():
        with get_db() as conn:
            rows = getMostPopularHouse(conn)
            print(currentDate(conn)[0]['CURRENT_TIMESTAMP'].split()[0])
            return render_template("table.html", rows=rows, name="Most Popular Houses")

    @bp.route("/all-users")
    def all_users():
        with get_db() as conn:
            rows = getAllUsers(conn)
            return render_template("table.html", rows=rows, name="All users")

    @bp.route("/add-purchase")
    def purchase_page():
        return render_template('addpurchase.html')

    @bp.route("/add-purchase", methods=["POST", "GET"])
    def add_purchase():
        if request.method == "POST":
            with get_db() as conn:
                houseName = request.form['house']
                userName = request.form['name']
                uid = findUserByName(conn, userName)[0]['uid']
                hid = findHouseByName(conn, houseName)[0]['hid']
                date = currentDate(conn)[0]['CURRENT_TIMESTAMP'].split()[0]
                if findHouseByName(conn, houseName)[0]['status'] != 'active':
                    return "House has already been bought"

                addPurchase(conn, uid, hid, date)
                updateHouse(conn, hid)
                return "SUCCESS"

    @bp.route("/add-user")
    def user_page():
        return render_template('adduser.html')

    @bp.route("/add-user", methods=["POST", "GET"])
    def add_user():
        if request.method == "POST":
            with get_db() as conn:
                userName = request.form['name']
                email = request.form['email']
                phone = request.form['phone-number']
                if (len(findUserByName(conn, userName)) >= 1):
                    return "Someone already has that name"

                addUser(conn, userName, phone, email)
                return "SUCCESS"

    @bp.route("/user-purchases", methods=["POST", "GET"])
    def user_purchase():
        if request.method == "POST":
            with get_db() as conn:
                userName = request.form['user-name']
                uid = findUserByName(conn, userName)[0]['uid']
                rows = findPurchaseByUser(conn, uid)
                return render_template("table.html", rows=rows, name=f"Purchases by {userName}")

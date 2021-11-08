from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/nearest_station", methods=["POST"])
def nearest():
    def sanitize(place):
        return place if place else "Babson College"

    stop = mbta_helper.find_stop_near(
        sanitize(request.form["place"]), mbta_helper.get_stop_collections()
    )

    def to_string(stop):
        accessible = (
            "wheelchair accessible"
            if stop["wheelchair"]
            else "not wheelchair accessible"
        )
        return f"The nearest stop is {stop['name']}, and it is {accessible}."

    return render_template("index.html", message=to_string(stop))

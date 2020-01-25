from flask import Flask, jsonify, request, render_template
# jsonify jest do pewnego stopnia serializerem

stores = [
    {
        "name": "Pizzeria",
        "items": [
            {"name": "pizza_1", "price": 19.99},
            {"name": "pizza_2", "price": 19.99},
            {"name": "pizza_3", "price": 19.99}
        ],
    }
]


# wszystko co robimy z Flaskiem musi być przez ten app
app = Flask(__name__)


@app.route("/")
def home_index():
    return render_template("index.html")


@app.route("/template")
def example():
    return render_template("example.html", stores=stores)


@app.route("/hello_name/<string:name>")
def hello_name(name):
    return f"Hello {name}!"


@app.route("/store", methods=['POST'])
def store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def display_store(name):
    for item in stores:
        if item["name"] == name:
            return jsonify(item)

    return jsonify({'message': 'Nie ma takiego sklepu.'})


@app.route("/store")
def get_store():
    return jsonify({"stores": stores})


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            store["items"].append({
                "name": request_data["name"],
                "price": request_data["price"]
            })
            return jsonify(store)

    return jsonify({'message': 'Nie ma takiego sklepu.'})


@app.route("/store/<string:name>/items")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})

    return jsonify({'message': 'Nie ma takiego sklepu.'})


app.run(debug=True)
# uruchomienie w konsoli: python app.py

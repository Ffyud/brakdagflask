from flask import Flask
app = Flask(__name__)

@app.route("/")
def welkom():
    return "Welkom!"

@app.route("/bronnen", method=["GET"])
def geefBronnen():
    return bronService().selectAll(request.get_json())

if __name__ == "__main__":
    Schema()
    app.run(debug=True)        
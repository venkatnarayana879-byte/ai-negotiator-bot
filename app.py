from flask import Flask, request, jsonify

# -------------------
# Simple Buyer Agent Logic (Placeholder)
# Replace with your real Concordia YourBuyerAgent class
# -------------------
class BuyerAgent:
    def __init__(self, name):
        self.name = name

    def get_counter_offer(self, product, offer_price):
        # Example: Always counter 10 less if above 50
        if offer_price > 50:
            return offer_price - 10
        return offer_price

# Create Flask app and BuyerAgent instance
app = Flask(__name__)
buyer_bot = BuyerAgent(name="Data Analyst Buyer")

# -------------------
# Routes
# -------------------
@app.route("/")
def home():
    return "✅ Flask server is running! Use POST /negotiate to start a negotiation."

@app.route("/negotiate", methods=["POST"])
def negotiate():
    """
    Accepts JSON:
    {
        "product": "mangoes",
        "offer_price": 60
    }
    """
    data = request.get_json()

    # Validate input
    if not data or "product" not in data or "offer_price" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    product = data["product"]
    try:
        offer_price = float(data["offer_price"])
    except ValueError:
        return jsonify({"error": "Invalid offer_price"}), 400

    # Get counter-offer from Buyer Agent
    counter_offer = buyer_bot.get_counter_offer(product, offer_price)

    return jsonify({
        "product": product,
        "original_offer": offer_price,
        "counter_offer": counter_offer,
        "message": f"{buyer_bot.name} suggests {counter_offer} for {product}"
    })

# -------------------
# Run Server
# -------------------
if __name__ == "__main__":
    app.run(debug=True)

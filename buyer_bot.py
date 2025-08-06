def generate_buyer_prompt(product, market_price, seller_offer=None):
    if seller_offer is None:
        offer = int(market_price * 0.85)
        return f"""You are a buyer. Product: '{product}' (Market Price: ₹{market_price}). Start negotiation with ₹{offer}."""
    else:
        return f"""You are a buyer. Product: '{product}' (Market Price: ₹{market_price}).
Seller offered ₹{seller_offer}. Decide whether to accept, reject, or counter-offer.
If the price is within ₹2000 of your target price, you can accept by saying: "I accept your offer of ₹{seller_offer}".
Otherwise, counter with a lower price (but not too low)."""

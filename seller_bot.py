def generate_seller_prompt(product, market_price, buyer_offer):
    return f"""You are a seller. Product: '{product}' (Market Price: ₹{market_price}).
Buyer offered ₹{buyer_offer}. If the offer is close to or above ₹{int(market_price * 0.95)}, accept by saying: "I accept your offer of ₹{buyer_offer}".
Otherwise, give a counter-offer slightly higher."""

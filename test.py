# test.py

from llm_utils import generate_response
import re

def extract_price(text: str) -> int:
    """
    Extracts the **last reasonable-looking number** (e.g., ₹21250) from a string.
    """
    matches = re.findall(r"₹?\s?(\d{4,6})", text)
    if matches:
        return int(matches[-1])
    return None

def negotiate(product: str):
    print(f"\n🔍 Estimating market price for: {product}")

    pricing_prompt = (
        f"You are a pricing expert. Estimate the average market price (in ₹) for this product:\n"
        f"'{product}'. Respond only with a number like: 45000"
    )
    market_price_str = generate_response(pricing_prompt)
    try:
        market_price = int(re.findall(r"\d+", market_price_str)[-1])
    except:
        print("❌ Could not determine market price.")
        return

    print(f"\n🧠 Predicted market price: ₹{market_price}\n")
    print(f"\n📦 Starting negotiation for '{product}' (Market Price: ₹{market_price})\n")

    target_price = int(market_price * 0.85)
    current_offer = target_price
    buyer_offer = None

    for round_num in range(5):
        # Buyer speaks
        buyer_prompt = (
            f"You are a buyer. Product: '{product}' (Market Price: ₹{market_price}). "
            f"Start negotiation with ₹{target_price}." if round_num == 0 else
            f"You are a buyer. Product: '{product}' (Market Price: ₹{market_price}).\n"
            f"Seller offered ₹{current_offer}. Decide whether to accept, reject, or counter-offer.\n"
            f"If the price is within ₹2000 of your target price, you can accept by saying: "
            f"\"I accept your offer of ₹{current_offer}\".\n"
            f"Otherwise, counter with a lower price (but not too low)."
        )
        buyer_response = generate_response(buyer_prompt)
        print(f"🟢 Buyer: {buyer_response}\n")

        if "accept" in buyer_response.lower():
            print("✅ Buyer accepted the deal.")
            return

        buyer_offer = extract_price(buyer_response)
        if buyer_offer is None:
            print("❌ Buyer response invalid. Ending negotiation.")
            return

        # Seller responds
        seller_prompt = (
            f"You are a seller. Product: '{product}' (Market Price: ₹{market_price}).\n"
            f"Buyer offered ₹{buyer_offer}. If the offer is close to or above ₹{int(market_price * 0.85)}, "
            f"accept by saying: \"I accept your offer of ₹{buyer_offer}\".\n"
            f"Otherwise, give a counter-offer slightly higher."
        )
        seller_response = generate_response(seller_prompt)
        print(f"🔴 Seller: {seller_response}\n")

        if "accept" in seller_response.lower():
            print("✅ Seller accepted the deal.")
            return

        current_offer = extract_price(seller_response)
        if current_offer is None:
            print("❌ Seller response invalid. Ending negotiation.")
            return

    print("❌ Negotiation failed after 5 rounds.")

if __name__ == "__main__":
    product_name = input("🔍 Enter a product name to negotiate: ")
    negotiate(product_name)

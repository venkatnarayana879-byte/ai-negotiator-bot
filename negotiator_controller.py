import time
import re
from buyer_bot import generate_buyer_prompt
from seller_bot import generate_seller_prompt
from llama_api import call_llama_api

def extract_offer(text):
    """
    Extracts ₹amount from a given string.
    E.g., "I offer ₹42000" → 42000
    """
    match = re.search(r"₹?(\d{4,6})", text)
    if match:
        return int(match.group(1))
    return None

def run_negotiation(product, market_price):
    print(f"\n📦 Starting negotiation for '{product}' (Market Price: ₹{market_price})\n")

    start_time = time.time()

    # Round 1: Buyer makes first offer
    buyer_prompt = generate_buyer_prompt(product, market_price)
    buyer_response = call_llama_api(buyer_prompt)
    print("🟢 Buyer:", buyer_response)

    for round_num in range(5):  # Max 5 negotiation rounds
        buyer_offer = extract_offer(buyer_response)

        # Seller responds
        seller_prompt = generate_seller_prompt(product, market_price, buyer_offer)
        seller_response = call_llama_api(seller_prompt)
        print("🔴 Seller:", seller_response)

        if "accept" in seller_response.lower():
            print("\n✅ Seller accepted the deal.")
            return

        seller_offer = extract_offer(seller_response)

        # Buyer responds
        buyer_prompt = generate_buyer_prompt(product, market_price, seller_offer)
        buyer_response = call_llama_api(buyer_prompt)
        print("🟢 Buyer:", buyer_response)

        if "accept" in buyer_response.lower():
            print("\n✅ Buyer accepted the deal.")
            return

        # Time check
        if time.time() - start_time > 180:
            print("\n⏱ Negotiation timed out (3 minutes).")
            return

    print("\n❌ Negotiation failed after 5 rounds.")

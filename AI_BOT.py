import ollama
import random
import time
import re

MODEL_NAME = "llama3.1:8b"

def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []
        self.last_price = None
        self.persona_hits = 0
        self.messages_count = 0

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))
        if match:
            return int(match.group(1))
        return None

    def check_persona_keywords(self, text):
        keywords = {
            "Aggressive Trader": ["urgent", "last offer", "take it or leave it", "rush", "final"],
            "Smooth Diplomat": ["win-win", "together", "mutual", "partnership", "collaborate"],
            "Data-Driven Analyst": ["data", "trend", "market", "statistics", "analysis"],
        }
        if self.persona in keywords:
            for kw in keywords[self.persona]:
                if kw.lower() in text.lower():
                    self.persona_hits += 1
                    break
        self.messages_count += 1

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = ("Negotiate to strike a profitable deal. "
                "Always mention your price offer in ₹ in every message. "
                "Stay true to your persona at all times.\n")
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self, time_left):
        prompt = self.generate_prompt()
        # Fallback deal closer if < 20 seconds left
        if time_left < 20:
            if self.role == "buyer":
                offer = self.limit
                response = f"Time is almost up! Let's settle for ₹{offer} — deal?"
            else:
                offer = self.limit
                response = f"Clock’s ticking! Final price: ₹{offer}. Take it or leave it."
        else:
            response = call_llama(prompt).strip()

        price = self.extract_price(response)
        if price:
            self.last_price = price

        self.check_persona_keywords(response)
        self.history.append(f"{self.name}: {response}")
        return response

def run_negotiation_round(buyer, seller, product_name, market_price, turns=10, time_limit_sec=180):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    final_price = None

    for turn in range(turns):
        elapsed = time.time() - start_time
        time_left = time_limit_sec - elapsed
        if time_left <= 0:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        print(f"\n--- Turn {turn + 1} ---")

        seller_response = seller.respond(time_left)
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        time_left = time_limit_sec - elapsed
        if time_left <= 0:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        buyer_response = buyer.respond(time_left)
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached!")
            break

    if not final_price:
        print("\n❌ No deal reached in allowed turns.")
        return None

    # Scoring
    profit_savings_score = 0
    if final_price:
        if buyer.role == "buyer":
            savings = buyer.limit - final_price
            profit_savings_score = (savings / buyer.limit) * 40
        else:
            profit = final_price - seller.limit
            profit_savings_score = (profit / final_price) * 40

    persona_score = ((buyer.persona_hits / max(1, buyer.messages_count)) +
                     (seller.persona_hits / max(1, seller.messages_count))) / 2 * 40

    speed_bonus = max(0, (time_limit_sec - (time.time() - start_time)) / time_limit_sec) * 20

    total_score = profit_savings_score + persona_score + speed_bonus

    print("\n📊 Match Report")
    print(f"Final Price: ₹{final_price}")
    print(f"Profit/Savings Score: {profit_savings_score:.2f}/40")
    print(f"Persona Consistency Score: {persona_score:.2f}/40")
    print(f"Speed Bonus: {speed_bonus:.2f}/20")
    print(f"🏆 Total Score: {total_score:.2f}/100")

    return final_price

if __name__ == "__main__":
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (Aggressive Trader / Smooth Diplomat / Data-Driven Analyst): ")
    buyer_persona = input("Enter Buyer Persona (Aggressive Trader / Smooth Diplomat / Data-Driven Analyst): ")
    market_price = int(input("Enter Market Price: ₹"))
    seller_price = int(input("Enter Seller Minimum Price: ₹"))
    buyer_price = int(input("Enter Buyer Maximum Price: ₹"))

    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Market Price: ₹{market_price}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes.\n")

    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    final_price = run_negotiation_round(buyer, seller, product_name, market_price)

    if final_price:
        print(f"\n💰 Final Agreed Price: ₹{final_price}")
    else:           
        print("\n💔 No Deal")




 
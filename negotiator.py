'''import ollama
import random
import time

# Use local llama3.1:8b
MODEL_NAME = "llama3.1:8b"

# Function to send a message to LLaMA 3.1 via Ollama
def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Negotiation Agent Class
class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Respond with your next negotiation message.\n"
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        self.history.append(f"{self.name}: {response}")
        return response

# Negotiation Function with Time Limit
def run_negotiation_round(buyer, seller, product_name, turns, time_limit_sec):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    for turn in range(turns):
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0

        print(f"\n--- Turn {turn + 1} ---")
        
        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            print("\n✅ Deal Reached within time!")
            return 1

    print("\n❌ No deal reached in allowed turns.")
    return 0

if __name__ == "__main__":
    # Inputs
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    turns = int(input("Enter number of turns: "))
    market_price = int(input("Enter Market Price: ₹"))

    # Auto-set seller and buyer price limits
    seller_price = int(market_price * (1 + random.uniform(0.10, 0.20)))  # +10% to +20%
    buyer_price = int(market_price * (1 - random.uniform(0.05, 0.15)))  # -5% to -15%

    # Show setup summary
    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Turns Allowed: {turns}")
    print(f"Market Price: ₹{market_price}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes or points  = 0.\n")

    # Create agents
    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    # Run negotiation
    points = run_negotiation_round(buyer, seller, product_name, turns, 180)
    print(f"\n🏆 Final Points: {points}")
'''


'''
import ollama
import random
import time
import re

# Use local llama3.1:8b
MODEL_NAME = "llama3.1:8b"

# Function to send a message to LLaMA 3.1 via Ollama
def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Negotiation Agent Class
class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []
        self.last_price = None  # Track last offered price

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))  # Find first number
        if match:
            return int(match.group(1))
        return None

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Always mention your price offer in ₹ in every message.\n"
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        price = self.extract_price(response)
        if price:
            self.last_price = price
        self.history.append(f"{self.name}: {response}")
        return response

# Negotiation Function with Time Limit
def run_negotiation_round(buyer, seller, product_name, turns, time_limit_sec):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    for turn in range(turns):
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        print(f"\n--- Turn {turn + 1} ---")
        
        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        # Check if deal is reached
        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached within time!")
            return 1, final_price

    print("\n❌ No deal reached in allowed turns.")
    return 0, None

if __name__ == "__main__":
    # Inputs
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    turns = int(input("Enter number of turns: "))
    market_price = int(input("Enter Market Price: ₹"))

    # Auto-set seller and buyer price limits
    seller_price = int(market_price * (1 + random.uniform(0.10, 0.20)))  # +10% to +20%
    buyer_price = int(market_price * (1 - random.uniform(0.05, 0.15)))  # -5% to -15%

    # Show setup summary
    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Turns Allowed: {turns}")
    print(f"Market Price: ₹{market_price}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes or points = 0.\n")

    # Create agents
    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    # Run negotiation
    points, final_price = run_negotiation_round(buyer, seller, product_name, turns, 180)

    print(f"\n🏆 Final Points: {points}")
    if final_price:
        print(f"💰 Final Agreed Price: ₹{final_price}")'''



'''

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

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))
        if match:
            return int(match.group(1))
        return None

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Always mention your price offer in ₹ in every message.\n"
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        price = self.extract_price(response)
        if price:
            self.last_price = price
        self.history.append(f"{self.name}: {response}")
        return response

def run_negotiation(buyer, seller, product_name, time_limit_sec):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    while True:
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached within time!")
            return 1, final_price

if __name__ == "__main__":
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    market_price = int(input("Enter Market Price: ₹"))

    seller_price = int(market_price * (1 + random.uniform(0.10, 0.20)))
    buyer_price = int(market_price * (1 - random.uniform(0.05, 0.15)))

    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Market Price: ₹{market_price}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes or points = 0.\n")

    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    points, final_price = run_negotiation(buyer, seller, product_name, 180)

    print(f"\n🏆 Final Points: {points}")
    if final_price:
        print(f"💰 Final Agreed Price: ₹{final_price}")
'''



'''
import ollama
import random
import time
import re

# Use local llama3.1:8b
MODEL_NAME = "llama3.1:8b"

# FAQ Rules for context
FAQ_RULES = """
Frequently Asked Questions (Competition Rules):
- You must only use the Llama-3-8B API for negotiations.
- No deal in 3 minutes = 0 points. Plan to close fast!
- You know your own price limit, but not your opponent's.
- Teams can mix skill sets (coders, strategists, domain experts).
- Always include a ₹ price in every message.
"""

# Function to send a message to LLaMA 3.1 via Ollama
def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Negotiation Agent Class
class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []
        self.last_price = None  # Track last offered price

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))  # Find first number
        if match:
            return int(match.group(1))
        return None

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Always mention your price offer in ₹ in every message.\n"
        return intro + task + FAQ_RULES + "\nConversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        price = self.extract_price(response)
        if price:
            self.last_price = price
        self.history.append(f"{self.name}: {response}")
        return response

# Negotiation Function with Time Limit
def run_negotiation_round(buyer, seller, product_name, turns, time_limit_sec):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    for turn in range(turns):
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        print(f"\n--- Turn {turn + 1} ---")
        
        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached. Points: 0")
            return 0, None

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        # Check if deal is reached
        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached within time!")
            return 1, final_price

    print("\n❌ No deal reached in allowed turns.")
    return 0, None

if __name__ == "__main__":
    # Inputs
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    market_price = int(input("Enter Market Price: ₹"))

    # Auto-set turns (random between 6–10)
    turns = random.randint(6, 10)

    # Auto-set seller and buyer price limits
    seller_price = int(market_price * (1 + random.uniform(0.10, 0.20)))  # +10% to +20%
    buyer_price = int(market_price * (1 - random.uniform(0.05, 0.15)))  # -5% to -15%

    # Show setup summary
    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Turns Allowed (auto): {turns}")
    print(f"Market Price: ₹{market_price}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes or points = 0.\n")

    # Create agents
    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    # Run negotiation
    points, final_price = run_negotiation_round(buyer, seller, product_name, turns, 180)

    print(f"\n🏆 Final Points: {points}")
    if final_price:
        print(f"💰 Final Agreed Price: ₹{final_price}")'''

'''
import ollama
import time
import re

# Use local llama3.1:8b
MODEL_NAME = "llama3.1:8b"

# Function to send a message to LLaMA 3.1 via Ollama
def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Negotiation Agent Class
class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []
        self.last_price = None  # Track last offered price

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))  # Find first number
        if match:
            return int(match.group(1))
        return None

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Always mention your price offer in ₹ in every message.\n"
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        price = self.extract_price(response)
        if price:
            self.last_price = price
        self.history.append(f"{self.name}: {response}")
        return response

# Negotiation Function with Time Limit
def run_negotiation_round(buyer, seller, product_name, time_limit_sec):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    turn = 1
    while True:
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        print(f"\n--- Turn {turn} ---")
        
        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached within time!")
            return final_price

        turn += 1

if __name__ == "__main__":
    # Inputs
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    seller_price = int(input("Enter Seller's Minimum Price (₹): "))
    buyer_price = int(input("Enter Buyer's Maximum Price (₹): "))

    # Show setup summary
    print("\n📋 Negotiation Setup")
    print(f"Product: {product_name}")
    if product_desc:
        print(f"Description: {product_desc}")
    print(f"Seller Persona: {seller_persona}")
    print(f"Buyer Persona: {buyer_persona}")
    print(f"Seller's Minimum Price: ₹{seller_price}")
    print(f"Buyer's Maximum Price: ₹{buyer_price}")
    print("Deal must be reached within 3 minutes.\n")

    # Create agents
    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    # Run negotiation
    final_price = run_negotiation_round(buyer, seller, product_name, 180)

    if final_price:
        print(f"💰 Final Agreed Price: ₹{final_price}")
    else:
        print("❌ No deal reached.")
'''





import ollama
import random
import time
import re

# Use local llama3.1:8b
MODEL_NAME = "llama3.1:8b"

# Function to send a message to LLaMA 3.1 via Ollama
def call_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Negotiation Agent Class
class NegotiationAgent:
    def __init__(self, name, role, limit, persona):
        self.name = name
        self.role = role
        self.limit = limit
        self.persona = persona
        self.history = []
        self.last_price = None  # Track last offered price

    def extract_price(self, text):
        match = re.search(r"₹?(\d+)", text.replace(",", ""))  # Find first number
        if match:
            return int(match.group(1))
        return None

    def generate_prompt(self):
        conversation = "\n".join(self.history)
        intro = f"You are a {self.persona} playing the role of a {self.role.upper()}.\n"
        task = f"Your {'maximum budget' if self.role == 'buyer' else 'minimum price'} is ₹{self.limit}.\n"
        goal = "Negotiate to strike a profitable deal. Always mention your price offer in ₹ in every message.\n"
        return intro + task + "Conversation so far:\n" + conversation + "\n" + goal

    def respond(self):
        prompt = self.generate_prompt()
        response = call_llama(prompt).strip()
        price = self.extract_price(response)
        if price:
            self.last_price = price
        self.history.append(f"{self.name}: {response}")
        return response

# Negotiation Function with 3-min Time Limit
def run_negotiation_round(buyer, seller, product_name, turns=10, time_limit_sec=180):
    buyer.history = []
    seller.history = []
    start_time = time.time()

    print("\n🟡 Negotiation Begins!\n")
    intro_message = f"{seller.name}: Let's begin. I have a great deal on {product_name}."
    seller.history.append(intro_message)
    buyer.history.append(intro_message)
    print(intro_message)

    for turn in range(turns):
        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        print(f"\n--- Turn {turn + 1} ---")
        
        seller_response = seller.respond()
        print(f"{seller.name}: {seller_response}")
        buyer.history.append(f"{seller.name}: {seller_response}")

        elapsed = time.time() - start_time
        if elapsed > time_limit_sec:
            print("\n⏳ Time’s up! No deal reached.")
            return None

        buyer_response = buyer.respond()
        print(f"{buyer.name}: {buyer_response}")
        seller.history.append(f"{buyer.name}: {buyer_response}")

        # Check if deal is reached
        if "deal" in seller_response.lower() or "deal" in buyer_response.lower():
            final_price = buyer.last_price if buyer.last_price else seller.last_price
            print("\n✅ Deal Reached within time!")
            return final_price

    print("\n❌ No deal reached in allowed turns.")
    return None

if __name__ == "__main__":
    # Inputs
    product_name = input("Enter the product for negotiation: ")
    product_desc = input("Describe the product briefly (optional): ")
    seller_persona = input("Enter Seller Persona (e.g., Aggressive Trader): ")
    buyer_persona = input("Enter Buyer Persona (e.g., Data-Driven Analyst): ")
    market_price = int(input("Enter Market Price: ₹"))
    seller_price = int(input("Enter Seller Minimum Price: ₹"))
    buyer_price = int(input("Enter Buyer Maximum Price: ₹"))

    # Show setup summary
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

    # Create agents
    seller = NegotiationAgent(name="Seller", role="seller", limit=seller_price, persona=seller_persona)
    buyer = NegotiationAgent(name="Buyer", role="buyer", limit=buyer_price, persona=buyer_persona)

    # Run negotiation
    final_price = run_negotiation_round(buyer, seller, product_name)

    if final_price:
        print(f"\n💰 Final Agreed Price: ₹{final_price}")
    else:       
        print("\n💔 No Deal")

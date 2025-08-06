import random

def call_llama_api(prompt):
    """
    Mock function to simulate LLaMA API response.
    In actual use, this would call the real API.
    """
    print("🧠 Mock LLaMA Prompt:\n" + prompt)

    # Basic simulation
    if "pricing expert" in prompt:
        price = random.randint(30000, 50000)
        print(f"🧠 Predicted market price: ₹{price}\n")
        return str(price)

    if "buyer" in prompt.lower():
        if "Seller offered" in prompt:
            return "I'll offer ₹" + str(random.randint(32000, 34000))
        else:
            return "I'll offer ₹" + str(random.randint(30000, 36000))

    if "seller" in prompt.lower():
        if "accept your offer" in prompt:
            return prompt.split("accept your offer of")[1].strip().split('"')[0]
        if "Buyer offered" in prompt:
            return "I'll offer ₹" + str(random.randint(33000, 35000))

    return "I accept your offer of ₹" + str(random.randint(33000, 35000))

def predict_market_price(product_name):
    """
    Predicts market price using the mock LLaMA prompt.
    """
    print("🧠 Mock LLaMA Prompt:")
    print(f"You are a pricing expert. Estimate the average market price (in ₹) for this product:\n    '{product_name}'. Respond only with a number like: 45000")
    price = random.randint(30000, 50000)
    print(f"🧠 Predicted market price: ₹{price}\n")
    return price

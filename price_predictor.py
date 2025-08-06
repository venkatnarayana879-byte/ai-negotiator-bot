from llama_api import call_llama_api
import re

def predict_price(product_description):
    prompt = f"""
    You are a pricing expert. Estimate the average market price (in ₹) for this product:
    '{product_description}'. Respond only with a number like: 45000
    """

    response = call_llama_api(prompt)

    # Extract just the number
    match = re.search(r"\d{4,6}", response)
    if match:
        return int(match.group(0))
    
    return 50000  # default/fallback price

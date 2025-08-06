# llm_utils.py

try:
    import ollama
    USE_OLLAMA = True
except ImportError:
    print("⚠️ 'ollama' module not found. Using mock responses.")
    USE_OLLAMA = False

def generate_response(prompt: str, model: str = "llama3") -> str:
    if USE_OLLAMA:
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content'].strip()
    else:
        # Mock fallback if ollama is not available
        if "pricing expert" in prompt.lower():
            return "25000"
        elif "buyer" in prompt.lower():
            return ("Hi there! I'm really interested in this old bike, it looks like it's been well-maintained and has a lot of character. "
                    "However, I was hoping we could discuss the price a bit.\n\n"
                    "As someone who's looking for a reliable ride, I think ₹25000 is a bit steep for me. "
                    "Would you be willing to meet me halfway at ₹21250?")
        elif "seller" in prompt.lower():
            return "I accept your offer of ₹21250"
        return "Let's negotiate."

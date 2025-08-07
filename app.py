import streamlit as st
from llm_utils import generate_response

st.set_page_config(page_title="🤝 AI Negotiator Bot", layout="centered")

st.title("🤝 AI Negotiator Bot")
st.markdown("""
This AI agent simulates a **negotiation between a buyer and a seller** over a given product using a large language model (LLM).
""")

# --- Product input
product = st.text_input("🔍 Enter a product name to negotiate:", "")

if product:
    with st.spinner("🧠 Predicting market price..."):
        market_price = generate_response(
            f"You are a pricing expert. Estimate the average market price (in ₹) for this product:\n'{product}'. Respond only with a number like: 45000"
        )

    try:
        market_price = int(market_price)
        st.success(f"🧠 Predicted market price: ₹{market_price}")
    except ValueError:
        st.error("❌ Could not determine a valid market price.")
        st.stop()

    st.markdown(f"### 📦 Negotiating for **{product}**")

    # --- Buyer Message
    buyer_offer = int(market_price * 0.85)
    buyer_msg = generate_response(
        f"You are a buyer. Product: '{product}' (Market Price: ₹{market_price}). Start negotiation with ₹{buyer_offer}."
    )
    st.markdown(f"#### 🟢 Buyer:")
    st.info(buyer_msg)

    # --- Seller Message (fixed prompt)
    seller_msg = generate_response(
        f"You are a seller. Product: '{product}' (Market Price: ₹{market_price}).\n"
        f"Buyer offered ₹{buyer_offer}. If the offer is close to or above ₹{int(market_price * 0.85)}, accept by saying: 'I accept your offer of ₹{buyer_offer}'.\n"
        "Otherwise, give a counter-offer slightly higher."
    )
    st.markdown(f"#### 🔴 Seller:")
    st.success(seller_msg)

    # --- Final outcome
    if "I accept" in seller_msg:
        st.markdown("✅ **Deal closed successfully!**")
    else:
        st.markdown("🔁 **Negotiation continues...**")

def run_full_negotiation_test(buyer_agent, seller_agent, product, buyer_budget):
    """
    Simulate negotiation between buyer_agent and seller_agent for a single product.
    Returns detailed results including final price, rounds, and conversation.
    """
    context = NegotiationContext(
        product=product,
        your_budget=buyer_budget,
        current_round=0,
        seller_offers=[],
        your_offers=[],
        messages=[]
    )

    # Seller opens
    seller_price, seller_msg = seller_agent.get_opening_price(product)
    context.seller_offers.append(seller_price)
    context.messages.append({"role": "seller", "message": seller_msg})

    deal_made = False
    final_price = None

    for round_num in range(10):
        context.current_round = round_num + 1

        # Buyer responds
        if round_num == 0:
            buyer_offer, buyer_msg = buyer_agent.generate_opening_offer(context)
            status = DealStatus.ONGOING
        else:
            status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
                context, seller_price, seller_msg
            )

        context.your_offers.append(buyer_offer)
        context.messages.append({"role": "buyer", "message": buyer_msg})

        if status == DealStatus.ACCEPTED:
            deal_made = True
            final_price = seller_price
            break

        # Seller responds
        seller_price, seller_msg, seller_accepts = seller_agent.respond_to_buyer(buyer_offer, round_num, product)
        context.seller_offers.append(seller_price)
        context.messages.append({"role": "seller", "message": seller_msg})

        if seller_accepts:
            deal_made = True
            final_price = buyer_offer
            break

    result = {
        "deal_made": deal_made,
        "final_price": final_price,
        "rounds": context.current_round,
        "savings": buyer_budget - final_price if deal_made else 0,
        "savings_pct": ((buyer_budget - final_price) / buyer_budget * 100) if deal_made else 0,
        "below_market_pct": ((product.base_market_price - final_price) / product.base_market_price * 100) if deal_made else 0,
        "conversation": context.messages
    }
    return result


def test_buyer_vs_seller(buyer_agent_class, seller_agent_class):
    """
    Run multiple negotiation scenarios between your buyer and seller agents.
    """
    test_products = [
        Product(
            name="Alphonso Mangoes",
            category="Mangoes",
            quantity=100,
            quality_grade="A",
            origin="Ratnagiri",
            base_market_price=180000,
            attributes={"ripeness": "optimal", "export_grade": True}
        ),
        Product(
            name="Kesar Mangoes", 
            category="Mangoes",
            quantity=150,
            quality_grade="B",
            origin="Gujarat",
            base_market_price=150000,
            attributes={"ripeness": "semi-ripe", "export_grade": False}
        )
    ]

    buyer_agent = buyer_agent_class("TestBuyer")
    seller_agent = seller_agent_class("TestSeller")

    total_savings = 0
    deals_made = 0

    print("="*60)
    print(f"TESTING BUYER VS SELLER")
    print("="*60)

    for product in test_products:
        for scenario in ["easy", "medium", "hard"]:
            if scenario == "easy":
                buyer_budget = int(product.base_market_price * 1.2)
            elif scenario == "medium":
                buyer_budget = int(product.base_market_price * 1.0)
            else:
                buyer_budget = int(product.base_market_price * 0.9)

            print(f"\nTest: {product.name} - {scenario} scenario")
            print(f"Your Budget: ₹{buyer_budget:,} | Market Price: ₹{product.base_market_price:,}")

            result = run_full_negotiation_test(buyer_agent, seller_agent, product, buyer_budget)

            if result["deal_made"]:
                deals_made += 1
                total_savings += result["savings"]
                print(f"✅ DEAL at ₹{result['final_price']:,} in {result['rounds']} rounds")
                print(f"   Savings: ₹{result['savings']:,} ({result['savings_pct']:.1f}%)")
                print(f"   Below Market: {result['below_market_pct']:.1f}%")
            else:
                print(f"❌ NO DEAL after {result['rounds']} rounds")

    print("\n" + "="*60)
    print("SUMMARY")
    print(f"Deals Completed: {deals_made}/{len(test_products)*3}")
    print(f"Total Savings: ₹{total_savings:,}")
    print(f"Success Rate: {deals_made/(len(test_products)*3)*100:.1f}%")
    print("="*60)


# Example usage:
# test_buyer_vs_seller(YourBuyerAgent, YourSellerAgent)
if __name__ == "__main__":
    from your_buyer_agent_file import YourBuyerAgent
    from your_seller_agent_file import YourSellerAgent

    test_buyer_vs_seller(YourBuyerAgent, YourSellerAgent)


from langchain_core.tools import tool

ORDERS = {
    "TN1001": {"item": "Laptop Pro 14", "status": "Shipped", "eta": "2 days"},
    "TN1002": {"item": "Noise-cancel Earbuds", "status": "Processing", "eta": "5 days"},
    "TN1003": {"item": "Phone X", "status": "Delivered", "eta": "-"},
}

POLICIES = {
    "returns": "Returns accepted within 30 days in original packaging.",
    "warranty": "All electronics carry a 1-year manufacturer warranty.",
    "shipping": "Free shipping above Rs. 999. Delivery in 3-5 days.",
}

@tool
def get_order_status(order_id: str) -> str:
    """Look up a TechNova order by its order ID, such as TN1001."""
    normalized = order_id.strip().upper()
    order = ORDERS.get(normalized)
    if not order:
        return f"I couldn't find order {normalized}. Please check the order ID and try again."
    return (
        f"Order {normalized}: {order['item']}; status: {order['status']}; "
        f"estimated delivery: {order['eta']}."
    )

@tool
def get_policy(topic: str) -> str:
    """Get TechNova store policy information. Topic should be returns, warranty, or shipping."""
    normalized = topic.strip().lower()
    if normalized not in POLICIES:
        valid = ", ".join(POLICIES)
        return f"I don't have a policy for '{topic}'. Available topics are: {valid}."
    return POLICIES[normalized]

tools = [get_order_status, get_policy]

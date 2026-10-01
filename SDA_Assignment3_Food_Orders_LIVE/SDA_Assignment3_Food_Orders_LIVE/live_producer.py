"""Continuously generate simulated food-order events for the live dashboard."""

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("live_orders.json")
SEED_FILE = Path("sample_data.json")
INTERVAL_SECONDS = 2

RESTAURANTS = ["REST101", "REST102", "REST103", "REST104", "REST105"]
PAYMENTS = ["UPI", "credit_card", "debit_card", "wallet", "cash_on_delivery"]
STATUSES = ["confirmed", "preparing", "pending", "out_for_delivery", "delivered"]
SOURCES = ["android_app", "ios_app", "website"]

def main():
    seed = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    orders = list(seed)
    DATA_FILE.write_text(json.dumps(orders, indent=2), encoding="utf-8")
    counter = len(orders) + 1

    print("Live producer started.")
    print("Writing a new order every 2 seconds to live_orders.json")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            quantity = random.randint(1, 4)
            amount = round(random.uniform(220, 1800) * quantity, 2)
            order = {
                "order_id": f"FOOD{2000 + counter}",
                "customer_id": f"CUS{300 + counter}",
                "restaurant_id": random.choice(RESTAURANTS),
                "item_id": f"ITEM{500 + random.randint(1, 10)}",
                "quantity": quantity,
                "amount": amount,
                "payment_method": random.choice(PAYMENTS),
                "order_status": random.choice(STATUSES),
                "source": random.choice(SOURCES),
                "event_timestamp": datetime.now(timezone.utc).isoformat(),
            }
            orders.append(order)
            DATA_FILE.write_text(json.dumps(orders, indent=2), encoding="utf-8")
            print(
                f"New event: {order['order_id']} | "
                f"{order['restaurant_id']} | ₹{order['amount']:,.2f} | "
                f"{order['order_status']}"
            )
            counter += 1
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nLive producer stopped.")

if __name__ == "__main__":
    main()

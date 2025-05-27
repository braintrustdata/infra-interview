import time
import random
from flask import Flask, jsonify, request
import datetime

# from datetime import timezone

app = Flask(__name__)
app.json.compact = False

# Hardcoded exchange rates (base: USD)
EXCHANGE_RATES = {
    "EUR": 0.89,
    "JPY": 155.00,
    "GBP": 0.78,
    "AUD": 1.47,
    "CAD": 1.36,
    "CHF": 0.91,
    "CNY": 7.20,
    "HKD": 7.80,
    "NZD": 1.58,
    "SEK": 10.50,
    "KRW": 1350.00,
    "SGD": 1.34,
}


def get_response_data():
    return {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "base_currency": "USD",
        "rates": EXCHANGE_RATES,
    }


@app.route("/rates", methods=["GET"])
def get_rates():
    # Simulate a slow response
    sleep_ms_str = request.args.get("sleep")
    if sleep_ms_str:
        try:
            sleep_ms = int(sleep_ms_str)
            if sleep_ms < 0:
                return (
                    jsonify(
                        {"error": "sleep parameter must be a non-negative integer"}
                    ),
                    400,
                )
            time.sleep(sleep_ms / 1000.0)  # Convert ms to seconds
        except ValueError:
            return jsonify({"error": "sleep parameter must be a valid integer"}), 400

    # Simulate 500 errors
    five_hundred_rate_str = request.args.get("500rate")
    if five_hundred_rate_str:
        try:
            five_hundred_rate = int(five_hundred_rate_str)
            if not (0 <= five_hundred_rate <= 100):
                return (
                    jsonify(
                        {
                            "error": "500rate parameter must be an integer between 0 and 100"
                        }
                    ),
                    400,
                )
            if random.randint(1, 100) <= five_hundred_rate:
                return jsonify({"error": "Internal Server Error (simulated)"}), 500
        except ValueError:
            return (
                jsonify({"error": "500rate parameter must be a valid integer"}),
                400,
            )

    return jsonify(get_response_data())


@app.route("/rates2", methods=["GET"])
def get_rates_v2():
    choice = random.choice(["error", "sleep", "normal"])

    if choice == "error":
        return jsonify({"error": "Internal Server Error (simulated)"}), 500
    elif choice == "sleep":
        time.sleep(5)

    return jsonify(get_response_data())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)

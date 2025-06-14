from flask import Flask, request, jsonify
import requests
import config
import jwt

app = Flask(__name__)

@app.route("/pay")
def pay():
    init_data = request.args.get("initData", "")
    try:
        # You should verify the JWT in production!
        payload = jwt.decode(init_data, options={"verify_signature": False})
    except Exception as e:
        return jsonify({"error": "Invalid initData"}), 400

    bundle_id = config.DEFAULT_BUNDLE_ID
    r = requests.get(
        f"https://api.stickerdom.store/api/v1/bundle/{bundle_id}/1",
        headers={"Authorization": f"Bearer {init_data}"}
    )

    if r.status_code != 200:
        return jsonify({"error": "Could not fetch bundle"}), 400

    bundle = r.json()
    recipient = bundle["payment"]["address"]
    amount = float(bundle["payment"]["amount"])
    ton_nano = int(amount * config.TON_DECIMALS)

    ton_link = (
        f"tonkeeper://send?recipient={recipient}&amount={ton_nano}&text=Buy%20Sticker%20Pack%20{bundle_id}"
    )

    return jsonify({"ton_link": ton_link})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

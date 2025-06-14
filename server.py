from flask import Flask, request, jsonify
import urllib.parse
import os

app = Flask(__name__)

TON_RECIPIENT = os.getenv("TON_RECIPIENT")

@app.route('/pay')
def pay():
    init_data = request.args.get('initData')
    if not init_data:
        return jsonify({"error": "Missing initData"}), 400
    if not TON_RECIPIENT:
        return jsonify({"error": "TON_RECIPIENT not configured"}), 500

    ton_link = f"tonkeeper://send?recipient={TON_RECIPIENT}&amount=1500000000&text=stickers-{urllib.parse.quote(init_data)}"
    return jsonify({"ton_link": ton_link})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

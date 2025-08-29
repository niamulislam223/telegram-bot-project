from flask import Flask, request, jsonify
import gspread
import os

app = Flask(__name__)

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_CREDS_JSON")
client = gspread.service_account_from_dict(eval(creds_json))
sheet = client.open("TelegramBotDB").sheet1

@app.route("/poll_results")
def poll_results():
    data = sheet.get_all_records()
    return jsonify(data)

@app.route("/send_message", methods=["POST"])
def send_message():
    user_id = request.json.get("user_id")
    text = request.json.get("text")
    # In real project, you would call Telegram API here
    return jsonify({"status": "sent", "user_id": user_id, "text": text})

if __name__ == "__main__":
    app.run()

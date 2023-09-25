from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route("/api/fetch_nfl_games", methods=["GET"])
def fetch_nfl_games_data():
    selected_date = request.args.get("date", default="", type=str)

    if not selected_date:
        return jsonify({"error": "Date parameter is missing."}), 400

    api_url = "https://api-american-football.p.rapidapi.com/games"
    headers = {
        "X-Rapidapi-Key": apiKey,
        "X-Rapidapi-Host": "api-american-football.p.rapidapi.com",
    }

    params = {"date": selected_date, "league": 1}

    try:
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return jsonify(data)
        else:
            return (
                jsonify(
                    {
                        "error": f"Failed to fetch NFL games data. Status Code: {response.status_code}"
                    }
                ),
                500,
            )
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

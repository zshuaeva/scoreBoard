import tkinter as tk
from tkcalendar import DateEntry
import requests
from tkinter.scrolledtext import ScrolledText


def fetch_nfl_games_data():
    selected_date = date_picker.get_date()
    api_url = ""
    headers = {
        "X-Rapidapi-Key": "",
        "X-Rapidapi-Host": "",
    }

    params = {"date": selected_date, "league": 1}

    try:
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            games_today = len(data["response"])  # Count of games for today
            games_today_label.config(text=f"Games today: {games_today}")

            game_info_text.delete("1.0", tk.END)

            for game in data["response"]:
                time = game["game"]["date"]["time"]
                home_team = game["teams"]["home"]["name"]
                away_team = game["teams"]["away"]["name"]

                game_info_text.insert(tk.END, f"Time (UTC): {time}\n")
                game_info_text.insert(tk.END, f"Home Team: {home_team}\n")
                game_info_text.insert(tk.END, f"Away Team: {away_team}\n")
                game_info_text.insert(tk.END, "\n")

        else:
            print(
                f"Failed to fetch NFL games data. Status Code: {response.status_code}"
            )
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("NFL Games Information")
root.geometry("400x400")

date_picker = DateEntry(root, width=12)
date_picker.pack()

games_today_label = tk.Label(root, text="Games today: 0")
games_today_label.pack()

game_info_text = ScrolledText(root, height=10, width=40)
game_info_text.pack(fill=tk.BOTH, expand=True)

fetch_button = tk.Button(
    root, text="Fetch NFL Games Data", command=fetch_nfl_games_data
)
fetch_button.pack()

root.mainloop()

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QDateEdit,
)
from PyQt5.QtCore import Qt, QDate
import requests


class NFLGamesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NFL Games Information")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)  # Enable calendar popup
        self.date_picker.setDate(QDate.currentDate())  # Set default date to today
        layout.addWidget(self.date_picker)

        self.games_info_text = QTextEdit()
        self.games_info_text.setReadOnly(True)
        layout.addWidget(self.games_info_text)

        fetch_button = QPushButton("Fetch NFL Games Data")
        fetch_button.clicked.connect(self.fetch_nfl_games_data)
        layout.addWidget(fetch_button)

    def fetch_nfl_games_data(self):
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")
        api_url = "https://api-american-football.p.rapidapi.com/games"
        headers = {
            "X-Rapidapi-Key": "API KEY",
            "X-Rapidapi-Host": "api-american-football.p.rapidapi.com",
        }

        params = {"date": selected_date, "league": 1}

        try:
            response = requests.get(api_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                games_today = len(data["response"])  # Count of games for today
                game_info = f"Date: {selected_date}\n"
                game_info += f"Games today: {games_today}\n\n"

                for game in data["response"]:
                    time = game["game"]["date"]["time"]
                    home_team = game["teams"]["home"]["name"]
                    away_team = game["teams"]["away"]["name"]

                    game_info += f"Time (UTC): {time}\n"
                    game_info += f"Home Team: {home_team}\n"
                    game_info += f"Away Team: {away_team}\n\n"

                self.games_info_text.setPlainText(game_info)

            else:
                print(
                    f"Failed to fetch NFL games data. Status Code: {response.status_code}"
                )
                print(response.text)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NFLGamesApp()
    window.show()
    sys.exit(app.exec_())

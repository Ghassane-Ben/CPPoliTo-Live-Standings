from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

CODEFORCES_API_URL = "https://codeforces.com/api/user.info?handles="

participants = ["paolofederico1", "salvini_god", "whiitex", "Petricore", "Nima_Naderi", "Homerus", "ilovelinux", "im_poli", "GiulioCosentino", "mrncreaz", "cancali", "Ghio", "FraBoni", "paoloAimar0705", "devastasi", "GiacAlex", "Haileoshu"]

@app.route('/')
def leaderboard():
    ratings = []
    try:
        response = requests.get(CODEFORCES_API_URL + ";".join(participants))
        data = response.json()
        if data["status"] == "OK":
            for user in data["result"]:
                ratings.append({
                    "name": user["handle"],
                    "rating": user["rating"]
                })
            ratings.sort(key=lambda x: x["rating"], reverse=True)
    except Exception as e:
        print(f"Error fetching ratings: {e}")

    current_date = datetime.now().strftime('%d/%m/%Y')
    
    return render_template('leaderboard.html', ratings=ratings, current_date=current_date)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

CODEFORCES_API_URL = "https://codeforces.com/api/user.info?handles="
CONTEST_HISTORY_URL = "https://codeforces.com/api/user.rating?handle="

participants = [
    "paolofederico1", "salvini_god", "whiitex", "Petricore", "Nima_Naderi", 
    "Homerus", "ilovelinux", "im_poli", "GiulioCosentino", "mrncreaz", "cancali", 
    "Ghio", "FraBoni", "paoloAimar0705", "devastasi", "GiacAlex", "Haileoshu", 
    "mikachelya", "Mugna0990", "musabkilic", "jack_03", "itsisma", "AbdelrahmanEhab1", 
    "Janaehab", "kyooz", "enigma.cpp"
]

# The date from which we want to start considering rating changes
CUT_OFF_DATE = datetime(2024, 12, 4)

@app.route('/')
def leaderboard():
    ratings = []
    try:
        # Fetch user information (like current rating)
        response = requests.get(CODEFORCES_API_URL + ";".join(participants))
        user_data = response.json()
        if user_data["status"] != "OK":
            return "Error fetching user data", 500
        
        # Now, fetch rating changes for each participant
        for user in user_data["result"]:
            handle = user["handle"]
            max_rating_after_cutoff = 0
            
            # Fetch the rating history of the user
            history_response = requests.get(CONTEST_HISTORY_URL + handle)
            history_data = history_response.json()
            if history_data["status"] != "OK":
                continue  # Skip if the history data is not fetched correctly
            
            # Iterate over the user's contest history
            for contest in history_data["result"]:
                contest_date = datetime.fromtimestamp(contest["startTimeSeconds"])
                if contest_date > CUT_OFF_DATE:
                    # Update max rating if this contest has a higher rating
                    max_rating_after_cutoff = max(max_rating_after_cutoff, contest["newRating"])
            
            # If no rating change was found after the cutoff date, assign rating 0
            ratings.append({
                "name": handle,
                "rating": max_rating_after_cutoff
            })
        
        # Sort by the max rating gained after the cutoff date (descending order)
        ratings.sort(key=lambda x: x["rating"], reverse=True)
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data", 500
    
    current_date = datetime.now().strftime('%d/%m/%Y')
    return render_template('leaderboard.html', ratings=ratings, current_date=current_date)

if __name__ == "__main__":
    app.run(debug=True)

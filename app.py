from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# API endpoints
CODEFORCES_API_URL = "https://codeforces.com/api/user.info?handles="
CONTEST_HISTORY_URL = "https://codeforces.com/api/user.rating?handle="

# Participants list
participants = [
    "paolofederico1", "salvini_god", "whiitex", "Petricore", "N.N_2004", 
    "im_poli", "GiulioCosentino", "itsisma", "kyooz", "enigma.cpp", "fakrulislam0085",
    "janaehab", "Kenpar", "SonicGT", "Calciferll", "krishanu8219", "ilovelinux",
    "Omino_95", "Toukennn", "GiacAlex", "luckyzio777", "airo.hub", "Luigi_05", 
    "Parishad", "Scampo", "EgeMorgul", "AliceAliceAlice_2001",
    "micheleCastellano", "iZ0R", "Ghassane"
]

# Define eligibility mapping (adjust as needed)
eligibility_map = {
    "salvini_god": "Ineligible",
    "Petricore": "Eligible",
    "whiitex": "Pending",
    "N.N_2004": "Eligible",
    "isma": "Eligible",
    "GiulioCosentino": "Eligible",
    "Ghassane": "Ineligible",
    "catgirl": "Eligible",
    "im_poli": "Eligible"
}

# The cutoff date (December 4, 2024)
CUT_OFF_DATE = datetime(2024, 12, 4)

def get_color_class(rating):
    if rating >= 3000:
        return "text-black"
    if rating >= 2600:
        return "text-red-900"
    if rating >= 2400:
        return "text-red-600"
    if rating >= 2300:
        return "text-orange-500"
    if rating >= 2100:
        return "text-orange-400"
    if rating >= 1900:
        return "text-purple-500"
    if rating >= 1600:
        return "text-blue-500"
    if rating >= 1400:
        return "text-cyan-500"
    if rating >= 1200:
        return "text-green-500"
    return "text-gray-500"

@app.route('/')
def leaderboard():
    ratings = []
    try:
        # Fetch user info for all participants
        response = requests.get(CODEFORCES_API_URL + ";".join(participants))
        user_data = response.json()
        if user_data["status"] != "OK":
            return "Error fetching user data", 500

        for user in user_data["result"]:
            handle = user["handle"]
            max_rating_after_cutoff = 0

            # Fetch contest history for each participant
            history_response = requests.get(CONTEST_HISTORY_URL + handle)
            history_data = history_response.json()
            if history_data["status"] != "OK":
                continue

            for contest in history_data["result"]:
                contest_date = datetime.fromtimestamp(contest["ratingUpdateTimeSeconds"])
                if contest_date > CUT_OFF_DATE:
                    max_rating_after_cutoff = max(max_rating_after_cutoff, contest["newRating"])

            ratings.append({
                "name": handle,
                "rating": max_rating_after_cutoff,
                "eligibility": eligibility_map.get(handle, "Eligible"),
                "color_class": get_color_class(max_rating_after_cutoff),
                "photo": user.get("titlePhoto", "https://sta.codeforces.com/s/74256/images/no-avatar.jpg")
            })

        # Sort by max rating (descending)
        ratings.sort(key=lambda x: x["rating"], reverse=True)

    except Exception as e:
        print("Error:", e)
        return "Error fetching data", 500

    current_date = datetime.now().strftime('%d/%m/%Y')
    return render_template('leaderboard.html', ratings=ratings, current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)

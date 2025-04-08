from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

participants = [
    "paolofederico1", "salvini_god", "whiitex", "Petricore", "N.N_2004", 
    "im_poli", "GiulioCosentino", "itsisma", "kyooz", "enigma.cpp", "fakrulislam0085",
    "janaehab", "Kenpar", "SonicGT", "Calciferll", "krishanu8219", "ilovelinux",
    "Omino_95", "Toukennn", "GiacAlex", "luckyzio777", "airo.hub", "Luigi_05", 
    "Parishad", "Scampo", "EgeMorgul", "AliceAliceAlice_2001",
    "micheleCastellano", "iZ0R", "Ghassane"
]

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

CUT_OFF_DATE = datetime(2024, 12, 4)
API_USER_INFO = "https://codeforces.com/api/user.info?handles="
API_USER_RATING = "https://codeforces.com/api/user.rating?handle="

def get_color_class(rating):
    if rating >= 3000: return "text-black"
    if rating >= 2600: return "text-red-900"
    if rating >= 2400: return "text-red-600"
    if rating >= 2300: return "text-orange-500"
    if rating >= 2100: return "text-orange-400"
    if rating >= 1900: return "text-purple-500"
    if rating >= 1600: return "text-blue-500"
    if rating >= 1400: return "text-cyan-500"
    if rating >= 1200: return "text-green-500"
    return "text-gray-500"

def get_badge_class(status):
    return {
        "Eligible": "bg-green-100 text-green-700",
        "Pending": "bg-yellow-100 text-yellow-700",
        "Ineligible": "bg-red-100 text-red-700"
    }.get(status, "bg-gray-100 text-gray-700")

@app.route('/')
def leaderboard():
    try:
        response = requests.get(API_USER_INFO + ";".join(participants))
        user_info = response.json()
        if user_info["status"] != "OK":
            return "Error fetching user info", 500

        result = []
        for user in user_info["result"]:
            handle = user["handle"]
            photo = user.get("titlePhoto", "")
            rating = 0

            history = requests.get(API_USER_RATING + handle).json()
            if history["status"] == "OK":
                for contest in history["result"]:
                    if "ratingUpdateTimeSeconds" in contest:
                        ts = datetime.fromtimestamp(contest["ratingUpdateTimeSeconds"])
                        if ts > CUT_OFF_DATE:
                            rating = max(rating, contest["newRating"])

            eligibility = eligibility_map.get(handle, "Eligible")
            result.append({
                "handle": handle,
                "photo": photo,
                "rating": rating,
                "eligibility": eligibility,
                "color": get_color_class(rating),
                "badge": get_badge_class(eligibility)
            })

        result.sort(key=lambda x: x["rating"], reverse=True)
        return render_template("leaderboard.html", ratings=result)

    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)

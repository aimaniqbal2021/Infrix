from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({"message": "TrailPulse API is live!"})


@app.route('/explore', methods=['POST'])
def explore():
    try:
        data = request.get_json()
        lat = float(data.get('lat'))
        lon = float(data.get('lon'))

        # Rule-based activity suggestion by latitude band
        if lat >= 60:
            activities = ['Dog Sledding', 'Aurora Watching', 'Ice Fishing', 'Snowshoeing', 'Glacier Hiking']
            terrain = 'Arctic Tundra'
            season = 'Polar Winter'
            difficulty = 'Extreme'
        elif lat >= 45:
            activities = ['Mountain Biking', 'Rock Climbing', 'Kayaking', 'Trail Running', 'Backcountry Skiing']
            terrain = 'Alpine Forest'
            season = 'Year-round'
            difficulty = 'Hard'
        elif lat >= 30:
            activities = ['Hiking', 'Paragliding', 'Canyon Rappelling', 'Mountain Trekking', 'Wildlife Safari']
            terrain = 'Temperate Highlands'
            season = 'Spring / Autumn'
            difficulty = 'Moderate'
        elif lat >= 10:
            activities = ['Jungle Trekking', 'White-water Rafting', 'Zip-lining', 'Scuba Diving', 'Surfing']
            terrain = 'Tropical Rainforest'
            season = 'Dry Season'
            difficulty = 'Moderate'
        else:
            activities = ['Desert Camping', 'Sandboarding', 'Camel Trekking', 'Stargazing', 'Dune Bashing']
            terrain = 'Arid Savanna'
            season = 'Winter Months'
            difficulty = 'Hard'

        return jsonify({
            "lat": lat,
            "lon": lon,
            "terrain": terrain,
            "season": season,
            "difficulty": difficulty,
            "activities": activities
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

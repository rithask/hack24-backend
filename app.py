from flask import Flask, request, jsonify, send_file
from distance import haversine_distance
from pymongo import MongoClient
from duckduckgo_search import DDGS
from textblob import TextBlob
import asyncio

MONGO_URI = "mongodb+srv://hack24:1lOvg0alxKgtQxF6@cluster0.efuv13d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.hack24
warehouses = db.warehouses

@app.route("/")
def home():
    return send_file("alen.jpg", mimetype="image/jpg")

@app.route("/warehouse", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        data = request.get_json()
        if "latitude" not in data or "longitude" not in data or "name" not in data:
            return jsonify({"error": "Latitude and Longitude are required"}), 400
        
        warehouses.insert_one(data)
        return "Warehouse added successfully"
    elif request.method == "GET":
        latitude = request.args.get("lat", '')
        longitude = request.args.get("long", '')
        all_warehouses = warehouses.find()
        distances = []
        for warehouse in all_warehouses:
            lat = warehouse["latitude"]
            lon = warehouse["longitude"]
            name = warehouse["name"]
            x = {}
            distance = haversine_distance(float(lat), float(lon), float(latitude), float(longitude))
            distances.append({"name": name, "distance": distance})
        # sort the distances
        distances.sort(key=lambda x: x["distance"])
        distances = jsonify(distances)
        distances.headers.add('Access-Control-Allow-Origin', '*')
        return distances
        # return f"Latitude: {lat}, Longitude: {lon}"


# port risk analysis

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def assess_risk(sentiment_score):
    if sentiment_score > 0.2:
        return "Low"
    elif sentiment_score > 0:
        return "Medium"
    else:
        return "High"

async def search_news(keywords, region="wt-wt", safesearch="off", timelimit="m", max_results=20):
    ddgs = DDGS()
    results = ddgs.news(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results
    )
    
    articles = []
    for result in results:
        articles.append(result)
    
    return articles

@app.route('/port', methods=['GET'])
def get_port_risk():
    port_name = request.args.get('name')
    if not port_name:
        return jsonify({"error": "port_name query parameter is required"}), 400
    
    keywords = f"port activities AND conflicts AND {port_name}"
    news_articles = asyncio.run(search_news(keywords))
    
    sentiment_scores = []
    for article in news_articles:
        description = article.get('snippet') or ""
        title = article.get('title') or ""
        content = title + " " + description

        sentiment_score = analyze_sentiment(content)
        sentiment_scores.append(sentiment_score)

    if sentiment_scores:
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
        risk_level = assess_risk(avg_sentiment_score)
    else:
        avg_sentiment_score = 0.0
        risk_level = "Unknown"

    response = {
        "port": port_name,
        "average_sentiment_score": avg_sentiment_score,
        "risk_level": risk_level
    }

    response = jsonify(response)

    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
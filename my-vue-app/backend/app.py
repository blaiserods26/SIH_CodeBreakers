from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store threat data globally
threat_data = []

def fetch_threat_data():
    url = "https://threatmap.fortiguard.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            threat_entries = soup.find_all('div', class_='threats-info')  # Example selector
            data = []
            for entry in threat_entries:
                location = entry.find('span', class_='location')
                severity = entry.find('span', class_='severity')
                if location and severity:
                    data.append({
                        'location': location.text.strip(),
                        'severity': severity.text.strip()
                    })
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Function to update global data periodically
def update_threat_data():
    global threat_data
    threat_data = fetch_threat_data()

# Schedule the scraper to run every 5 minutes (300 seconds)
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_threat_data, trigger="interval", seconds=300)
scheduler.start()

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({"stats": threat_data})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Start Flask server
    app.run(debug=True, port=5000)

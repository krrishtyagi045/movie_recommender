from flask import Flask, render_template, request, jsonify
import pandas as pd
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)


API_KEY = '09TOJfmxm9RweKrZV-CG9TF71QHOhzAXFrwntNsAfS_0'
SERVICE_URL = 'https://api.au-syd.assistant.watson.cloud.ibm.com/instances/31c1455a-4b7b-4a34-a597-439d06bc532bL'
ASSISTANT_ID = '54bfc5a8-69c8-4282-95de-c5e91b2e3e73'

authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(SERVICE_URL)
# -------------------------

movies = pd.read_csv("movies.csv")

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    language = request.form['language']
    
    filtered = movies[
        (movies['genre'].str.lower() == genre.lower()) & 
        (movies['language'].str.lower() == language.lower())
    ]
    
    if filtered.empty:
        result = ["No movies found"]
    else:
        result = filtered['title'].tolist()
        
    return render_template("result.html", movies=result)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        
        response = assistant.message_stateless(
            assistant_id=ASSISTANT_ID,
            input={'text': user_message}
        ).get_result()
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
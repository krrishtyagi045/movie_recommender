from flask import Flask, render_template, request, jsonify
import pandas as pd
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# IBM Watson Configuration (now hidden)
API_KEY = os.getenv('IBM_API_KEY')
SERVICE_URL = os.getenv('IBM_SERVICE_URL')
ASSISTANT_ID = os.getenv('IBM_ASSISTANT_ID')

authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(SERVICE_URL)

# Load Movies Dataset
movies = pd.read_csv("movies.csv")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    language = request.form['language']

    filtered = movies[
        (movies['genre'].str.strip().str.lower() == genre.strip().lower()) &
        (movies['language'].str.strip().str.lower() == language.strip().lower())
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
            input={
                'message_type': 'text',
                'text': user_message
            }
        ).get_result()

        bot_reply = response['output']['generic'][0]['text']
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
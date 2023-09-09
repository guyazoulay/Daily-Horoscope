import random
from datetime import datetime

import requests as requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__, template_folder='templates')

users = []
astro_sign_url = {"Gemini": "https://www.elle.com/horoscopes/daily/a99/gemini-daily-horoscope/",
 "Taurus" : "https://www.elle.com/horoscopes/daily/a98/taurus-daily-horoscope/",
 "Aries" : "https://www.elle.com/horoscopes/daily/a60/aries-daily-horoscope/",
 "Pisces" : "https://www.elle.com/horoscopes/daily/a108/pisces-daily-horoscope/",
 "Aquarius" : "https://www.elle.com/horoscopes/daily/a107/aquarius-daily-horoscope/",
 "Libra" : "https://www.elle.com/horoscopes/daily/a103/libra-daily-horoscope/",
 "Capricorn" : "https://www.elle.com/horoscopes/daily/a106/capricorn-daily-horoscope/",
 "Virgo" : "https://www.elle.com/horoscopes/daily/a102/virgo-daily-horoscope/",
 "Sagittarius" : "https://www.elle.com/horoscopes/daily/a105/sagittarius-daily-horoscope/",
 "Leo" : "https://www.elle.com/horoscopes/daily/a101/leo-daily-horoscope/",
 "Scorpio" : "https://www.elle.com/horoscopes/daily/a104/scorpio-daily-horoscope/",
 "Cancer" : "https://www.elle.com/horoscopes/daily/a100/cancer-daily-horoscope/"}
happy_sentences = [
    "Happiness is a choice, make it yours every day.",
    "Smile and the world smiles with you.",
    "Life is better when you're laughing.",
    "Find joy in the ordinary.",
    "Count your blessings and spread positivity."
]

sad_sentences = [
    "It's okay not to be okay sometimes.",
    "Tears are the words the heart can't express.",
    "Rainy days can't last forever.",
    "Embrace the pain; it will make you stronger.",
    "Tomorrow is a new day with a fresh start."
]

excited_sentences = [
    "Embrace the excitement of the unknown.",
    "Good things come to those who chase their dreams.",
    "Every day is a new adventure waiting to happen.",
    "Feel the adrenaline and let it drive you forward.",
    "Your enthusiasm is contagious; spread it around."
]

exhausted_sentences = [
    "Rest when you're weary; you deserve it.",
    "Take a break, recharge, and come back stronger.",
    "Exhaustion is a sign of hard work and dedication.",
    "You can't pour from an empty cup, so take care of yourself.",
    "Recovery is just as important as the work itself."
]

fear_sentences = [
    "Courage is not the absence of fear but the triumph over it.",
    "Face your fears; they will lose their power over you.",
    "Fear is a natural response to the unknown; embrace it.",
    "Don't let fear hold you back from your potential.",
    "The only thing to fear is fear itself."
]

@app.route('/')
def home():
    return 'Hello, World!.'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']

        # Store user data (you'll replace this with database storage)
        user_data = { 'username': username, 'dob': dob, 'password': password }
        users.append(user_data)
        # Redirect to a success page or user dashboard
        return redirect(url_for('login', dob=dob))


    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the login form
        username = request.form['username']
        password = request.form['password']
        selected_emotion = request.form['emotion']

        # Check if the user exists and the password matches (you'll replace this with database checks)

        for user_data in users:
            if user_data['username'] == username and user_data['password'] == password:
                dob = user_data['dob']
                user_data_json = json.dumps(user_data)

                return redirect(url_for('dashboard', user_data=user_data_json, emotion=selected_emotion, dob=dob))

        # If login fails, show an error message
    error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    user_data = request.args.get('user_data')
    selected_emotion = request.args.get('emotion')
    dob = request.args.get('dob')
    user_data_dict = json.loads(user_data)
    astrological_sign = calculate_astrological_sign(dob)
    astro_url = astro_sign_url[astrological_sign]
    horoscope = scrape_horoscope(astro_url)
    if selected_emotion == 'Happy':
        selected_sentence = random.choice(happy_sentences)
    elif selected_emotion == 'Sad':
        selected_sentence = random.choice(sad_sentences)
    elif selected_emotion == 'Excited':
        selected_sentence = random.choice(excited_sentences)
    elif selected_emotion == 'Exhausted':
        selected_sentence = random.choice(exhausted_sentences)
    elif selected_emotion == 'Fear':
        selected_sentence = random.choice(fear_sentences)
    else:
        selected_sentence = "No specific sentence for this emotion."

    return render_template('dashboard.html', user_data=user_data_dict, emotion=selected_emotion, astrological_sign=astrological_sign,horoscope=horoscope, selected_sentence=selected_sentence)


def calculate_astrological_sign(dob):
    # Convert DOB string to a datetime object
    print(dob)
    dob_date = datetime.strptime(dob, '%Y-%m-%d')

    # Define the date ranges for each astrological sign (customize as needed)
    astrological_signs = {
        'Aries': (datetime(dob_date.year, 3, 21), datetime(dob_date.year, 4, 19)),
        'Taurus': (datetime(dob_date.year, 4, 20), datetime(dob_date.year, 5, 20)),
        'Gemini': (datetime(dob_date.year, 5, 21), datetime(dob_date.year, 6, 20)),
        'Cancer': (datetime(dob_date.year, 6, 21), datetime(dob_date.year, 7, 22)),
        'Leo': (datetime(dob_date.year, 7, 23), datetime(dob_date.year, 8, 22)),
        'Virgo': (datetime(dob_date.year, 8, 23), datetime(dob_date.year, 9, 22)),
        'Libra': (datetime(dob_date.year, 9, 23), datetime(dob_date.year, 10, 22)),
        'Scorpio': (datetime(dob_date.year, 10, 23), datetime(dob_date.year, 11, 21)),
        'Sagittarius': (datetime(dob_date.year, 11, 22), datetime(dob_date.year, 12, 21)),
        'Capricorn': (datetime(dob_date.year, 12, 22), datetime(dob_date.year, 12, 31)) or (datetime(dob_date.year, 1, 1), datetime(dob_date.year, 1, 19)),
        'Aquarius': (datetime(dob_date.year, 1, 20), datetime(dob_date.year, 2, 18)),
        'Pisces': (datetime(dob_date.year, 2, 19), datetime(dob_date.year, 3, 20))
    }
    for sign, (start_date, end_date) in astrological_signs.items():
        if start_date <= dob_date <= end_date:
            return sign

    return 'Unknown'

def scrape_horoscope(url):
    # Send a GET request to the URL to retrieve the HTML content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <p> element with the specified data-node-id attribute
        horoscope_element = soup.find('p', {'data-node-id': '3'})

        if horoscope_element:
            # Extract the text from the element
            horoscope_text = horoscope_element.get_text()
            return horoscope_text.strip()  # Remove leading/trailing whitespace

    # If the page or element is not found, return None or an appropriate error message
    return "Horoscope not available."


if __name__ == '__main__':
    app.run()

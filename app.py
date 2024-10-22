from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Ensure the API key is set correctly
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY environment variable not set")

genai.configure(api_key=api_key)

# Create a model instance
model = genai.GenerativeModel("gemini-1.5-flash")

def get_unsplash_image(query="iot"):
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    if not UNSPLASH_ACCESS_KEY:
        print("Unsplash Access Key not found")
        return "https://source.unsplash.com/1600x900/?iot"  # Fallback to random Unsplash image
    
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['urls']['regular']  # Get the regular size URL of the image
    else:
        print(f"Failed to get image from Unsplash: {response.status_code}, {response.text}")
        return "https://source.unsplash.com/1600x900/?iot"  # Fallback to random Unsplash image


def generate_content_with_image(prompt, language):
    image_url = get_unsplash_image()
    
    if not image_url:
        image_url = "https://source.unsplash.com/1600x900/?iot"  # Fallback in case of None
    
    detailed_prompt = f"""
    Generate HTML content in {language} that is visually structured like a blog post or whitepaper.
    Requirements:
    1. A title header with "BLOGBEITRAG" or "WHITEPAPER".
    2. A subtitle for the article.
    3. Use this dynamic image: <img src="{image_url}" alt="IoT Image">
    4. Main content section with paragraphs.
    5. Sections with key points or bullet points.
    6. A footer with a call-to-action.
    7. Ensure that the content is structured and formatted in a way similar to a corporate blog post or whitepaper.
    Content Topic: {prompt}
    """
    
    response = model.generate_content(detailed_prompt)
    return response.text.strip()

def embed_references(content, links):
    for keyword, link in links.items():
        content = content.replace(keyword, f'<a href="{link}" target="_blank">{keyword}</a>')
    return content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt', '').strip() # Get and trim whitespace
    language = request.form['language']

    if not prompt:
        return jsonify({'content': 'No content generated. Please enter a valid prompt.'})

    content = generate_content_with_image(prompt, language)
    
    links = {
        "IoT innovations": "https://iot.telekom.com/en/the-world-of-tracking",
        "smart cities": "https://iot.telekom.com/en/digitized-workplace"
    }
    
    referenced_content = embed_references(content, links)
    return jsonify({'content': referenced_content})

if __name__ == '__main__':
    app.run(debug=True)
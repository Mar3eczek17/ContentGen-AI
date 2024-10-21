from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Ensure the API key is set correctly
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY environment variable not set")

genai.configure(api_key=api_key)

# Create a model instance
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_content(prompt, language):
    detailed_prompt = f"""
    Generate HTML content in {language} that is visually structured like a blog post or whitepaper.
    Requirements:
    1. A title header with "BLOGBEITRAG" or "WHITEPAPER".
    2. A subtitle for the article.
    3. An image placeholder. Use the image <img src='/static/placeholder.jpeg' alt='Placeholder Image'>.
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

    content = generate_content(prompt, language)
    
    links = {
        "IoT innovations": "https://iot.telekom.com/en/the-world-of-tracking",
        "smart cities": "https://iot.telekom.com/en/digitized-workplace"
    }
    
    referenced_content = embed_references(content, links)
    return jsonify({'content': referenced_content})

if __name__ == '__main__':
    app.run(debug=True)

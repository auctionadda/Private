from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the web scraping API service"})

@app.route("/scrape", methods=['GET'])
def scrape_for_prefix():
    # Get the prefix from the query parameters
    prefix = request.args.get('prefix')

    try:
        # Send a GET request to fetch the raw HTML content from the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch the webpage. Status code: {response.status_code}"}), 400

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <h4> tag that contains the given prefix (case-insensitive search)
        h4_element = soup.find('h4', string=lambda text: text and prefix.lower() in text.lower())

        if h4_element:
            # Once the <h4> is found, get the next sibling <span>
            span_element = h4_element.find_next_sibling('span')

            if span_element:
                # Extract the text from the <span> tag
                span_value = span_element.text
                return jsonify({"prefix": prefix, "extracted_value": span_value})
            else:
                return jsonify({"error": "Couldn't find the sibling <span> tag."}), 404
        else:
            return jsonify({"error": f"Couldn't find the <h4> tagg with the prefix '{prefix}'."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

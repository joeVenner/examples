from flask import Flask, jsonify, request
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

def getData(params):
    url = f'https://news.google.com/rss/search?q={params}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)
    news_articles = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        description_html = item.find('description').text
        soup = BeautifulSoup(html.unescape(description_html), 'html.parser')
        description_text = soup.get_text()
        source = item.find('source').text
        news_articles.append({'Title': title, 'Link': link, 'Publication Date': pubDate, 'Description': description_text, 'Source': source})

    return news_articles

@app.route('/')
def documentation():
    return """
    <h2>Google News API Documentation</h2>
    <p>Use this API to fetch news articles based on a search query.</p>
    <h3>Endpoints</h3>
    <ul>
        <li><strong>/news</strong>: Fetch news articles.</li>
    </ul>
    <h3>Usage</h3>
    <p>To fetch news articles, make a GET request to the <code>/news</code> endpoint with a <code>q</code> query parameter specifying your search term. For example:</p>
    <code>GET /news?q=policycenter</code>
    <h3>Response Format</h3>
    <p>The response will be a JSON array of articles, with each article containing:</p>
    <ul>
        <li>Title</li>
        <li>Link</li>
        <li>Publication Date</li>
        <li>Description</li>
        <li>Source</li>
    </ul>
    """

@app.route('/news', methods=['GET'])
def get_news():
    params = request.args.get('q', '')  # Get the search query parameter from the URL
    if not params:
        return jsonify({'error': 'Missing query parameter "q"'}), 400
    data = getData(params)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for 
import requests 
import time 
from googletrans import Translator 
from textblob import TextBlob 
 
app = Flask(_name_) 
 
# Replace with your actual NewsAPI key 
api_key = '24be048e36114998a46000c06c02d10a' 
news_api_url = 'https://newsapi.org/v2/everything' 
trending_news_url = 'https://newsapi.org/v2/top-headlines' 
 
# Initialize the translator 
translator = Translator() 
 
def analyze_sentiment(text): 
    """Analyze sentiment using TextBlob on English text.""" 
    analysis = TextBlob(text) 
    if analysis.sentiment.polarity > 0.1: 
        return 'Positive' 
    elif analysis.sentiment.polarity < -0.1: 
        return 'Negative' 
    else: 
        return 'Neutral' 
 
def translate_text(text, dest_language): 
    """Translate text to the desired language.""" 
    if not text: 
        return "No content available" 
    try: 
        translated = translator.translate(text, dest=dest_language) 
        return translated.text 
    except Exception as e: 
        print(f"Translation error: {e}") 
        return text  # Fallback to original if translation fails 
 
def fetch_with_retries(url, params, max_retries=3, delay=5): 
    """Fetch data with retries to handle API rate limits.""" 
    for attempt in range(max_retries): 
        try: 
            response = requests.get(url, params=params) 
            response.raise_for_status() 
            articles = response.json().get('articles', []) 
            # Filter out unwanted articles 
            available_articles = [
  article for article in articles 
                if article.get('title') and article.get('description') and article.get('url') and  
                article['title'] != '[Removed]' and article['description'] != '[Removed]' 
            ] 
            return available_articles 
        except requests.exceptions.RequestException as e: 
            print(f"Request error on attempt {attempt + 1}: {e}") 
            if attempt < max_retries - 1: 
                print(f"Retrying in {delay} seconds...") 
                time.sleep(delay) 
    return [] 
 
@app.route('/') 
def home(): 
    return render_template('start.html') 
 
@app.route('/index') 
def index(): 
    """Render the home page with trending articles in the default language.""" 
    language = request.args.get('language', 'en') 
    trending_articles = get_translated_trending_articles(language) 
     
    # Debugging: Print articles being passed to template 
    print("Trending Articles for index route:", trending_articles) 
     
    return render_template('index.html', trending_articles=trending_articles, 
selected_language=language) 
 
@app.route('/search', methods=['POST']) 
def search(): 
    """Search for articles based on keyword, then translate and classify by sentiment.""" 
    user_language = request.form.get('language', 'en') 
    keyword = request.form.get('keyword', '') 
    page_size = int(request.form.get('pageSize', 15)) 
    target_per_sentiment = max(1, page_size // 3) 
 
    params = { 
        'apiKey': api_key, 
        'q': keyword, 
        'pageSize': page_size * 2, 
        'language': 'en' 
    } 
 
    articles = fetch_with_retries(news_api_url, params) 
 
    classified_articles = {'Positive': [], 'Neutral': [], 'Negative': []} 
 
    for article in articles: 
        if all(len(classified_articles[sentiment]) >= target_per_sentiment for sentiment in 
classified_articles): 


    break 
 
        title = article['title'] 
        description = article['description'] 
        url = article['url'] 
        image_url = article.get('urlToImage', '') 
 
        full_text = f"{title} {description}" 
        sentiment = analyze_sentiment(full_text) 
 
        translated_title = translate_text(title, user_language) if user_language != 'en' else title 
        translated_description = translate_text(description, user_language) if user_language != 
'en' else description 
 
        if len(classified_articles[sentiment]) < target_per_sentiment: 
            classified_articles[sentiment].append({ 
                'title': translated_title, 
                'description': translated_description, 
                'url': url, 
                'imageUrl': image_url 
            }) 
 
    return render_template('results.html', articles=classified_articles, 
language=user_language) 
 
def get_translated_trending_articles(language): 
    """Fetch trending articles and translate if necessary.""" 
    params = { 
        'apiKey': api_key, 
        'country': 'us', 
        'pageSize': 10 
    } 
    trending_articles = fetch_with_retries(trending_news_url, params) 
     
    # Debugging: Print fetched articles 
    print("Trending articles fetched:", trending_articles) 
 
    if language != 'en': 
        for article in trending_articles: 
            article['title'] = translate_text(article['title'], language) 
            article['description'] = translate_text(article['description'], language) 
     
    # Debugging: Print translated articles 
    print("Trending articles after translation (if applied):", trending_articles) 
     
    return trending_articles 
 
 
 
@app.route('/trending') 
def trending(): 
    """Fetch and return trending news articles in the selected language.""" 
    language = request.args.get('language', 'en') 
    trending_articles = get_translated_trending_articles(language) 
    return jsonify(trending_articles) 
 
if _name_ == '_main_': 
    app.run(debug=True) 
# 📰 AI-Based News Translator

An intelligent web-based news translator that fetches the latest news articles using the NewsAPI, analyzes sentiment with TextBlob, and translates the content into multiple languages using Google Translator. This project provides an accessible and multilingual news-reading experience for users across the globe.

## 🌐 Features

- 🔍 **Search News**: Fetches news articles based on user input.
- 🌍 **Multilingual Translation**: Translates news headlines and content into selected languages.
- 📈 **Sentiment Analysis**: Detects and displays the tone of the news (Positive, Neutral, Negative).
- 🗣️ **Text-to-Speech**: Option to listen to translated news (if included).
- 📢 **Trending News Section**: Displays top 3 trending articles with images and headlines.

## 🛠️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **APIs & Libraries**:
  - [NewsAPI](https://newsapi.org/) – Fetch latest and trending news
  - [TextBlob](https://textblob.readthedocs.io/en/dev/) – Sentiment analysis
  - [Googletrans](https://py-googletrans.readthedocs.io/en/latest/) – Language translation (Google Translate unofficial API)

### Prerequisites

- Python 3.x
- Flask
- newsapi-python
- textblob
- googletrans==4.0.0-rc1

### Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/news-translator.git
   cd news-translator
install 
pip install -r requirements.txt
news-translator/
│
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   └── results.html
├── app.py
├── README.md
└── requirements.txt
📌 Future Improvements
Add support for summarizing long news articles.

Improve translation quality with official Google Translate API.

Add user preferences and news history.

Support for news categories (Sports, Tech, Health, etc.).

🤝 Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.

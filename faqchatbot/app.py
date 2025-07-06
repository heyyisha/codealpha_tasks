
from flask import Flask, render_template, request, jsonify
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
app = Flask(__name__)
# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# Load the FAQs
with open('faqs.json', 'r') as f:
    faqs = json.load(f)
# Initialize NLTK objects
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
# Preprocess text: lowercase, remove stopwords and punctuation, lemmatize
def preprocess(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)
# Preprocess all questions
questions = [q['question'] for q in faqs]
processed_questions = [preprocess(q) for q in questions]
# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(processed_questions)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json['question']
    
    # Preprocess the user's question
    processed_user_question = preprocess(user_question)
    user_vector = vectorizer.transform([processed_user_question])
    
    # Calculate cosine similarity between user question and FAQs
    similarities = cosine_similarity(user_vector, question_vectors)
    best_match_index = similarities.argmax()
    best_match_score = similarities[0, best_match_index]
    
    # Only return a match if the similarity score is above a threshold
    if best_match_score > 0.3:  # Adjust this threshold as needed
        best_answer = faqs[best_match_index]['answer']
        return jsonify({'answer': best_answer})
    else:
        return jsonify({'answer': "Sorry, I don't understand that question. Please try rephrasing or ask another question about Python."})
if __name__ == '__main__':
    app.run(debug=True)

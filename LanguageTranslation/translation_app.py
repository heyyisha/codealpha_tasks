from translate import Translator
from flask import Flask, render_template, request, jsonify
import pyperclip
import pyttsx3
import threading

app = Flask(__name__)

# Language dictionary
language_dict = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic', 'az': 'Azerbaijani',
    'eu': 'Basque', 'bn': 'Bengali', 'be': 'Belarusian', 'bg': 'Bulgarian',
    'ca': 'Catalan', 'zh': 'Chinese', 'hr': 'Croatian', 'cs': 'Czech',
    'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto',
    'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French',
    'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
    'gu': 'Gujarati', 'ht': 'Haitian Creole', 'he': 'Hebrew', 'hi': 'Hindi',
    'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian', 'ga': 'Irish',
    'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada', 'ko': 'Korean',
    'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'mk': 'Macedonian',
    'ms': 'Malay', 'mt': 'Maltese', 'no': 'Norwegian', 'fa': 'Persian',
    'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian',
    'sr': 'Serbian', 'sk': 'Slovak', 'sl': 'Slovenian', 'es': 'Spanish',
    'sw': 'Swahili', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'vi': 'Vietnamese', 'cy': 'Welsh', 'yi': 'Yiddish'
}

@app.route('/')
def index():
    return render_template('index.html', languages=language_dict)

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data['text']
        dest_lang = data['dest_lang']
        
        if not text.strip():
            return jsonify({'error': 'Please enter text to translate'})
        
        translator = Translator(to_lang=dest_lang)
        translation = translator.translate(text)
        
        return jsonify({
            'translated_text': translation,
            'dest_lang_full': language_dict.get(dest_lang, dest_lang)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/copy', methods=['POST'])
def copy_text():
    data = request.get_json()
    text = data['text']
    pyperclip.copy(text)
    return jsonify({'status': 'Text copied to clipboard!'})

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data['text']
    lang = data['lang']
    
    def speak():
        engine = pyttsx3.init()
        
        # Try to set voice for the target language (works best on Windows)
        try:
            voices = engine.getProperty('voices')
            for voice in voices:
                if lang in voice.languages[0].lower():
                    engine.setProperty('voice', voice.id)
                    break
        except:
            pass
        
        engine.say(text)
        engine.runAndWait()
    
    # Run speech in a separate thread to avoid blocking
    thread = threading.Thread(target=speak)
    thread.start()
    
    return jsonify({'status': 'Speaking...'})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, send_file
from googletrans import Translator
from gtts import gTTS
import os
import threading
from io import BytesIO

app = Flask(__name__)

def translate_text(text, target_lang):
    """
    Translate text to the target language.

    Parameters:
        text (str): The text to be translated.
        target_lang (str): The target language code.

    Returns:
        str: Translated text.
    """
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

def text_to_speech(text, lang):
    """
    Convert text to speech in a specified language and save it as an audio file.

    Parameters:
        text (str): The text to be converted to speech.
        lang (str): Language code.

    Returns:
        str: Path to the saved audio file.
    """
    tts = gTTS(text, lang=lang)
    folder_path = "converted_audio_files"
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
    filename = os.path.join(folder_path, "output_audio.mp3")
    tts.save(filename)
    return filename

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech_api():
    """
    API endpoint to convert text to speech.
    Expects JSON input with the text and target language.
    Returns the generated audio file.
    """
    data = request.json
    if 'text' not in data or 'target_lang' not in data:
        return jsonify({'error': 'Text or target language field is missing'}), 400

    input_text = data['text']
    target_lang = data['target_lang']

    # Translate input text to the target language
    translated_text = translate_text(input_text, target_lang)
    
    # Generate the audio file
    audio_file = text_to_speech(translated_text, target_lang)
    
    # Send the audio file as the response
    return send_file(audio_file, mimetype='audio/mpeg')

def run_flask():
    app.run(host='0.0.0.0', port=6969, debug=False)

if __name__ == "__main__":
    thread = threading.Thread(target=run_flask)
    thread.start()

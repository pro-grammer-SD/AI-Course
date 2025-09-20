import os
import tempfile
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
from io import BytesIO
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from deep_translator import GoogleTranslator
from unidecode import unidecode

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)
EVE_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

def speak(text):
    text = unidecode(text)
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=EVE_VOICE_ID,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    play(audio)

def record_audio(duration=5, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp_file.name, recording, fs)
    return tmp_file.name

def translate_and_speak(audio_file_path, target_lang="es"):
    with open(audio_file_path, "rb") as f:
        audio_data = BytesIO(f.read())
    transcription = elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",
        language_code="eng",
        diarize=False
    )
    text = transcription.text
    if not text:
        return
    print(f"🧑 You said: {text}")
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    print(f"🤖 Translated: {translated}")
    speak(translated)

def main():
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    print("Supported language codes:")
    for code, name in langs.items():
        print(f"{code} → {name}")
    target_lang = input("Enter target language code: ").strip()
    while True:
        audio_file = record_audio(duration=5)
        translate_and_speak(audio_file, target_lang)
        again = input("Translate another? (y/n): ").strip().lower()
        if again != "y":
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
    
"""
Speech-to-Text Audio Recorder with Waveform Visualization

This script demonstrates AI transmission systems by:
1. Recording live audio from microphone
2. Converting analog speech to digital data
3. Visualizing the audio waveform
4. Using Google Speech Recognition API for transcription
5. Saving both audio and text outputs

Required libraries:
pip install SpeechRecognition pyaudio numpy matplotlib

For macOS users, also run:
brew install portaudio
"""

import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData
import os

# Global event to coordinate stopping the recording
stop_event = threading.Event()

def wait_for_enter():
    """
    Waits for user to press Enter to stop recording.
    This runs in a separate thread so recording can continue.
    """
    input("\nPress Enter to stop recording...\n")
    stop_event.set()

def spinner():
    """
    Shows an animated spinner in the terminal while recording.
    Provides visual feedback that the system is actively listening.
    """
    spinner_chars = '|/-\\'
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\rRecording... {spinner_chars[idx % len(spinner_chars)]} ')
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write('\rRecording stopped.          \n')
    sys.stdout.flush()

def record_until_enter():
    """
    Records audio from the microphone until Enter is pressed.
    
    Audio Settings:
    - Format: 16-bit PCM (standard for speech recognition)
    - Channels: 1 (mono)
    - Sample Rate: 16kHz (optimal for speech APIs)
    - Buffer: 1024 frames per read
    
    Returns:
        tuple: (audio_data_bytes, sample_rate, sample_width)
    """
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Audio configuration
    format = pyaudio.paInt16  # 16-bit samples
    channels = 1              # Mono audio
    rate = 16000             # 16kHz sample rate (speech recognition standard)
    frames_per_buffer = 1024 # Buffer size
    
    # Open audio stream
    try:
        stream = p.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=frames_per_buffer
        )
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        print("Make sure your microphone is connected and accessible.")
        p.terminate()
        return None, None, None
    
    frames = []
    
    # Start background threads for user interaction
    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()
    
    # Record audio until Enter is pressed
    print("🎤 Recording started...")
    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print(f"Error reading audio stream: {e}")
            break
    
    # Clean up audio resources
    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(format)
    p.terminate()
    
    # Combine all audio frames into single byte string
    audio_data = b''.join(frames)
    
    print(f"✅ Recorded {len(audio_data)} bytes of audio data")
    return audio_data, rate, sample_width

def save_audio(data, rate, width, filename="recorded_audio.wav"):
    """
    Saves raw audio data to a WAV file.
    
    Args:
        data (bytes): Raw audio data
        rate (int): Sample rate (samples per second)
        width (int): Sample width in bytes
        filename (str): Output filename
    """
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)      # Mono
            wf.setsampwidth(width)  # Sample width in bytes
            wf.setframerate(rate)   # Sample rate
            wf.writeframes(data)    # Write audio data
        
        file_size = os.path.getsize(filename)
        print(f"💾 Audio saved: {filename} ({file_size} bytes)")
        return True
    except Exception as e:
        print(f"❌ Error saving audio: {e}")
        return False

def transcribe_audio(data, rate, width, filename="transcription.txt"):
    """
    Transcribes audio data using Google Speech Recognition API.
    
    Args:
        data (bytes): Raw audio data
        rate (int): Sample rate
        width (int): Sample width in bytes  
        filename (str): Output text filename
    
    Returns:
        str: Transcribed text
    """
    print("🤖 Transcribing audio...")
    
    # Initialize speech recognizer
    r = sr.Recognizer()
    
    # Create AudioData object for the API
    audio = AudioData(data, rate, width)
    
    try:
        # Send to Google Speech Recognition API
        text = r.recognize_google(audio)
        print(f"📝 Transcription: '{text}'")
        
        # Save transcription to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"💾 Transcription saved: {filename}")
        
        return text
        
    except sr.UnknownValueError:
        error_msg = "Could not understand the audio. Try speaking more clearly."
        print(f"❌ {error_msg}")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ERROR] {error_msg}")
        
        return error_msg
        
    except sr.RequestError as e:
        error_msg = f"API Error: {e}. Check your internet connection."
        print(f"❌ {error_msg}")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[ERROR] {error_msg}")
        
        return error_msg

def show_waveform(data, rate):
    """
    Visualizes the audio waveform using matplotlib.
    
    This shows how analog speech becomes digital data that AI can process.
    
    Args:
        data (bytes): Raw audio data
        rate (int): Sample rate
    """
    print("📊 Generating waveform visualization...")
    
    try:
        # Convert byte data to numpy array of 16-bit integers
        samples = np.frombuffer(data, dtype=np.int16)
        
        # Create time axis (x-axis) in seconds
        duration = len(samples) / rate
        time_axis = np.linspace(0, duration, num=len(samples))
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(time_axis, samples, linewidth=0.5, color='blue')
        
        # Formatting
        plt.title(f"Audio Waveform - Duration: {duration:.2f} seconds", fontsize=14)
        plt.xlabel("Time (seconds)", fontsize=12)
        plt.ylabel("Amplitude", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Add some statistics as text
        max_amplitude = np.max(np.abs(samples))
        avg_amplitude = np.mean(np.abs(samples))
        
        plt.text(0.02, 0.98, f'Max Amplitude: {max_amplitude}\nAvg Amplitude: {avg_amplitude:.0f}\nSample Rate: {rate} Hz',
                transform=plt.gca().transAxes, 
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        print("📈 Displaying waveform...")
        plt.show()
        
    except Exception as e:
        print(f"❌ Error creating waveform: {e}")

def check_dependencies():
    """
    Checks if all required dependencies are available.
    """
    missing_deps = []
    
    try:
        import pyaudio
    except ImportError:
        missing_deps.append("pyaudio")
    
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("SpeechRecognition")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with: pip install " + " ".join(missing_deps))
        return False
    
    return True

def print_intro():
    """
    Prints introduction and instructions.
    """
    print("=" * 60)
    print("🎤 SPEECH-TO-TEXT AI DEMONSTRATION")
    print("=" * 60)
    print()
    print("This program demonstrates AI transmission systems:")
    print("1. 🎵 Captures analog voice signals from your microphone")
    print("2. 📊 Converts them to digital data (16kHz, 16-bit)")
    print("3. 📈 Visualizes the waveform to show voice as data")
    print("4. 🤖 Uses Google's AI to transcribe speech to text")
    print("5. 💾 Saves both audio file and transcription")
    print()
    print("This shows how AI systems 'hear' and process human speech!")
    print()

def main():
    """
    Main function that orchestrates the entire speech-to-text pipeline.
    """
    print_intro()
    
    # Check if all dependencies are installed
    if not check_dependencies():
        return
    
    # Reset the stop event in case of multiple runs
    stop_event.clear()
    
    print("🚀 Starting speech recording...")
    print("💡 Tip: Speak clearly and avoid background noise for best results")
    
    # Step 1: Record audio from microphone
    audio_data, rate, width = record_until_enter()
    
    if audio_data is None:
        print("❌ Failed to record audio. Exiting.")
        return
    
    if len(audio_data) == 0:
        print("❌ No audio data recorded. Please try again.")
        return
    
    print()
    print("🔄 Processing your recording...")
    print()
    
    # Step 2: Save audio to file
    if not save_audio(audio_data, rate, width):
        print("⚠️ Could not save audio file, but continuing with transcription...")
    
    # Step 3: Transcribe using Google Speech Recognition
    transcription = transcribe_audio(audio_data, rate, width)
    
    # Step 4: Show waveform visualization
    show_waveform(audio_data, rate)
    
    print()
    print("=" * 60)
    print("✅ PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"📝 Your speech: '{transcription}'")
    print("📁 Files created:")
    print("   - recorded_audio.wav (your voice recording)")
    print("   - transcription.txt (speech-to-text result)")
    print()
    print("🎓 You've successfully demonstrated how AI processes human voice!")

if __name__ == "__main__":
    main()
    
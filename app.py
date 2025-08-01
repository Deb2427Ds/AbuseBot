from transformers import pipeline
import sounddevice as sd
import scipy.io.wavfile as wav

# Record 5 sec audio
def record_audio(filename="temp.wav"):
    fs = 16000
    print("Recording...")
    audio = sd.rec(int(5 * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, audio)
    print("Recording saved")

record_audio()

# Transcribe with whisper
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")
result = asr("temp.wav")
print("Transcript:", result["text"])

toxic = pipeline("text-classification", model="unitary/toxic-bert")
output = toxic(result["text"])
print("Toxicity:", output)

from deepface import DeepFace
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite("frame.jpg", frame)
cap.release()

analysis = DeepFace.analyze("frame.jpg", actions=['emotion'])
print("Detected Emotion:", analysis[0]['dominant_emotion'])

import gradio as gr

def detect_abuse(audio):
    transcript = asr(audio)["text"]
    toxicity = toxic(transcript)[0]
    return f"Transcript: {transcript}", f"Toxicity: {toxicity['label']} ({toxicity['score']:.2f})"

gr.Interface(
    fn=detect_abuse,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs=["text", "text"]
).launch()




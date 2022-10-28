import requests



"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/alanhernandez/Downloads/swift-firmament-365303-039e5e7f9d95.json"
from google.cloud import texttospeech
# Instantiates a client
client = texttospeech.TextToSpeechClient()

#----------------------------------------------------------
#PDF converting part


# importing required modules
import PyPDF2

# creating a pdf file object
pdfFileObj = open('/Users/alanhernandez/Downloads/beauty_and_the_beast.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(1)

# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=pageObj.extractText())

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')


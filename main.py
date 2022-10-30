import requests
import os
from google.cloud import texttospeech
import PyPDF2
from tkinter import *
from tkinter import filedialog
from pygame import mixer
path=""
file_name=""
playing=False

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/alanhernandez/Downloads/swift-firmament-365303-039e5e7f9d95.json"

#Find path of PDF file with filedialog
def filename_select(event) -> str:
    select_canvas.create_text(60, 60, text="✔", fill="green", font=("Ariel", 50, "bold"))
    global path
    print("entering function")
    window.filename=filedialog.askopenfilename(initialdir="/Users", title="Select A PDF File", filetypes=[(".pdf files", "*.pdf")])
    path=window.filename
    print(window.filename)
    print(f"Path: {path}")

def play_file(event) -> None:
    global playing
    global file_name
    print(f'File name is: {file_name}')
    if playing == False:
     play_canvas.itemconfig(play_container, image=pause_img)
     play_canvas.itemconfig(play_label, text="Pause")
     mixer.init()
     mixer.music.load(file_name)
     mixer.music.play()
     playing=True
    else:
        play_canvas.itemconfig(play_container, image=play_img)
        play_canvas.itemconfig(play_label, text="Play")
        mixer.music.stop()
        playing=False

def text_extraction():
    global path
    output = ""
    # creating a pdf file object
    pdfFileObj = open(path, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # printing number of pages in pdf file
    print(pdfReader.numPages)
    # creating a page object
    pageObj = pdfReader.getPage(2)
    # extracting text from page
    text_extracted=pageObj.extractText()
    print(len(text_extracted.encode('utf-8')))
    pdfFileObj.close()


    return text_extracted

def text_to_speech_gcs(event) -> None:
    convert_canvas.create_text(60, 60, text="✔", fill="green", font=("Ariel", 50, "bold"))
    global path
    global file_name
    file_name= entry.get() + ".mp3"
    print(file_name)
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_extraction())
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    # The response's audio_content is binary.
    with open(file_name, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {file_name}')

# # creating a pdf file object
# pdfFileObj = open('/Users/alanhernandez/PycharmProjects/Text To Speech Script/beauty_and_the_beast.pdf', 'rb')
#
# # creating a pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#
# # printing number of pages in pdf file
# print(pdfReader.numPages)
#
# # creating a page object
# pageObj = pdfReader.getPage(1)
#
# # extracting text from page
# print(type(pageObj.extractText()))
#
# text_extraction(pageObj.extractText())
#
# # closing the pdf file object
# pdfFileObj.close()



# # Instantiates a client
# client = texttospeech.TextToSpeechClient()
# # Set the text input to be synthesized
# synthesis_input = texttospeech.SynthesisInput(text=text_extraction(path))
# # Build the voice request, select the language code ("en-US") and the ssml
# # voice gender ("neutral")
# voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
# # Select the type of audio file you want returned
# audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
# # Perform the text-to-speech request on the text input with the selected
# # voice parameters and audio file type
# response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
# # The response's audio_content is binary.
# with open("output.mp3", "wb") as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')

BACKGROUND_COLOR = '#E9E9E9'

print(path)

window = Tk()
window.title("Audiobook Maker")
window.config(padx=100, pady=100, bg = BACKGROUND_COLOR)

# Logo Canvas
logo_canvas = Canvas(width=100, height = 100)
logo_img = PhotoImage(file="logo.png")
logo_canvas.create_image(48, 51, image=logo_img)
logo_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
logo_canvas.grid(row=0, column=0)

# Title Canvas
title_canvas = Canvas(width=300, height = 100)
title_canvas.create_text(120, 51, text="Audiobook Maker", fill="black", font=("Ariel", 30, "italic"))
title_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_canvas.grid(row=0, column=1, columnspan=2)

#Select Canvas
select_canvas = Canvas(width=100, height = 150)
select_img = PhotoImage(file="select.png")
select_canvas.create_image(48, 51, image=select_img)
select_canvas.create_text(60, 120, text="Select", fill="black", font=("Ariel", 15, "bold"))
select_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
select_canvas.bind('<Button>', filename_select)
select_canvas.grid(padx=(40,40), pady=(100, 15),row=1, column=0)

#Convert Canvas
convert_canvas = Canvas(width=100, height = 150)
convert_img = PhotoImage(file="convert.png")
convert_canvas.create_image(48, 51, image=convert_img)
convert_canvas.create_text(50, 120, text="Convert", fill="black", font=("Ariel", 15, "bold"))
convert_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
convert_canvas.bind('<Button>', text_to_speech_gcs)
convert_canvas.grid(padx=(40,40), pady=(100, 15), row=1, column=1)

#Play Canvas
play_canvas = Canvas(width=100, height = 150)
play_img = PhotoImage(file="play.png")
pause_img=PhotoImage(file="pause.png")
play_container=play_canvas.create_image(48, 51, image=play_img)
play_label=play_canvas.create_text(50, 120, text="Play", fill="black", font=("Ariel", 15, "bold"))
play_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
play_canvas.bind('<Button>', play_file)
play_canvas.grid(padx=(40,40), pady=(100, 15),row=1, column=2)

entry = Entry(width=30, background=BACKGROUND_COLOR, font=("Ariel", 15, "bold"))
entry.insert(END, string="NameYourFile")
#Gets text in entry
print(entry.get())
entry.grid(row=2, column=0, columnspan=3)



window.mainloop()


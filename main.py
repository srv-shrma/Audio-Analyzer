# Required Libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import mutagen
from mutagen.wave import WAVE
import json
import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt


r = sr.Recognizer()


# Function to get audio chunks for easy speech recognition
def get_large_audio_transcription(path):

    sound = AudioSegment.from_wav(path)
    # splitting audio sound where silence is 300 miliseconds or more and get chunks
    chunks = split_on_silence(
        sound,
        min_silence_len = 300,
        silence_thresh = sound.dBFS-14,
        keep_silence=300,
    )
    count_of_pauses = len(chunks)
    folder_name = "audio-chunks"
    # creating a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                pass
                # print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text, count_of_pauses


# def audio_duration(length):
# 	hours = length // 3600 # calculate in hours
# 	length %= 3600
# 	mins = length // 60 # calculate in minutes
# 	length %= 60
# 	seconds = length # calculate in seconds
#
# 	return hours, mins, seconds # returns the duration


# Function to create the dictionary from the text generated from audio
def count(elements):
    if elements[-1] == '.':
        elements = elements[0:len(elements) - 1]
    if elements in dictionary:
        dictionary[elements] += 1
    else:
        dictionary.update({elements: 1})


# Function to count the repetitive words
def cnt_repetition_of_words(dictionary):
    count_repetition_words = 0
    for allKeys in dictionary:
        if dictionary[allKeys] > 1:
            count_repetition_words += 1
    return count_repetition_words


# Function to write dictionary of repetitive words to json file
def convert_dict_json(dictionary):
    rep = {}
    for allKeys in dictionary:
        if dictionary[allKeys] > 1:
            rep[allKeys] = dictionary[allKeys]
    with open("repetitive_words.json", "w") as outfile:
        json.dump(rep, outfile, indent=4)


# "Understood" Driver Function
if __name__ == "__main__":

    dictionary = {}
    path = "asset/voicedatawav.wav"
    # print(get_large_audio_transcription(path))
    # Splitting the audio in smaller chunks by cutting it on the basis of pauses
    # simultaneously counting the pauses
    sentence, count_of_pauses = get_large_audio_transcription(path)
    audio = WAVE("asset/voicedatawav.wav")
    audio_info = audio.info
    length = int(audio_info.length)
    # hours, mins, seconds = audio_duration(length)
    mins = length / 60

    # splitting the text from audio to list of words
    lst = sentence.split()
    for elements in lst:
        count(elements)

    # saving repetitive words dictionary in json file
    # and saving conversion of audio to text in txt file
    convert_dict_json(dictionary)
    text_file = open("audioToText.txt", "w")
    text_file.write(sentence)
    text_file.close()

    # Plotting the audio signals and saving it with name graph_audio.jpeg
    plt.figure(figsize=(15, 4))
    data1, sample_rate1 = librosa.load(path, sr=22050, mono=True, offset=0.0, duration=50, res_type='kaiser_best')
    librosa.display.waveplot(data1, sr=sample_rate1, max_points=50000.0, x_axis='time', offset=0.0, max_sr=1000)
    # plt.show()
    plt.savefig("graph_audio.jpeg")

    # All the printing statements
    print('Text of the Audio :  {}' .format(sentence))
    print('Total Duration of audio in mins : {}'.format(mins))
    print()
    print('Total number of pauses : {}'.format(count_of_pauses))
    print('Total number of different words : {}'.format(len(dictionary)))
    print('Total number of repetitive words : {}'.format(cnt_repetition_of_words(dictionary)))
    print('Number of words spoken per minute : {}'.format(len(lst)//int(mins)))



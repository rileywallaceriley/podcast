import streamlit as st
from pydub import AudioSegment
from pytube import YouTube
import re
import os

# Function to process the uploaded audio file
def process_audio(audio_file):
    voiceover = AudioSegment.from_file(audio_file)
    return voiceover

# Function to process the script and download songs
def process_script(script_text):
    songs = []
    lines = script_text.split("\n")
    for line in lines:
        matches = re.findall(r'\[(.*?)\]', line)
        if matches:
            song_title = matches[0]
            search_query = f"{song_title} audio"
            try:
                yt_search = YouTube(f"https://www.youtube.com/results?search_query={search_query}")
                video_url = yt_search.streams.filter(only_audio=True).first().url
                songs.append({"title": song_title, "url": video_url})
            except:
                st.warning(f"Song '{song_title}' not found on YouTube.")
    return songs

# Function to download YouTube audio
def download_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path="downloads", filename="temp_audio")
    return os.path.join("downloads", "temp_audio" + audio_stream.subtype)

# Function to edit and mix audio segments
def edit_and_mix(voiceover, songs):
    edited_audio = voiceover
    for song in songs:
        st.write(f"Downloading {song['title']}...")
        audio_file = download_audio(song["url"])
        song_audio = AudioSegment.from_file(audio_file)
        # Assuming you want to insert the song audio after each mention
        edited_audio = edited_audio.append(song_audio, crossfade=1000)
    return edited_audio

# Function to export final edited audio
def export_audio(edited_audio):
    output_path = "output/podcast.mp3"
    edited_audio.export(output_path, format="mp3")
    return output_path

# Streamlit app interface
def main():
    st.title("Podcast Editor")
    
    # Upload audio file
    audio_file = st.file_uploader("Upload Audio File", type=["mp3"])
    
    # Input script text
    script_text = st.text_area("Paste Script Here")
    
    # Process audio and script when submitted
    if st.button("Edit Podcast"):
        if audio_file is not None and script_text != "":
            voiceover = process_audio(audio_file)
            songs = process_script(script_text)
            if songs:
                st.success("Songs found and downloaded successfully!")
                edited_audio = edit_and_mix(voiceover, songs)
                output_path = export_audio(edited_audio)
                st.success("Podcast edited successfully!")
                st.audio(output_path, format="audio/mp3", start_time=0)
                st.markdown(f"### [Download Edited Podcast]({output_path})")
            else:
                st.warning("No songs found in the script.")
        else:
            st.warning("Please upload an audio file and paste the script.")

if __name__ == "__main__":
    main()

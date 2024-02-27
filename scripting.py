import datetime
import openai
import requests
import streamlit as st

# Replace these with your actual API keys
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

openai.api_key = OPENAI_API_KEY

def get_current_date():
    """Returns the current date in a readable format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def create_dynamic_intro():
    """Generates a dynamic introduction for the podcast."""
    intro = f"Good morning, tech enthusiasts! It's {get_current_date()}, and you're listening to the RepuRocket Daily with your host. Let's dive into the cutting-edge of technology and innovation, sprinkled with good vibes and humor. Get ready for a ride into the future!"
    return intro

def search_for_news(api_key, query):
    """Searches for news articles using the Google Custom Search JSON API."""
    search_engine_id = 'YOUR_SEARCH_ENGINE_ID'
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
    response = requests.get(url)
    results = response.json().get('items', [])
    news_urls = [result['link'] for result in results[:3]]  # Limiting to top 3 results
    return news_urls

def summarize_news(news_urls):
    """Generates summaries for a list of news URLs using OpenAI's GPT-4."""
    prompts = [f"Summarize this article: {url}" for url in news_urls]
    summaries = []
    for prompt in prompts:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        summaries.append(response.choices[0].text.strip())
    return summaries

def find_songs(youtube_api_key, query):
    """Finds songs related to a query using the YouTube Data API."""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={query}&key={youtube_api_key}"
    response = requests.get(url)
    results = response.json().get('items', [])
    songs = [f"{result['snippet']['title']} (YouTube Link: https://www.youtube.com/watch?v={result['id']['videoId']})" for result in results if result['id'].get('videoId')]
    return songs

def main():
    st.title("Podcast Script Generator")
    
    intro = create_dynamic_intro()
    news_query = "latest technology news"
    # Assuming you have a function like this to fetch news URLs
    news_urls = search_for_news(GOOGLE_API_KEY, news_query)
    # Assuming you have a function to summarize these URLs
    news_summaries = summarize_news(news_urls)
    news_segment = "Here are today's top tech stories: " + " ".join(news_summaries)
    
    songs_query = "top tech innovation songs"
    # Assuming you have a function like this to find songs
    songs = find_songs(YOUTUBE_API_KEY, songs_query)
    mixtape_segment = "And now, let's get your mood right with our daily mixtape: " + " ".join(songs)
    
    full_script = f"{intro}\n\n{news_segment}\n\n{mixtape_segment}"
    
    # Use Streamlit functions to display the script
    st.subheader("Generated Podcast Script")
    st.text(full_script)  # This displays the full script as plain text. Use st.markdown for markdown.

if __name__ == "__main__":
    main()

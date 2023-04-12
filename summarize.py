import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define function to scrape text from a URL
def scrape_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return text

# Read in list of URLs from a page in a GitHub repo
url = 'https://raw.githubusercontent.com/<username>/<repo>/main/urls.txt'
response = requests.get(url)
urls = response.content.decode().split('\n')

# Remove empty elements from the list
urls = [u for u in urls if u]

# Generate summary using OpenAI API
for u in urls:
    text = scrape_text(u)
    prompt = f"Summarize the article at {u}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    print(f"Summary of {u}:")
    print(summary)

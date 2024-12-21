import requests
from bs4 import BeautifulSoup
import openai
import re

# Initialize the OpenAI API key
openai.api_key = ""

def fetch_article_content(url):
    """Fetches the content of an article from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the article text (customize the tag and class based on the website structure)
        paragraphs = soup.find_all('p')
        article_content = ' '.join([para.get_text() for para in paragraphs])

        return article_content
    except Exception as e:
        return f"Error fetching article content: {e}"

def analyze_article_credibility(article_content):
    """Analyzes the credibility of an article using OpenAI API."""
    try:
        prompt = (
            "Analyze the following article for credibility. Assess the tone, use of sources, potential bias, and fact-based claims. "
            "Group your analysis into categories: 'Tone', 'Sources', 'Bias', 'Fact-Based Claims', and 'Overall Assessment'. "
            "Provide an average credibility score between 1 and 10 based on your evaluation:\n\n"
            f"Article Content:\n{article_content}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional fact-checker and content analyzer."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the analysis and credibility score from the API's response
        analysis = response['choices'][0]['message']['content']
        return analysis
    except Exception as e:
        return f"Error analyzing article: {e}"

def is_link(string):
    """Checks if a string is a valid URL."""
    url_pattern = re.compile(
        r'^(https?://)?'  # http:// or https:// (optional)
        r'((([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})|'  # Domain name
        r'localhost|'  # localhost
        r'(\d{1,3}\.){3}\d{1,3})'  # OR IPv4 address
        r'(:\d+)?'  # Port number (optional)
        r'(/[-a-zA-Z0-9%_.~+]*)*'  # Path (optional)
        r'(\?[;&a-zA-Z0-9%_.~+=-]*)?'  # Query string (optional)
        r'(#[a-zA-Z0-9_]*)?$',  # Fragment identifier (optional)
        re.IGNORECASE
    )
    return re.match(url_pattern, string) is not None

# Main Program
def text_analysis(user_input):
    print("Welcome to the Article Credibility Verifier")

    if is_link(user_input):
        print("Fetching article content...")
        article_content = fetch_article_content(user_input)

        if article_content.startswith("Error"):
            print(article_content)
            return
    else:
        article_content = user_input

    print("Analyzing the article's credibility...")
    analysis = analyze_article_credibility(article_content)

    print("\n--- Analysis ---\n")
    print(analysis)
    return analysis

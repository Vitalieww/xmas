import requests
from bs4 import BeautifulSoup
import openai
import re
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv("./variables.env")
api_key = os.getenv("OPENAI_API_KEY")

# Validate OpenAI API Key
def validate_openai_api_key(api_key):
    """Validates the OpenAI API key by making a test request."""
    try:
        openai.api_key = api_key
        openai.Engine.list()  # Test request
        return True
    except openai.error.AuthenticationError:
        return False
    except Exception as e:
        print(f"Unexpected error during API key validation: {e}")
        return False

# Fetch Article Content
def fetch_article_content(url):
    """Fetches the content of an article from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        article_content = ' '.join([para.get_text() for para in paragraphs])

        return article_content if article_content.strip() else "Error: No article content found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching article content: {e}"

# Analyze Credibility
def analyze_article_credibility(article_content):
    """Generates a detailed credibility analysis using OpenAI."""
    try:
        prompt = (
            "Analyze the following article for credibility. Assess the tone, use of sources, potential bias, and fact-based claims. "
            "Group your analysis into categories: 'Tone', 'Sources', 'Bias', 'Fact-Based Claims', and 'Overall Assessment'. "
            "Provide an average credibility score between 1 and 10 based on your evaluation:\n\n"
            f"Article Content:\n{article_content}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional fact-checker and content analyzer."},
                {"role": "user", "content": prompt}
            ]
        )

        analysis = response['choices'][0]['message']['content']
        return analysis
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key."
    except Exception as e:
        return f"Error analyzing article: {e}"

# Summarize Analysis
def summarize_analysis(analysis):
    """Summarizes the analysis into criteria."""
    try:
        prompt = (
            "Summarize the following analysis into the criteria: 'Tone', 'Sources', 'Bias', 'Fact-Based Claims', and 'Overall Assessment'.\n\n"
            f"{analysis}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional summarizer."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        return f"Error summarizing analysis: {e}"

# Helper function to check if input is a URL
def is_link(string):
    """Checks if a string is a valid URL."""
    url_pattern = re.compile(
        r'^(https?://)?'
        r'((([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})|'
        r'localhost|'
        r'(\d{1,3}\.){3}\d{1,3})'
        r'(:\d+)?'
        r'(/[-a-zA-Z0-9%_.~+]*)*'
        r'(\?[;&a-zA-Z0-9%_.~+=-]*)?'
        r'(#[a-zA-Z0-9_]*)?$',
        re.IGNORECASE
    )
    return re.match(url_pattern, string) is not None

# Main Program
def text_analysis(user_input):
    """Main function to fetch, analyze, and summarize an article."""
    if not validate_openai_api_key(api_key):
        return "Error: Invalid OpenAI API key."

    # Fetch article content
    if is_link(user_input):
        article_content = fetch_article_content(user_input)
        if article_content.startswith("Error"):
            return article_content
    else:
        article_content = user_input

    if len(article_content.split()) < 50:
        return "Error: The provided text does not resemble an article."

    # Detailed analysis
    analysis = analyze_article_credibility(article_content)
    if "Error" in analysis:
        return analysis

    # Summarize analysis
    summary = summarize_analysis(analysis)

    return {"analysis": analysis, "summary": summary}
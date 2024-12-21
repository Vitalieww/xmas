import requests
from bs4 import BeautifulSoup
import openai

# Initialize the OpenAI API key
openai.api_key = "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"

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
            "Provide a brief assessment of its reliability and include a credibility score between 1 and 10 based on your evaluation:\n\n"
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

# Main Program
def main():
    print("Welcome to the Article Credibility Verifier")
    url = input("Enter the URL of the article to analyze: ")

    print("Fetching article content...")
    article_content = fetch_article_content(url)

    if article_content.startswith("Error"):
        print(article_content)
        return

    print("Analyzing the article's credibility...")
    analysis = analyze_article_credibility(article_content)

    print("\n--- Analysis ---\n")
    print(analysis)

if __name__ == "__main__":
    main()

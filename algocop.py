import requests 
from bs4 import BeautifulSoup 
import openai 
import re 
 
 
 
def validate_openai_api_key(api_key): 
    """Validates the OpenAI API key by making a test request.""" 
    try: 
        openai.api_key = api_key 
        openai.Engine.list()  # Test request to validate the API key 
        return True 
    except openai.error.AuthenticationError: 
        return False 
    except Exception as e: 
        print(f"Unexpected error during API key validation: {e}") 
        return False 
 
def fetch_article_content(url): 
    """Fetches the content of an article from a given URL.""" 
    try: 
        response = requests.get(url) 
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser') 
 
        # Extract the article text (customize the tag and class based on the website structure) 
        paragraphs = soup.find_all('p') 
        article_content = ' '.join([para.get_text() for para in paragraphs]) 
 
        return article_content if article_content.strip() else "Error: No article content found." 
    except Exception as e: 
        return f"Error fetching article content: {e}" 
 
def is_text_an_article(text): 
    """Checks if the provided text resembles an article.""" 
    word_count = len(text.split()) 
    if word_count < 50: 
        return False 
    return True 
 
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
    except openai.error.AuthenticationError: 
        return "Error: Invalid OpenAI API key." 
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
def text_analysis(user_input, api_key): 
    print("Welcome to the Article Credibility Verifier") 
 
    if not validate_openai_api_key(api_key): 
        analysis="Error: Invalid OpenAI API key." 
        return analysis 
 
    if is_link(user_input): 
        print("Fetching article content...") 
        article_content = fetch_article_content(user_input) 
 
        if article_content.startswith("Error"): 
            print(article_content) 
            return 
    else: 
        article_content = user_input 
 
    if not is_text_an_article(article_content): 
        analysis="Error: The provided text does not resemble an article." 
        return analysis 
 
    print("Analyzing the article's credibility...") 
    analysis = analyze_article_credibility(article_content) 
 
    print("\n--- Analysis ---\n") 
    print(analysis) 
    return analysis 
 
api_key = "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"
from flask import Flask, render_template, request
from algocop import text_analysis, api_key  # Assuming this is your text analysis function
import re

app = Flask(__name__)


# Function to extract the credibility score
def score_text(analysis):
    """Extracts the credibility score from the analysis text."""
    try:
        lines = analysis.splitlines()
        for line in lines:
            if "Credibility score" in line:
                for line in lines:
                    match = re.search(r'\b(?:10|[0-9])\b', line)
                    if match:
                        return match 
        return None  # Return None if no score is found
    except Exception as e:
        return f"Error extracting score: {e}"

# Function to format text with bold and newlines
def format_text_with_bold_and_newlines(text):
    """Formats text by adding newlines after periods and around bold sections marked with ."""
    parts = text.split('**')  # Split the text by 
    formatted_text = ''

    for i in range(len(parts)):
        if i % 2 == 0:  # Plain text (outside )
            # Add newlines after periods in plain text
            formatted_text += re.sub(r'\. ', '.\n', parts[i])  # Add newline after every period followed by space
        else:  # Bold text (inside )
            formatted_text += '\n**' + parts[i] + '**\n'  # Add newlines around bold text

    return formatted_text.strip()  # Remove trailing newline or spaces

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search')  # Get the search input from the query string
    if not query:
        return render_template('index.html', error="Please enter a query.")  # Handle empty query

    # Analyze the text and calculate the score
    result = text_analysis(query, api_key)  # Process the query with your text_analysis function
    score = score_text(result)  # Extract the score from the analysis
    print(result)
    # Format the result text
    formatted_result = format_text_with_bold_and_newlines(result)

    # Render the result page with the score and formatted result
    return render_template('result.html', score=score, result=formatted_result)

if __name__ == '__main__':
    app.run(debug=True)
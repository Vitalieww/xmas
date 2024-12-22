from flask import Flask, render_template, request
from algocop import text_analysis, summarize_analysis
import re

app = Flask(__name__)

# Extract score from analysis
def score_text(analysis):
    """Extracts the credibility score from the analysis text."""
    try:
        lines = analysis.splitlines()  # Split the analysis into individual lines
        for line in lines:
            if "credibility" in line.lower():  # Check for the keyword "credibility" in the line
                match = re.search(r'(\d+)/10', line)  # Look for a pattern like '6/10'
                if match:
                    return int(match.group(1))  # Return the numeric score as an integer
        return None  # Return None if no score is found
    except Exception as e:
        return f"Error extracting score: {e}"

# Flask routes
@app.route('/')
def index():
    """Render the index page with the search form."""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """Handle the search query and process the analysis."""
    query = request.args.get('search')  # Get the query string from the request
    if not query:
        return render_template('index.html', error="Please enter a query.")  # Handle empty query

    # Run text analysis
    result = text_analysis(query)  # Analyze the query using the imported text_analysis function
    if isinstance(result, str):  # If an error message is returned
        return render_template('index.html', error=result)

    # Extract score and get the summarized result
    score = score_text(result['analysis'])  # Extract the score from the analysis
    formatted_result = result['summary']  # Use the summary provided by the analysis

    # Render the result page with the score and formatted analysis
    return render_template('result.html', score=score, result=formatted_result)

if __name__ == '__main__':
    app.run(debug=True)
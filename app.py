from flask import Flask, render_template, request
from algocop import text_analysis, summarize_analysis
import re

app = Flask(__name__)


def process_analysis(formatted_list):
    """Convert analysis list into a dictionary and extract score."""
    result_dict = {}
    for item in formatted_list:
        # Split on first occurrence of ': '
        if ': ' in item:
            key, value = item.split(': ', 1)
            result_dict[key] = value

    # Extract numeric score from Credibility Score text
    if 'Credibility Score' in result_dict:
        score_text = result_dict['Credibility Score']
        score_match = re.search(r'(\d+)\s*out of\s*10', score_text)
        if score_match:
            # Format as '9/10'
            score = score_match.group(1)
            result_dict['Credibility Score'] = f"{score}/10"

    return result_dict



@app.route('/')
def index():
    """Render the index page with the search form."""
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    """Handle the search query and process the analysis."""
    query = request.args.get('search')
    if not query:
        return render_template('index.html', error="Please enter a query.")

    try:
        # Run text analysis
        result = text_analysis(query)
        if isinstance(result, str):
            return render_template('index.html', error=result)

        # Process the formatted result
        formatted_list = [line.strip() for line in result['summary'].split('\n') if line.strip()]
        result_dict = process_analysis(formatted_list)

        # Extract just the number from the score
        score = result_dict['Credibility Score'].split('/')[0]

        return render_template('result.html', score=score, result=result_dict)

    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
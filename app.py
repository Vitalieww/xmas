from flask import Flask, render_template, request
from algocop import text_analysis  # Assuming this is your text analysis function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search')  # Get the search input from the query string
    if query:
        result = text_analysis(query)  # Process the query with your text_analysis function
        return render_template('result.html', result=result)  # Pass the result to the result page
    else:
        return render_template('index.html', error="Please enter a query.")  # Handle empty query

if __name__ == '__main__':
    app.run(debug=True)

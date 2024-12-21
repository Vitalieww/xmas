from flask import Flask, render_template, request
from algocop import text_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Handle the search request
    query = request.args.get('search')  # Get the search input
    print(text_analysis(query))
    return render_template("result.html")

if __name__ == '__main__':
    app.run(debug=True)

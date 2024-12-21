from flask import Flask, render_template, request 
from algocop import text_analysis, api_key # Assuming this is your text analysis function 
def format_text_around_bold(text): 
    """Adds a newline before and after each pair of '**'.""" 
    parts = text.split('**') 
    formatted_text = '' 
    for i in range(len(parts)): 
        if i % 2 == 0: 
            formatted_text += parts[i]  # Add the plain text 
        else: 
            formatted_text += '\n**' + parts[i] + '**\n'  # Add newlines around the bold text 
    return formatted_text.strip()  # Remove trailing newline 
app = Flask(__name__) 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/search', methods=['GET']) 
def search(): 
    query = request.args.get('search')  # Get the search input from the query string 
    if query: 
        result = text_analysis(query, api_key)  # Process the query with your text_analysis function 
        formatted_result = format_text_around_bold(result)  # Format the result text 
        return render_template('result.html', result=formatted_result)  # Pass the formatted result to the result page 
    else: 
        return render_template('index.html', error="Please enter a query.")  # Handle empty query 
 
 
if __name__ == '__main__': 
    app.run(debug=True)
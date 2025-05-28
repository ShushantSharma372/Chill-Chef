from flask import Flask, request, jsonify
from recommendation_engine import recommend_recipes

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    ingredients = data.get('ingredients', '')

    if not ingredients:
        return jsonify({'error': 'No ingredients provided'}), 400

    results = recommend_recipes(ingredients)
    return jsonify({'recommended_recipes': results})

if __name__ == '__main__':
    app.run(debug=True)

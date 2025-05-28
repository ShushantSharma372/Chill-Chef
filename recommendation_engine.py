# recommendation_engine.py
import pickle
import pandas as pd
import numpy as np
import re
import ast
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open('recipe_recommendation_model.pkl', 'rb') as f:
    vocab = pickle.load(f)

df = pd.read_csv('recipes_processed1.csv')
df['Ingredient_Vector'] = df['Ingredient_Vector'].apply(ast.literal_eval)

def vectorize_ingredients(ingredient_str, vocab):
    vector = [0] * len(vocab)
    ingredients = [ingredient.strip().lower() for ingredient in re.split(r',|\s', ingredient_str) if ingredient]
    lemmatized_ingredients = [lemmatizer.lemmatize(ingredient) for ingredient in ingredients]
    for ingredient in ingredients:
        if ingredient in vocab:
            vector[vocab.index(ingredient)] = 1
    return vector

def recommend_recipes(user_vector, top_n=5):
    recipe_vectors = np.array(df['Ingredient_Vector'].tolist())
    user_vector = vectorize_ingredients(user_vector, vocab)
    user_vector = np.array(user_vector).reshape(1, -1)
    similarity_scores = cosine_similarity(user_vector, recipe_vectors)[0]
    
    recipe_similarity = list(enumerate(similarity_scores))
    top_indices = sorted(recipe_similarity, key=lambda x: x[1], reverse=True)[:top_n]
    
    results = []
    for index, score in top_indices:
        name = df.loc[index, 'Title']
        diff = df.loc[index, 'Difficulty']
        url = df.loc[index, 'Link']
        image = df.loc[index, 'Image Link']
        time = df.loc[index, 'Total Cook Time']
        results.append({'name': name, 'Difficulty': diff, 'url': url, 'time': time, 'image':image})
    
    return results

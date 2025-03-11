# ----------------------------------------------
# Section 1: Import necessary libraries
# ----------------------------------------------
import openai
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import json
import os
from dotenv import load_dotenv


# ----------------------------------------------
# Section 2: Load API Key & Data
# ----------------------------------------------

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load dataset of products
DATA_FILE = "products.json"  # Updated dataset name
df = pd.read_json(DATA_FILE)

# Load SentenceTransformer for text embedding
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Compute embeddings for product descriptions
df["embedding"] = df["description"].apply(lambda x: embedding_model.encode(x) if isinstance(x, str) else np.zeros(384))

# Define JSON file to store recommendation history
RECOMMENDATIONS_FILE = "recommendations.json"


# ----------------------------------------------
# Section 3: Functions for Processing Queries
# ----------------------------------------------

def get_text_embedding(text):
    """Generate an embedding vector for a given text using SentenceTransformer."""
    return embedding_model.encode(text)

def analyze_user_input(user_query):
    """
    Extracts structured product details from the user query using OpenAI API.
    - Identifies product category, budget range, and key features.
    """
    prompt = f"""
    You are a smart shopping assistant. Extract:
    - Category (e.g., shoes, electronics, clothing)
    - Budget (e.g., 50-200 USD)
    - Key features (e.g., waterproof, lightweight, gaming)

    User query: "{user_query}"
    
    Provide output in JSON format with keys: "category", "budget", "features".
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    
    extracted_info = response["choices"][0]["message"]["content"]
    print(f"Extracted Query Info: {extracted_info}")  # Debugging output
    
    return extracted_info


def recommend_products(user_query, top_n=5):
    """
    Generates product recommendations based on user query analysis.
    Uses:
    - Semantic similarity matching
    - Product popularity (rating & review count)
    - Budget filtering if provided
    """
    extracted_info = analyze_user_input(user_query)

    # Extract key details
    category = extracted_info.get("category")
    budget = extracted_info.get("budget")
    features = extracted_info.get("features")

    # Step 1: Filter dataset based on extracted category
    filtered_df = df[df["category"].str.lower() == category.lower()] if category else df

    # Step 2: Filter by budget range (if provided)
    if budget and isinstance(budget, list) and len(budget) == 2:
        min_price, max_price = budget
        filtered_df = filtered_df[(filtered_df["price"] >= min_price) & (filtered_df["price"] <= max_price)]

    # Step 3: Compute semantic similarity between user query and product descriptions
    query_embedding = get_text_embedding(user_query)
    filtered_df["similarity_score"] = filtered_df["embedding"].apply(lambda emb: cosine_similarity([query_embedding], [emb])[0][0])

    # Step 4: Compute final weighted score combining:
    # - Semantic similarity (60%)
    # - Product rating (30%)
    # - Review count (10%)
    filtered_df["final_score"] = (
        filtered_df["similarity_score"] * 0.6 +
        filtered_df["rate"] * 0.3 +
        np.log1p(filtered_df["review_count"]) * 0.1
    )

    # Debugging line to see ranking of recommendations
    print(filtered_df[["title", "similarity_score", "final_score"]].sort_values(by="final_score", ascending=False).head(10))

    # Step 5: Return top recommendations
    filtered_df = filtered_df.sort_values(by="final_score", ascending=False)
    return filtered_df.head(top_n)[["title", "price", "description", "rate", "review_count"]].to_dict(orient="records")


# ----------------------------------------------
# Section 4: Handling Cold Start Problem
# ----------------------------------------------

def recommend_products_with_fallback(user_query, top_n=5):
    """
    Handles recommendations for cases where little or no user data is available (Cold Start Problem).
    - If no recommendations are found, return the most popular products based on rating & reviews.
    """
    try:
        recommendations = recommend_products(user_query, top_n)

        if not recommendations:  # Only fallback if no real recommendations exist
            print("⚠ No valid recommendations found! Using fallback...")
            return df.sort_values(by=["rate", "review_count"], ascending=False).head(top_n)[
                ["title", "price", "description", "rate", "review_count"]
            ].to_dict(orient="records")

        return recommendations

    except Exception as e:
        print(f"Error in recommendation system: {str(e)}")
        return df.sort_values(by=["rate", "review_count"], ascending=False).head(top_n)[
            ["title", "price", "description", "rate", "review_count"]
        ].to_dict(orient="records")


# ----------------------------------------------
# Section 5: JSON Storage for Recommendations
# ----------------------------------------------

def load_existing_recommendations():
    """Load existing recommendations from JSON file."""
    if os.path.exists(RECOMMENDATIONS_FILE):
        with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_recommendations(query, recommendations):
    """Save new recommendations to JSON, keeping previous searches."""
    data = load_existing_recommendations()
    data.append({"query": query, "recommendations": recommendations})
    with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ----------------------------------------------
# Section 6: Flask API Integration
# ----------------------------------------------

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({"message": "API is running"})

@app.route("/recommend", methods=["POST"])
def recommend():
    """API endpoint for product recommendations."""
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    recommendations = recommend_products_with_fallback(user_query)
    return jsonify({"query": user_query, "recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)

import streamlit as st
import json
import requests
import os


# ----------------------------------------------
# Section 1: Cache Handling (Clearing Previous Results)
# ----------------------------------------------

# Configure Streamlit page settings
st.set_page_config(page_title="Smart Shopping Assistant", layout="wide")


# Button to clear cached data and restart UI
if st.button("Clear Cache & Restart"):
    st.cache_data.clear()  # Clear cached data
    st.rerun()  # Restart UI


# ----------------------------------------------
# Section 2: API and File Configurations
# ----------------------------------------------

# Define the API endpoint of the Flask server
API_URL = "http://127.0.0.1:5000/recommend"

# Define the JSON file to store search history and recommendations
RECOMMENDATIONS_FILE = "recommendations.json"


# ----------------------------------------------
# Section 3: Helper Functions (Loading and Saving Recommendations)
# ----------------------------------------------

def load_existing_recommendations():
    """
    Load previous recommendations from the JSON file.
    If the file does not exist or is corrupted, return an empty list.
    """
    try:
        with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)  # Load the existing recommendations
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file is missing or corrupted


def save_recommendations(query, recommendations):
    """
    Save new recommendations to the JSON file while preserving previous searches.
    If no previous file exists, a new one is created.
    """
    data = load_existing_recommendations()  # Load current data
    data.append({"query": query, "recommendations": recommendations})  # Append the new query

    # Write the updated data back to the file
    with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ----------------------------------------------
# Section 4: Streamlit UI Setup
# ----------------------------------------------


# Display the page title and instructions
st.title("Smart Shopping Assistant")
st.subheader("Enter your query below to get product recommendations.")

# User input field for product search
query = st.text_input("What are you looking for?", placeholder="e.g. I need a gaming laptop under $1500")


# ----------------------------------------------
# Section 5: Handling User Input and API Calls
# ----------------------------------------------

# When the user clicks the button, send a request to the API
if st.button("Get Recommendations"):
    if query:  # Ensure input is not empty
        with st.spinner("Fetching recommendations..."):  # Show loading indicator
            try:
                response = requests.post(API_URL, json={"query": query})  # Send request to Flask API

                if response.status_code == 200:  # If response is successful
                    result = response.json()  # Parse the JSON response
                    recommendations = result.get("recommendations", [])  # Extract the recommended products

                    if recommendations:
                        # Display the recommendations on the UI
                        st.success(f"Here are your recommendations for: **{query}**")
                        for item in recommendations:
                            st.markdown(f"**{item['title']}** - ${item['price']}")
                            st.markdown(f"*{item['description']}*")
                            st.markdown(f"⭐ Rating: {item['rate']} ({item['review_count']} reviews)")
                            st.write("---")

                        # Save the query and recommendations to JSON for history tracking
                        save_recommendations(query, recommendations)

                    else:
                        st.warning("No recommendations found. Try a different query.")

                else:
                    st.error("Error fetching recommendations. Please try again.")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

    else:
        st.warning("Please enter a query before searching.")


# ----------------------------------------------
# Section 6: Displaying Search History
# ----------------------------------------------

# Button to show search history
if st.button("Show Search History"):
    history = load_existing_recommendations()  # Load the stored recommendations

    if history:
        st.subheader("Search History")  # Title for history section
        for entry in reversed(history):  # Display the latest searches first
            st.write(f"**Query:** {entry['query']}")
            for item in entry["recommendations"]:
                st.markdown(f"- **{item['title']}** - ${item['price']} ⭐ ({item['rate']}/5)")
            st.write("---")  # Separator for readability
    else:
        st.warning("No previous searches found.")  # Display if no history exists


import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import streamlit as st
import json
import numpy as np
import scipy.sparse as sp
import implicit

# Need to first save track metadata and trained ALS model to artifacts folder   
# Add this after the cell that generates track metadata list:
# track_metadata_str_keys = {str(k): v for k, v in track_metadata.items()}

# with open(ART_DIR / "track_metadata.json", "w", encoding="utf-8") as f:
#     json.dump(track_metadata_str_keys, f)

# print("Saved track_metadata.json successfully!")

# Add this after the cell that trains ALS model:
# als_model.save(ART_DIR / "als_model.npz")
# print("Model saved successfully!")

# 1. Setup Paths & Load Data Safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ART_DIR = os.path.join(BASE_DIR, 'artifacts_mpd_shannon')

@st.cache_resource
def load_data():
    with open(os.path.join(ART_DIR, 'track_metadata.json'), 'r', encoding="utf-8") as f:
        track_metadata = json.load(f)
    with open(os.path.join(ART_DIR, 'track2idx.json'), 'r', encoding="utf-8") as f:
        track2idx = json.load(f)
        
    model_path = os.path.join(ART_DIR, 'als_model.npz')
    if os.path.exists(model_path):
        model = implicit.cpu.als.AlternatingLeastSquares.load(model_path)
    else:
        model = None
        
    return track_metadata, track2idx, model

track_metadata, track2idx, model = load_data()

# 2. Setup "Memory" for the app (Session State)
if 'seed_playlist' not in st.session_state:
    st.session_state.seed_playlist = []

# --- BUILD THE USER INTERFACE ---
st.title("🎵 AI Playlist Continuer")

if model is None:
    st.error("⚠️ Model not found! Please check your file paths.")
    st.stop()

# --- Section 1: The Playlist Builder ---
st.subheader("🎧 Your Seed Playlist")

if not st.session_state.seed_playlist:
    st.info("Your playlist is empty! Search below to add some tracks.")
else:
    for i, track in enumerate(st.session_state.seed_playlist):
        st.write(f"**{i+1}.** {track['name']} by {track['artist']}")
    
    if st.button("🗑️ Clear Playlist"):
        st.session_state.seed_playlist = []
        st.rerun()

st.divider()

# --- Section 2: The Search Bar ---
search_query = st.text_input("Search for a song to add to your playlist:")

if search_query:
    matches = []
    for idx, data in track_metadata.items():
        if search_query.lower() in data['track_name'].lower():
            matches.append((idx, data['track_name'], data['artist_name'], data['track_uri']))
            if len(matches) >= 5: 
                break
                
    if not matches:
        st.warning("No songs found.")
    else:
        st.write("*Click to add a track:*")
        for idx, track_name, artist, uri in matches:
            if st.button(f"➕ {track_name} by {artist}", key=f"search_{idx}"):
                st.session_state.seed_playlist.append({
                    'name': track_name,
                    'artist': artist,
                    'math_index': track2idx[uri]
                })
                # Clear the search bar text visually by rerunning
                st.rerun()

st.divider()

# --- Section 3: The AUTO-GENERATING AI Recommendations ---
# If they have at least 1 track, we instantly show recommendations!
if len(st.session_state.seed_playlist) > 0:
    st.subheader("🔥 AI Recommendations")
    st.write("Click ➕ to add a recommended song to your playlist. The AI will instantly adapt to your new vibe!")
    
    # 1. Get all math indices from the session state
    seed_indices = [track['math_index'] for track in st.session_state.seed_playlist]
    
    # 2. Build the Matrix Row for this user
    num_total_tracks = len(track2idx)
    data = [1.0] * len(seed_indices)
    rows = [0] * len(seed_indices) 
    user_items = sp.csr_matrix((data, (rows, seed_indices)), shape=(1, num_total_tracks))
    
    # 3. Ask the model for recommendations (ask for extra in case of duplicates)
    ids, scores = model.recommend(0, user_items[0], N=20, recalculate_user=True)
    
    # 4. Display results with Add Buttons!
    rank = 1
    for recommended_idx in ids:
        rec_idx_int = int(recommended_idx) # Ensure it's a clean integer
        
        # Don't recommend songs already in the seed playlist
        if rec_idx_int not in seed_indices:
            rec_data = track_metadata[str(rec_idx_int)]
            
            # Use columns to make it look like a real app (Text on left, Button on right)
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**{rank}.** {rec_data['track_name']} by {rec_data['artist_name']}")
                
            with col2:
                # Add a unique key to the button so Streamlit doesn't get confused
                if st.button("➕ Add", key=f"rec_{rec_idx_int}"):
                    st.session_state.seed_playlist.append({
                        'name': rec_data['track_name'],
                        'artist': rec_data['artist_name'],
                        'math_index': rec_idx_int
                    })
                    # Rerun instantly recalculates the math with the new song included!
                    st.rerun()
            
            rank += 1
            if rank > 10:
                break

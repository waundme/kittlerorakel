import faiss
import pickle
import pandas as pd
import streamlit as st
from PIL import Image
from sentence_transformers import SentenceTransformer
from vector_engine.utils import vector_search, id2details


@st.cache
def read_data(data="sentences.csv"):
    """Read the data from local."""
    return pd.read_csv(data)


@st.cache(allow_output_mutation=True)
def load_bert_model(name="T-Systems-onsite/cross-en-de-roberta-sentence-transformer"):
    """Instantiate a sentence-level cross-language RoBERTa model."""
    return SentenceTransformer(name)


@st.cache(allow_output_mutation=True)
def load_faiss_index(path_to_faiss="models/faiss_index.pickle"):
    """Load and deserialize the Faiss index."""
    with open(path_to_faiss, "rb") as h:
        data = pickle.load(h)
    return faiss.deserialize_index(data)

def load_image_from_local(image_path, image_resize=None):
    image = Image.open(image_path)

    if isinstance(image_resize, tuple):
        image = image.resize(image_resize)
    return image

def main():
    # Load data and models
    data = read_data()
    model = load_bert_model()
    faiss_index = load_faiss_index()

    #st.set_page_config(page_title="Kittlerorakel")
    st.title("Kittlerorakel")
    st.image("img/kittler2.jpg", caption="Credit: IMAGO / DRAMA-Berlin.de")
    #st.image(load_image_from_local("img/kittler.jpg"))
    
    # User search
    user_input = st.text_area("Frag das Orakel", "")
    
    # Filters
    #st.sidebar.markdown("**Filters**")
    #filter_year = st.sidebar.slider("Publication year", 2010, 2021, (2010, 2021), 1)
    #filter_citations = st.sidebar.slider("Citations", 0, 250, 0)
    num_results = st.sidebar.slider("Anzahl der Orakelsätze", 10, 20, 30)

    # Fetch results
    if st.button("Antwort!") or user_input:
        D, I = vector_search([user_input], model, faiss_index, num_results)
        
        titles = id2details(data, I, "Title")
        texts = id2details(data, I, "Text")

        for i in range(1, num_results):
            st.write(f"""**{str(texts[i][0])}** (aus: {str(titles[i][0]).replace(".pdf", "")})""")


if __name__ == "__main__":
    main()

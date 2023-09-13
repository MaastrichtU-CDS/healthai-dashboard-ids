import numpy as np
import plotly.express as px
import streamlit as st
from fldemo.common import init
from fldemo.kmeans import KmeansAlgo


def render_kmeans_download_page():
    algo: KmeansAlgo = st.session_state['kmeans_algo']

    st.write("# Kmeans TNM model")
    st.write("Kmeans is a clustering algorithm used in the demo to cluster \
             patients based on their TNM data. The model is trained on TNM data from the \
             lung1 dataset")

    model = algo.get_model()

    if model is None:
        st.write("No model available")
        return

    st.write("### Quick overview")
    st.write("For no other that demonstration purposes and so you may be able to pick up a on differences between different trained modles, here's a quick visualization of it")

    # Convert to numpy array and transpose for easier indexing
    model = np.array(model["centroids"]).T

    # Create Plotly figure
    fig = px.scatter_3d(x=model[0], y=model[1], z=model[2])

    # Update layout to change initial camera angle
    fig.update_layout(
        scene_camera=dict(
            eye=dict(x=1.25, y=1.75, z=1.5)
        )
    )

    # Display figure in Streamlit
    st.plotly_chart(fig)

    st.write("## Download model")
    st.write("You can download the model and use for your own application or research")
    st.write("The model is stored in json format")

    st.download_button('Download :arrow_down:', data=algo.get_model_bytes(), file_name='kmeans.json', mime='application/json')


init()

if st.session_state.get("authentication_status"):
    render_kmeans_download_page()
else:
    st.warning('Please log in to see this dashboard')

import streamlit as st
from fldemo.basealgo import BaseAlgo
from fldemo.common import init
from fldemo.kmeans import KmeansAlgo
from fldemo.stats import StatsAlgo
import json

def request_model_run(algo: BaseAlgo, **params):
    with st.status("Executing model run...", expanded=True) as status:
        algo.request_new_model()

    st.write("Saving new model") 
    saved = algo.save_model()
    if saved:
        st.write("Saved new model")
    else:
        st.write("A model already existed, and overwritting was deemed not safe. Model not saved.")

    return algo

def render_request_page():
    # load workers.json
    endpoint = st.session_state["flconfig"]["endpoint"]
    workers = st.session_state["flconfig"]["workers"]

    st.write("#### Workers on which to run the model")
    for i, worker in enumerate(workers):
        workers[i]['widget'] = st.toggle(worker['name'], value=worker['default'])

    # select which algorithm to run: either kmeans or stats
    st.write("#### Algorithm to run")
    alg = st.selectbox('Algorithm', options=['stats', 'kmeans'])

    st.write("#### General parameters")
    # select dataset
    dataset = st.selectbox('Dataset', options=['lung1_test.csv'])

    do_overwrite = st.checkbox('Overwrite previous model if smaller')

    # add some space
    st.write('')

    st.write(f"##### Parameters for algorithm {alg}")
    # if kmeans, select number of clusters
    if alg == 'kmeans':
        k = st.slider('Number of clusters', min_value=2, max_value=10, value=4)
        centroids = st.text_area("Initial centroids (JSON)", value='[[1, 0, 0], [2, 1, 0], [3, 2, 0], [5, 3, 1]]')
        columns = st.multiselect('Columns to use for clustering', options=['t', 'n', 'm'], default=['t', 'n', 'm'])
        epsilon = st.number_input('Convergence criterion epsilon', min_value=0.01, max_value=1.0, value=0.01)
        max_iter = st.number_input('Maximum number of iterations', min_value=1, max_value=100, value=10)

    # if stats, select 'cutoff' and 'delta'
    if alg == 'stats':
        cutoff = st.number_input('Cutoff (survival curve)', min_value=30, max_value=4000, value=365)
        delta = st.number_input('Delta (survival curve)', min_value=1, max_value=4000, value=30)

    # add button to recollect information and do a request.post to the server with 'algo', 'dataset', 'k', 'cutoff', 'delta', 'workers'
    if st.button('Request model run'):
        new_algo: BaseAlgo = None
        workers_ids = [worker['id'] for worker in workers if worker['widget']]
        # TODO: can definitely be improved..
        if alg == 'kmeans':
            centroids = json.loads(centroids)
            new_algo = KmeansAlgo(
                endpoint=st.session_state['kmeans_algo'].endpoint,
                overwrite=do_overwrite,
                model_path=st.session_state['kmeans_algo'].model_path,
                file_key=dataset,
                workers=workers_ids,
                k=k,
                centroids=centroids,
                epsilon=epsilon,
                columns=columns,
                max_iter=max_iter
            )
        elif alg == 'stats':
            new_algo = StatsAlgo(
                endpoint=st.session_state['stats_algo'].endpoint,
                overwrite=do_overwrite,
                model_path=st.session_state['stats_algo'].model_path,
                file_key=dataset,
                workers=workers_ids,
                cutoff=cutoff,
                delta=delta
            )
        request_model_run(new_algo)


init()

if not st.session_state.get("authentication_status"):
    st.warning('Please log in to see this dashboard')
else:
    render_request_page()


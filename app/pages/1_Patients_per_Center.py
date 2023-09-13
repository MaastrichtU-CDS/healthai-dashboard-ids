import logging

import pandas as pd
import streamlit as st
from fldemo.common import init
from fldemo.stats import StatsAlgo

logger = logging.getLogger(__name__)

def plot_patients_per_center():
    algo: StatsAlgo = st.session_state['stats_algo']
    data = algo.get_model()["results"]
    if data is None:
        st.write("No data available")
        return
    df = pd.DataFrame(data)
    st.bar_chart(df[['organisation', 'nids']].set_index('organisation'))


st.title("Patients per center")
st.write('')


logger.info("Initializing....")
init()

if st.session_state.get("authentication_status"):
    plot_patients_per_center()
else:
    st.warning('Please log in to see this dashboard')

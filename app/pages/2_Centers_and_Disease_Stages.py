import streamlit as st
from fldemo.common import init, plot_patients_per_stage_and_attr

st.title("Patients per stage and center")
st.write('')


init()

if st.session_state.get("authentication_status"):
    data = st.session_state['stats_algo'].get_model()["results"]
    plot_patients_per_stage_and_attr(data, 'stage', transpose='both')
else:
    st.warning('Please log in to see this dashboard')

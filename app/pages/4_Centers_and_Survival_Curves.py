import pandas as pd
import streamlit as st
from fldemo.common import init
from matplotlib import pyplot as plt


def plot_survival_curve_per_center(data, cutoff, delta):
    df = pd.DataFrame(data)

    sel_center = st.selectbox('Select center', options=list(df['organisation']))

    org_df = df[df['organisation'] == sel_center]
    # not sure why it gets saved as a series of a list... but it does so we explode()
    survival = org_df['survival'].explode()
    ax = pd.DataFrame({
        'survival rate': survival,
        'survival days': list(range(0, cutoff, delta))
    }).plot(x='survival days', y='survival rate', title=f'Survival curve for {sel_center}', legend=False)
    ax.set_xlabel('days')
    ax.set_ylabel('survival rate')

    st.pyplot(plt.gcf())


st.title("Survival curve per center")
st.write('')

init()

if st.session_state.get("authentication_status"):
    data = st.session_state['stats_algo'].get_model()
    plot_survival_curve_per_center(data['results'], cutoff=data['cutoff'], delta=data['delta'])
else:
    st.warning('Please log in to see this dashboard')



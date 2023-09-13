import json
import logging
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from fldemo.stats import StatsAlgo
from fldemo.kmeans import KmeansAlgo
import streamlit_authenticator as stauth

TIMEOUT_SECONDS = 30
FL_CONFIG_PATH = Path('config/config.json')
CRED_CONFIG_PATH = Path('config/credentials.yaml')
DATA_DIR = Path('data/')
STATS_DATA_FILE = 'stats.json'
KMEANS_DATA_FILE = 'kmeans.json'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def init():
    """ Initializes session_state."""

    # if not logged in, log in the user
    if 'authenticator_obj' not in st.session_state:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s | %(message)s')
        logger.info("Loading credentials file: %s", CRED_CONFIG_PATH)
        with open(CRED_CONFIG_PATH) as file:
            creds_config = yaml.load(file, Loader=SafeLoader)
        logger.info("Initializing authenticator object")
        authenticator = stauth.Authenticate(
            creds_config['credentials'],
            creds_config['cookie']['name'],
            creds_config['cookie']['key'],
            creds_config['cookie']['expiry_days'],
            creds_config['preauthorized']
        )
        logger.info("Logging in user")
        # FIXME: this doesn't work.. st.writes on pages overwrite this..?
        authenticator.login('Login', 'main')
        st.session_state['authenticator_obj'] = authenticator
    else:
        logger.info("Authenticator object already initialized")

    is_authed = st.session_state.get("authentication_status")
    logger.info("Authentication status: %s", is_authed)

    # 'flconfig' because I'm paranoid it might clash with some streamlit variable.. 
    if is_authed and 'flconfig' not in st.session_state:
        logger.info("Loading config file: %s", FL_CONFIG_PATH)
        with open(FL_CONFIG_PATH) as file:
            st.session_state['flconfig'] = yaml.load(file, Loader=SafeLoader)

    # NOTE: In a FL setting, it's probably a better idea to have the trained
    # model and the metadata about the model separate.  It's interesting to know
    # which nodes participated in the training, who did the aggregation, etc,
    # but it's potentially sensitive data. In this case, for this demo, we've
    # just assumed that metadata for the initial stored model and put it in the
    # config file.
    if is_authed and 'stats_algo' not in st.session_state:
        logger.info("Loading initial stats model")
        config = st.session_state['flconfig']
        st.session_state['stats_algo'] = StatsAlgo(
            endpoint=config['endpoint'],
            model_path=DATA_DIR / STATS_DATA_FILE,
            file_key=config['file_keys'][0],
            workers=config['workers']
        )

    if is_authed and 'kmeans_algo' not in st.session_state:
        logger.info("Loading initial kmeans model")
        config = st.session_state['flconfig']
        st.session_state['kmeans_algo'] = KmeansAlgo(
            endpoint=config['endpoint'],
            model_path=DATA_DIR / KMEANS_DATA_FILE,
            file_key=config['file_keys'][0],
            workers=config['workers']
        )


def plot_patients_per_stage_and_attr(data, attr: str, transpose: str = 'no'):
    if data is None:
        st.write("No data available")
        return

    df = pd.DataFrame(data)

    attrs = {}
    for stage, org_name in zip(df[attr], df['organisation']):
        attrs[org_name] = {stage[attr][k]: stage['id'][k] for k in stage[attr]}

    if transpose != 'only':
        pd.DataFrame(attrs).plot(kind='bar', stacked=True)
        # axis labels
        plt.xlabel(attr)
        plt.ylabel('number of patients')
        st.pyplot(plt.gcf())
    if transpose == 'both' or transpose == 'only':
        pd.DataFrame(attrs).T.plot(kind='bar', stacked=True)
        plt.xlabel('center')
        plt.ylabel('number of patients')
        st.pyplot(plt.gcf())

    if transpose not in ['no', 'both', 'only']:
        logger.warning("Invalid transpose value: %s", transpose)
        logger.warning("Valid values are: 'no', 'both', 'only'")



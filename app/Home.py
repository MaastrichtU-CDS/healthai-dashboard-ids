import logging
from pathlib import Path

import streamlit as st
from fldemo.common import init

logger = logging.getLogger(__name__)

FL_CONFIG_PATH = Path('config/config.json')
CRED_CONFIG_PATH = Path('config/credentials.yaml')
DATA_DIR = Path('data/')
STATS_DATA_FILE = 'stats.json'
KMEANS_DATA_FILE = 'kmeans.json'


def main():
    st.set_page_config(page_title='Home')
    st.write("# HealthAI TNO's TSG demonstration")
    st.write("### Log in using left panel to explore dashboards")
    st.write('''
             HealthAI dashboard aiming to demonstrate multi-center analysis in a federated fashion.\n
             Using [TNO Security Gateway](https://tno-tsg.gitlab.io/) implementation.
             ''')

    init()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s | %(message)s')
    main()

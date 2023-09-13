import logging

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

logger = logging.getLogger(__name__)


def render_login_page():
    # TODO: troubleshoot why auth is not working as expected and merge this with init() in common.py...
    with open('config/credentials.yaml') as file:
        creds_config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        creds_config['credentials'],
        creds_config['cookie']['name'],
        creds_config['cookie']['key'],
        creds_config['cookie']['expiry_days'],
        creds_config['preauthorized']
    )

    authenticator.login('Login', 'main')

    if st.session_state.get("authentication_status"):
        authenticator.logout('Logout', 'main', key='unique_key')
        st.title(f'Welcome {st.session_state["name"]}')
        st.write('Use the pages on the left panel to explore different statistics')
    elif st.session_state.get("authentication_status") is False:
        logger.info("User failed to login")
        st.error('Username/password is incorrect')
    elif st.session_state.get("authentication_status") is None:
        st.warning('Please enter your username and password')

render_login_page()

import json
import logging
import time
from abc import ABC, abstractmethod

import requests
import streamlit as st

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TIMEOUT_SECONDS = 30


class BaseAlgo(ABC):
    """ Represents and handles an algorithm run. Its execution and its result. Warning: it st.writes()!"""
    def __init__(self, algo, endpoint, model_path, do_overwrite, file_key, workers):
        self.endpoint = endpoint
        self.algo = algo
        self.file_key = file_key
        self.workers = workers
        self.do_overwrite = do_overwrite
        self.model = None
        # path to the current model, used to save the model
        self.model_path = model_path
        # json_req will be sent to /initialize endpoint, exndenting classes may
        # super().__init__() and then add more fields to it
        self.json_req = {
            "algo": algo,
            "key": file_key,
            "rounds": 1,
            "workers": workers
        }

    def request_new_model(self):
        # initialize
        st.write("Initializing model parameters at server side and workers...")
        requests.post(self.endpoint + '/initialize', json=self.json_req)
        time.sleep(1.5)
        st.write("Executing training...")

        # train
        requests.post(self.endpoint + '/train', json={})

        # wait for results
        new_model = None
        maxtime = time.time() + TIMEOUT_SECONDS
        st.write("Waiting for results... :hourglass_flowing_sand:")
        finished = False
        while time.time() < maxtime and not finished:
            time.sleep(1)
            resp = requests.post(self.endpoint + '/model', json={})
            # FIXME: the way we handle status at server side is not good! But I
            # couldn't reach '/status'
            if resp.status_code == 425:
                logger.debug("Waiting for results... status_code: %s", resp.status_code)
            else:
                finished = True
                new_model = resp.json()
                st.write("Training done! :white_check_mark:")
            time.sleep(1)

        if not finished:
            st.write("Training did not finish in time :x:")
        else:
            logger.info("model: %s", json.dumps(new_model, indent=4))

        self.model = new_model

    def save_model(self):
        did_save = False

        if self.model is None:
            raise Exception("No new model to save")

        # check if there's already a model in the model_path
        if not self.model_path.exists() or self.overwrite_accepted():
            json.dump(self.model, open(self.model_path, "w"))
            did_save = True
        else:
            logger.info("A model already existed, and overwritting was deemed not safe. Model not saved.")

        return did_save

    @abstractmethod
    def overwrite_accepted(self):
        return False

    def get_model(self):
        # open the current model file and return it
        return json.load(open(self.model_path, "r"))

    def get_model_bytes(self):
        return open(self.model_path, "rb").read()

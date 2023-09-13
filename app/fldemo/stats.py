from fldemo.basealgo import BaseAlgo
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class StatsAlgo(BaseAlgo):
    def __init__(self, endpoint, overwrite=False, model_path=None, file_key=None, workers=None, cutoff=None, delta=None):
        super().__init__("stats", endpoint, model_path, overwrite, file_key, workers)
        # TODO: not the place to do this...
        # if super()__init__() got path to a model, we can read and get some params from there
        cur_model = None
        if self.model_path is not None:
            cur_model = self.get_model()
        if cur_model is not None:
            if cutoff is None:
                self.cutoff = cur_model['cutoff']
            if delta is None:
                self.delta = cur_model['delta']


    def overwrite_accepted(self):
        if len(self.model["results"]) < len(self.get_model()["results"]) and not self.do_overwrite:
            return False
        else:
            return True

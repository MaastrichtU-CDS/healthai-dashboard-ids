from fldemo.basealgo import BaseAlgo
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class KmeansAlgo(BaseAlgo):
    def __init__(self, endpoint, overwrite=False, model_path=None, file_key=None, workers=None, k=None, centroids=None, columns=None, epsilon=None, max_iter=None):
        super().__init__("kmeans", endpoint, model_path, overwrite, file_key, workers)
        # TODO: not the place to do this...
        # if super()__init__() got path to a model, we can read and get some params from there
        self.k = k
        self.centroids = centroids
        self.columns = columns
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.json_req['k'] = k
        self.json_req['centroids'] = centroids
        self.json_req['columns'] = columns
        self.json_req['epsilon'] = epsilon
        self.json_req['max_iter'] = max_iter


    def overwrite_accepted(self):
        # TODO
        if len(self.model) == 0:
            return False
        else:
            return True

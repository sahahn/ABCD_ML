import os
import tempfile
import numpy as np
from ...helpers.Data_File import Data_File
from ...main.Params_Classes import Problem_Spec
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection._base import SelectorMixin
from ...main.Params_Classes import Param_Search
from ...main.CV import BPtCV, CV_Strategy
from ...dataset.Dataset import Dataset


class ToFixedTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, to, n_jobs=1):
        self.to = to
        self.n_jobs = n_jobs

    def fit(self, X, y):
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X_trans = np.zeros(X.shape)
        X_trans[:] = self.to
        return X_trans


class FakeSelector(SelectorMixin, BaseEstimator):

    def __init__(self, mask):
        self.mask = mask

    def fit(self, X, y):
        return self

    def _get_support_mask(self):
        return self.mask


def get_param_search():

    param_search = Param_Search(search_type='RandomSearch',
                                cv='default',
                                n_iter=10,
                                scorer='default',
                                weight_scorer=False,
                                mp_context='loky',
                                n_jobs='default',
                                dask_ip=None,
                                memmap_X=False,
                                search_only_params=None,
                                progress_loc=None)

    ps = Problem_Spec(random_state=1,
                      n_jobs=2,
                      problem_type='regression')

    ps_dict = param_search.as_dict(ps)
    ps_dict['cv'] = BPtCV(splits=3, n_repeats=1,
                          cv_strategy=CV_Strategy(), splits_vals=None)

    return ps_dict


def get_temp_files(n):

    temp_dr = tempfile.gettempdir()
    return [os.path.join(temp_dr, 'test_' + str(i) + '.npy') for i in range(n)]


def get_fake_mapping(n):

    locs = get_temp_files(n)

    mapping = {}
    for i, loc in enumerate(locs):
        data = np.zeros((2, 2))
        data[:] = i

        np.save(loc, data)

        mapping[i] = Data_File(loc=loc, load_func=np.load)

    return mapping


def clean_fake_mapping(n):

    locs = get_temp_files(n)
    for loc in locs:
        os.unlink(loc)


def get_fake_data_dataset(data_keys=None,
                          cat_keys=None):

    if data_keys is None:
        data_keys = []

    if cat_keys is None:
        cat_keys = []

    dataset = Dataset()

    for key in data_keys:
        dataset[key] = []
        dataset.set_role(key, 'data')

    for key in cat_keys:
        dataset[key] = []
        dataset.set_role(key, 'data')
        dataset.add_scope(key, 'category')

    dataset._check_scopes()

    return dataset

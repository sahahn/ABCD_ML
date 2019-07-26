"""
Default_Params.py
====================================
File with different saved default parameter grids,
for various classifiers within ABCD_ML.
"""

from scipy.stats import (randint as sp_randint, uniform as sp_uniform)
from sklearn.feature_selection import f_regression, f_classif

PARAMS = {}

# Models
PARAMS['base logistic'] = {'solver': ['saga'],
                           'max_iter': [5000],
                           'multi_class': ['auto'],
                           'penalty': ['none']}

PARAMS['base lasso'] = PARAMS['base logistic'].copy()
PARAMS['base lasso']['penalty'] = ['l1']

PARAMS['base ridge'] = PARAMS['base logistic'].copy()
PARAMS['base ridge']['penalty'] = ['l2']

PARAMS['base elastic'] = PARAMS['base logistic'].copy()
PARAMS['base elastic']['penalty'] = ['elasticnet']
PARAMS['base elastic']['l1_ratio'] = [.5]

PARAMS['lasso C'] = PARAMS['base lasso'].copy()
PARAMS['lasso C']['C'] = sp_uniform(loc=1e-4, scale=1e+4)

PARAMS['ridge C'] = PARAMS['base ridge'].copy()
PARAMS['ridge C']['C'] = sp_uniform(loc=1e-4, scale=1e+4)

PARAMS['elastic classifier'] = PARAMS['base elastic'].copy()
PARAMS['elastic classifier']['C'] = sp_uniform(loc=1e-4, scale=1e+4)
PARAMS['elastic classifier']['l1_ratio'] = sp_uniform()

PARAMS['base elastic net'] = {'max_iter': [5000]}
PARAMS['elastic regression'] = PARAMS['base elastic net'].copy()
PARAMS['elastic regression']['alpha'] = sp_uniform(loc=1e-4, scale=1e+4)
PARAMS['elastic regression']['l1_ratio'] = sp_uniform()

PARAMS['base huber'] = {'epsilon': [1.35]}
PARAMS['base gnb'] = {'var_smoothing': [1e-9]}

PARAMS['base knn'] = {'n_neighbors': [5]}
PARAMS['knn rs'] = {'weights': ['uniform', 'distance'],
                    'n_neighbors': sp_randint(2, 20)}

PARAMS['base dt'] = {}
PARAMS['dt rs'] = {'max_depth': sp_randint(1, 20),
                   'min_samples_split': sp_randint(2, 50)}

PARAMS['base linear'] = {'fit_intercept': [True]}

PARAMS['base rf'] = {'n_estimators': [100]}
PARAMS['rf rs'] = {'n_estimators': sp_randint(3, 500),
                   'max_depth': sp_randint(2, 200),
                   'max_features': sp_uniform(),
                   'min_samples_split': sp_uniform(),
                   'bootstrap': [True]}

PARAMS['base lgbm'] = {'silent': [True]}
PARAMS['lgbm rs'] = {'silent': [True],
                     'boosting_type': ['gbdt', 'dart', 'goss'],
                     'n_estimators': sp_randint(3, 500),
                     'num_leaves': sp_randint(6, 50),
                     'min_child_samples': sp_randint(100, 500),
                     'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1,
                                          1e2, 1e3, 1e4],
                     'subsample': sp_uniform(loc=0.2, scale=0.8),
                     'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
                     'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
                     'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]}

PARAMS['base gp regressor'] = {'n_restarts_optimizer': [5],
                               'normalize_y': [True]}
PARAMS['base gp classifier'] = {'n_restarts_optimizer': [5]}


PARAMS['base svm'] = {'kernel': ['rbf'],
                      'gamma': ['scale']}

PARAMS['svm rs'] = PARAMS['base svm'].copy()
PARAMS['svm rs']['C'] = [.0001, .001, .10, .1, 1, 5, 10, 25, 50, 100, 500,
                         1000, 5000, 10000]
PARAMS['svm rs']['gamma'] = ['auto', 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]

# Scalers
PARAMS['base standard'] = {'with_mean': [True],
                           'with_std': [True]}

PARAMS['base minmax'] = {'feature_range': [(0, 1)]}

PARAMS['base robust'] = {'quantile_range': [(5, 95)]}

PARAMS['base power'] = {'method': ['yeo-johnson'],
                        'standardize': [True]}

PARAMS['base pca'] = {}

# Feat Selectors
PARAMS['base univar fs regression'] = {'score_func': [f_regression],
                                       'percentile': [50]}

PARAMS['base univar fs classifier'] = {'score_func': [f_classif],
                                       'percentile': [50]}


def get(str_indicator, preprend):

        params = PARAMS[str_indicator].copy()
        params = {preprend + '__' + key: params[key] for key in params}

        return params


def show(str_indicator):

        params = PARAMS[str_indicator].copy()

        if len(params) == 0:
                print('None')

        for key in params:
                print(key, ': ', sep='', end='')

                value = params[key]

                # If either rand int or uniform dist
                if 'scipy' in str(type(value)):

                        # Randint distr
                        if isinstance(value.a, int):
                                print('Random Integer Distribution (',
                                      value.a, ', ', value.b, ')', sep='')

                        else:
                                print('Random Uniform Distribution',
                                      value.interval(1))

                elif len(value) == 1:
                        if callable(value[0]):
                                print(value[0].__name__)
                        else:
                                print(value[0])

                else:
                        print(value)









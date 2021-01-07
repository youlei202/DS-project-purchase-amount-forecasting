from typing import Optional, List, Dict, Any

import numpy as np
import pandas as pd

from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation as prophet_cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import add_changepoints_to_plot

from sklearn.model_selection import ParameterGrid
from scipy.signal import find_peaks, argrelextrema


class ForecastingModel(object):

    MODEL_PARAMS_GRID = {'growth_model': ['linear'],
                        'seasonality_mode': ['multiplicative'],
                        'changepoint_prior_scale':  [0.4],
                        'yearly_seasonality_prior_scale':  [0.1],
                        'yearly_fourier_order': [4],
                        }


    def __init__(self):
        pass


    def _get_changepoints(self, df: pd.DataFrame):
        peaks = argrelextrema(np.array(df['y'].dropna()), np.greater)
        valleys = argrelextrema(np.array(df['y'].dropna()), np.less)
        changepoints = sorted(list(set(df['ds'].loc[peaks].dt.strftime('%Y-%m-%d').tolist() + df['ds'].loc[valleys].dt.strftime('%Y-%m-%d').tolist())))

        return changepoints


    def _fit_model(self, df: pd.DataFrame, model_params: Dict[str, List[Any]]):
        """Fits Prophet model.

        Args:
            df (pandas DataFrame): training data
            model_params (dict): dictionary of model hyperparameters
        """

        m = Prophet(
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    growth=model_params['growth_model'],
                    seasonality_mode=model_params['seasonality_mode'],
                    changepoints=model_params['changepoints'],
                    changepoint_prior_scale=model_params['changepoint_prior_scale'],
        )

        # Add bi-yearly seasonality
        m.add_seasonality(name='bi-yearly', period=365*2, fourier_order=model_params['yearly_fourier_order'],
                            prior_scale=model_params['yearly_seasonality_prior_scale'],
                            mode=model_params['seasonality_mode'])

        m.fit(df);

        return m


    def _train_model(self, train: pd.DataFrame, model_params: Dict[str, Any]):
        """Training Prophet model with given parameters

        Args:
            df (pandas DataFrame): training data
        """

        # fit model
        model = self._fit_model(train, model_params)

        # cross validation
        df_cv = prophet_cross_validation(model, period='180 days', horizon='365 days')
        df_perform = performance_metrics(df_cv)
        cv_results = df_perform[['mse', 'rmse', 'mae', 'mape']].mean().to_dict()

        return cv_results, model


    def fit(self, df: pd.DataFrame, model_params_grid: Optional[Dict[str, Any]]=MODEL_PARAMS_GRID, metric='mape'):
        """Grid search over a set of hyperparametsrs

        Args:
            df (pandas DataFrame): training data
            model_params_grid (dict, optional): dictionary of hyperparameters grid
        """

        # get changepoints
        model_params_grid['changepoints'] = [self._get_changepoints(df)]

        # convert parametergrid to list, and then traverse the list for grid search
        params_list = list(ParameterGrid(model_params_grid))
        training_results = pd.DataFrame()
        for i, params_set in enumerate(params_list):
            print(f'Iteration {i+1} out of {len(params_list)}')
            print(f'Fitting with parameter set: \n{params_set}')
            cv_results, model = self._train_model(df, params_set)
            training_results = training_results.append({'params_set': params_set, 'cv_results': cv_results}, ignore_index=True)
        training_results = training_results.reset_index(drop=True)

        # getting the best hyperparameter settings from the grid search results
        best_i = 0
        best_params_set = training_results.loc[best_i]['params_set']
        minimum_error = training_results.loc[best_i]['cv_results'][metric]
        for i in range(training_results.shape[best_i]):
            row = training_results.loc[i]
            cv_results = row['cv_results']
            params_set = row['params_set']
            if minimum_error > cv_results[metric]:
                minimum_error = cv_results[metric]
                best_params_set = params_set
                best_i = i

        # refit the model
        print(f'Fitting with best parameter set: \n{best_params_set}')
        _, model = self._train_model(df, best_params_set)

        return training_results.loc[best_i], best_params_set, model

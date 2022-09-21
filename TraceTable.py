import pandas as pd
import plotly.graph_objects as go
import numpy as np



class TraceTable:

    def __init__(self):
        self.__params = []
        self.__functions = {}
        self.__df = pd.DataFrame()

    def add_param(self, *keys):
        for key in keys:
            self.__params.append(key)

    def add_function(self, key, param_keys, func):
        self.__functions[key] = [func, param_keys]

    def build_table(self, matrix):
        self.__df = pd.DataFrame()

        for row in matrix:
            new_row = {}
            for col, key in zip(row, self.__params):
                new_row[key] = [col]
            for key, value in self.__functions.items():
                try:
                    new_row[key] = [value[0](*[new_row[i][0] for i in value[1]])]
                except BaseException as err:
                    print(err.args)
                    new_row[key] = [np.NaN]
            new_df = pd.DataFrame(new_row)
            self.__df = pd.concat([self.__df, new_df], ignore_index=True)

    def build_fig(self, x_key, y_key):
        fig = go.Figure()
        fig.update_xaxes(title=x_key)
        fig.update_yaxes(title=y_key)

        fig.add_trace(go.Scatter(x=self.__df[x_key], y=self.__df[y_key]))
        return fig

    def display(self):
        return self.__df

    def __repr__(self):
        return str(self.__df)

    def __str__(self):
        return str(self.__df)
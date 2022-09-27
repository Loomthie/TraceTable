import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    def build_fig(self, x=None, y=None):
        fig = go.Figure()
        if x is not None and y is not None:

            if type(x) == str and type(y) == str:
                fig = go.Figure()
                fig.update_xaxes(title=x)
                fig.update_yaxes(title=y)

                fig.add_trace(go.Scatter(x=self.__df[x], y=self.__df[y]))

            elif type(x) == str:
                fig = make_subplots(rows=len(y),cols=1,
                                    row_titles=y,column_titles=[x])
                for row in range(len(y)):
                    fig.add_trace(go.Scatter(x=self.__df[x],y=self.__df[y[row]]),row=row+1,col=1)

            elif type(y) == str:
                fig = make_subplots(rows=1,cols=len(x),
                                    row_titles=[y],
                                    column_titles=x)
                for col in range(len(x)):
                    fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y]),row=1,col=col+1)
            else:
                fig = make_subplots(rows=len(y),cols=len(x),
                                    row_titles=y,
                                    column_titles=x)
                for row in range(len(y)):
                    for col in range(len(x)):
                        fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y[row]]),row=row+1,col=col+1)

        elif x is not None:
            if type(x) == list:
                y = [key for key in self.__df]
                fig = make_subplots(rows=len(y),cols=len(x),
                                    row_titles=y,
                                    column_titles=x)
                for row in range(len(y)):
                    for col in range(len(x)):
                        fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y[row]]),row=row+1,col=col+1)
            else:
                y = [key for key in self.__df]
                fig = make_subplots(rows=len(y),cols=1,
                                    column_titles=[x],
                                    row_titles=y)
                for row in range(len(y)):
                    fig.add_trace(go.Scatter(x=self.__df[x],y=self.__df[y[row]]),row=row+1,col=1)

        elif y is not None:
            if type(y) == list:
                x = [key for key in self.__df]
                fig = make_subplots(rows=len(y),cols=len(x),
                                    row_titles=y,
                                    column_titles=x)
                for row in range(len(y)):
                    for col in range(len(x)):
                        fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y[row]]),row=row+1,col=col+1)
            else:
                x = [key for key in self.__df]
                fig = make_subplots(rows=1,cols=len(x),
                                    row_titles=[y],
                                    column_titles=x)
                for col in range(len(x)):
                    fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y]),row=1,col=col+1)
        else:
            x = [key for key in self.__df]
            y = [key for key in self.__df]

            fig = make_subplots(rows=len(y),cols=len(x),
                                row_titles=y,
                                column_titles=x)

            for row in range(len(y)):
                for col in range(len(x)):
                    fig.add_trace(go.Scatter(x=self.__df[x[col]],y=self.__df[y[row]]),row=row+1,col=col+1)

        fig.update_layout(showlegend=False)
        return fig

    def display(self):
        return self.__df

    def __repr__(self):
        return str(self.__df)

    def __str__(self):
        return str(self.__df)
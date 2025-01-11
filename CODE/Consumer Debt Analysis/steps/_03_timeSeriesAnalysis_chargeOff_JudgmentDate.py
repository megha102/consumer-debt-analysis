from behave import *
import pandas as pd
import allure
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib
from pandas import Series
import matplotlib.pyplot as plt
from lets_plot import *
import matplotlib.dates as mdates
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_notebook, output_file
from statsmodels.tsa.statespace.sarimax import SARIMAX
from plotly.offline import plot
from IPython.display import IFrame
import plotly.graph_objs as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Global variable for the file path
file_path = 'Data Analysis/data/accounts.csv'
LetsPlot.setup_html()


@given('the consumer debt data is loaded')
def load_data(context):
    # Load the data
    context.data = pd.read_csv(file_path)
    context.data['chargeoff_date'] = pd.to_datetime(context.data['chargeoff_date'], errors='coerce')
    context.data['judgment_date'] = pd.to_datetime(context.data['judgment_date'], errors='coerce', format='%d/%m/%y')
    context.data['chargeoff_month'] = context.data['chargeoff_date'].dt.to_period('M')
    context.data['judgment_month'] = context.data['judgment_date'].dt.to_period('M')


@when('we aggregate the monthly chargeoff and judgment data')
def step_impl(context):
    context.data['days_between'] = (context.data['judgment_date'] - context.data['chargeoff_date']).dt.days
    # Aggregate the data by month for chargeoffs and judgments
    context.monthly_aggregates = context.data.groupby('chargeoff_month').agg(
        num_chargeoffs=('data_id', 'count')
    ).reset_index()
    context.monthly_aggregates2 = context.data.groupby('judgment_month').agg(
        num_judgments=('data_id', 'count')
    ).reset_index()

    context.monthly_aggregates['chargeoff_month'] = context.monthly_aggregates['chargeoff_month'].dt.to_timestamp()
    context.monthly_aggregates2['judgment_month'] = context.monthly_aggregates2['judgment_month'].dt.to_timestamp()


@when('we calculate the average days between chargeoff and judgment for "{period}"')
def step_impl(context, period):
    if period == 'pre-COVID':
        start_date, end_date = '2015-01-01', '2019-12-31'
    elif period == 'post-COVID':
        start_date, end_date = '2020-01-01', '2023-12-31'
    mask = (context.data['chargeoff_date'] >= start_date) & (context.data['chargeoff_date'] <= end_date)
    filtered_data = context.data.loc[mask]
    context.filtered_data = filtered_data
    context.time_series = filtered_data.groupby(filtered_data['chargeoff_date'].dt.to_period("M"))['days_between'].mean().dropna()


@then('plot for Isolated fields the simple time series trend for "{period}"')
def plot_isolatedFields(context, period):
    # Convert PeriodIndex to DateTimeIndex for plotting
    if isinstance(context.time_series.index, pd.PeriodIndex):
        context.time_series.index = context.time_series.index.to_timestamp()
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=context.time_series.index, y=context.time_series, mode='lines', name='Monthly Average',
                             line=dict(color='blue')))

    # Update the layout of the figure
    fig.update_layout(
        title=f'Simple {period} Trend Analysis',
        xaxis_title='Month and Year',
        yaxis_title='Average Days Between Chargeoff and Judgment',
        legend_title='Legend',
        xaxis=dict(
            tickmode='auto',
            nticks=20,
            tickangle=90
        )
    )

    # Show the plot
    fig.show()
    plotly_html_file = 'test_reports/timeSeries_01_01.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Average Days Between Chargeoff and Judgment',
                           attachment_type=allure.attachment_type.HTML)


@then('Combined Plot for the Base Analysis')
def plot_baseAnalysis(context):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the Number of Charge-offs trace
    fig.add_trace(
        go.Scatter(x=context.monthly_aggregates['chargeoff_month'],
                   y=context.monthly_aggregates['num_chargeoffs'],
                   name='Number of Charge-offs',
                   line=dict(color='red')),
        secondary_y=False,
    )

    # Add the Number of Judgments trace
    fig.add_trace(
        go.Scatter(x=context.monthly_aggregates2['judgment_month'],
                   y=context.monthly_aggregates2['num_judgments'],
                   name='Number of Judgments',
                   line=dict(color='blue')),
        secondary_y=True,
    )

    # Add a vertical grey line at the significant drop
    significant_drop_date = "2020-08-01"
    fig.add_vline(x=significant_drop_date, line_width=2, line_dash="dash", line_color="grey")

    # Add an annotation for the significant drop
    fig.add_annotation(
        x=significant_drop_date,
        y=max(context.monthly_aggregates['num_chargeoffs'].max(), context.monthly_aggregates2['num_judgments'].max()),
        text="Significant Drop",
        showarrow=True,
        arrowhead=1,
        ax=20,
        ay=-30
    )

    # Update the layout to add titles and axis labels
    fig.update_layout(
        title_text="Monthly Charge-off and Judgment Trends",
        xaxis_title="Month",
        yaxis_title="Number of Charge-offs",
        yaxis2_title="Number of Judgments",
    )

    # Update y-axis labels
    fig.update_yaxes(title_text="Number of Charge-offs", secondary_y=False)
    fig.update_yaxes(title_text="Number of Judgments", secondary_y=True)

    # Show the interactive plot
    fig.show()
    plotly_html_file = 'test_reports/timeSeries_01_02.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Monthly Charge-off and Judgment Trends', attachment_type=allure.attachment_type.HTML)


@when('perform seasonal decomposition of the data')
def decomposition1(context):
    # Perform seasonal decomposition
    context.monthly_aggregates['num_chargeoffs'].dropna(inplace=True)
    context.monthly_aggregates2['num_judgments'].dropna(inplace=True)
    # Decompose the first dataset
    context.decomposition1 = seasonal_decompose(context.monthly_aggregates['num_chargeoffs'], model='additive', period=12)
    # Decompose the second dataset
    context.decomposition2 = seasonal_decompose(context.monthly_aggregates2['num_judgments'], model='additive', period=12)


@then('plot the seasonal decomposition for "{field}"')
def decomposition1_plot(context, field):
    if field == 'num_chargeoffs':
        monthly_aggregates = context.monthly_aggregates
    else:
        monthly_aggregates = context.monthly_aggregates2

    decomposition = seasonal_decompose(monthly_aggregates[field], model='additive', period=12)

    # Create subplots for each component of the decomposition
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'))

    # Add traces for observed, trend, seasonal, and residual components
    fig.add_trace(go.Scatter(x=decomposition.observed.index, y=decomposition.observed, mode='lines', name='Observed'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=decomposition.trend.index, y=decomposition.trend, mode='lines', name='Trend'), row=2,
                  col=1)
    fig.add_trace(go.Scatter(x=decomposition.seasonal.index, y=decomposition.seasonal, mode='lines', name='Seasonal'),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=decomposition.resid.index, y=decomposition.resid, mode='lines', name='Residual'), row=4,
                  col=1)

    # Update layout
    fig.update_layout(height=800, title_text="Seasonal Decomposition")

    # Show the interactive plot
    fig.show()
    plotly_html_file = 'test_reports/timeSeries_01_03.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Seasonal Decomposition', attachment_type=allure.attachment_type.HTML)



@when('Calculate SARIMAX forecast results for "{params}"')
def forecast_sarimax(context, params):
    # Data preprocessing
    context.data['chargeoff_date'] = pd.to_datetime(context.data['chargeoff_date'], errors='coerce')
    context.data['chargeoff_month'] = context.data['chargeoff_date'].dt.to_period('M').dt.to_timestamp()
    context.monthly_aggregates = context.data.groupby('chargeoff_month').agg(
        num_chargeoffs=('data_id', 'count')).reset_index()

    # Set 'chargeoff_month' as the index
    context.monthly_aggregates.set_index('chargeoff_month', inplace=True)

    # Full range of months for reindexing
    start_period = context.monthly_aggregates.index.min()
    end_period = context.monthly_aggregates.index.max()
    full_range = pd.date_range(start=start_period, end=end_period, freq='MS')

    # Reindex and fill data
    context.monthly_aggregates = context.monthly_aggregates.reindex(full_range, fill_value=pd.NaT)
    context.monthly_aggregates['num_chargeoffs'].fillna(0, inplace=True)

    # SARIMAX Model
    order = tuple(map(int, params.split(',')))
    model = SARIMAX(context.monthly_aggregates['num_chargeoffs'],
                    order=order,
                    seasonal_order=(1, 1, 0, 12),
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    results = model.fit()
    # Forecasting
    forecast_steps = 12
    forecast = results.get_forecast(steps=forecast_steps)
    context.forecast_index = pd.date_range(start=context.monthly_aggregates.index[-1], periods=forecast_steps + 1, freq='MS')[
                     1:]
    context.forecast_mean = forecast.predicted_mean
    context.forecast_conf_int = forecast.conf_int()


@then('plot the SARIMAX forecast results')
def plot_sarimax_results(context):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Historical data trace
    fig.add_trace(go.Scatter(x=context.monthly_aggregates.index, y=context.monthly_aggregates['num_chargeoffs'],
                             name='Historical Charge-offs'), secondary_y=False)

    # Forecast data trace
    fig.add_trace(go.Scatter(x=context.forecast_index, y=context.forecast_mean, name='Forecasted Charge-offs', mode='lines+markers'),
                  secondary_y=False)

    # Confidence interval area
    fig.add_trace(
        go.Scatter(x=context.forecast_index, y=context.forecast_conf_int.iloc[:, 0], fill=None, mode='lines', line=dict(color='gray'),
                   showlegend=False), secondary_y=False)
    fig.add_trace(go.Scatter(x=context.forecast_index, y=context.forecast_conf_int.iloc[:, 1], fill='tonexty', mode='lines',
                             line=dict(color='gray'), showlegend=False), secondary_y=False)

    # Set plot layout
    fig.update_layout(title='Monthly Charge-off Forecast',
                      xaxis_title='Year',
                      yaxis_title='Number of Charge-offs',
                      legend_title='Legend',
                      hovermode="x unified")
    fig.update_yaxes(title_text="Number of Charge-offs", secondary_y=False)

    fig.show()
    plotly_html_file = 'test_reports/timeSeries_01_04.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Chow Breakpoint Test', attachment_type=allure.attachment_type.HTML)


@when('perform the Dickey-Fuller Test')
def perform_dickey_fuller_test(context):
    context.dickey_fuller_result = adfuller(context.monthly_aggregates['num_chargeoffs'].dropna())
    context.dickey_fuller_result2 = adfuller(context.monthly_aggregates2['num_judgments'].dropna())


@then('report the Dickey-Fuller Test results')
def report_dickey_fuller_results(context):
    df_output = pd.Series(context.dickey_fuller_result[:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key, value in context.dickey_fuller_result[4].items():
        df_output['Critical Value (%s)' % key] = value
    print("Dickey-Fuller Test Results for Charge-offs:")
    print(df_output)
    df_output2 = pd.Series(context.dickey_fuller_result2[:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key, value in context.dickey_fuller_result2[4].items():
        df_output2['Critical Value (%s)' % key] = value
    print("Dickey-Fuller Test Results for Judgments:")
    print(df_output2)




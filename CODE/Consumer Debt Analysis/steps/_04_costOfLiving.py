from behave import *
import pandas as pd
import allure
from lets_plot import *
from utils import chow_test
from scipy import stats
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import statsmodels.api as sm
from scipy.stats import f
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS

LetsPlot.setup_html()

#global variable for file path
file_path = 'Data Analysis/data/macroEconomiData.csv'

@given('Subset of Consumer Debt Data: Macro Economic Data is loaded')
def load_data(context):
    # Load the data
    context.macro_economic_data = pd.read_csv(file_path)
    # extract RPP
    context.rpp_data = context.macro_economic_data[
        context.macro_economic_data['factor'].str.contains('Regional price parities', case=False, na=False)]


@when('calculate RPP values')
def calculateRPP(context):
    # calculate avg RPP yearly
    context.years = [str(year) for year in range(1998, 2023)]
    context.avg_rpp_yearly = context.rpp_data[context.years].mean()
    # calculate yearly percentage changes
    context.yearly_percentage_change = context.avg_rpp_yearly.pct_change() * 100


@then('plot Average RPP and %yearly change accordingly')
def plot_avgRPP_yearlyChange(context):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Average RPP trace to the primary y-axis with a standard CSS color name
    fig.add_trace(
        go.Scatter(x=context.years, y=context.avg_rpp_yearly, name='Average RPP', marker_color='red'),
        secondary_y=False,
    )

    # Add Yearly % Change trace to the secondary y-axis with a standard CSS color name
    fig.add_trace(
        go.Scatter(x=context.years, y=context.yearly_percentage_change, name='Yearly % Change', marker_color='blue',
                   line=dict(dash='dash')),
        secondary_y=True,
    )

    # Update the layout to add titles, axis labels, and set the colors of the y-axes to match the traces
    fig.update_layout(
        title_text='Average Regional Price Parities (RPPs) and Yearly % Change',
        xaxis_title='Year'
    )

    fig.update_yaxes(title_text='<b>Average RPP</b>', secondary_y=False, color='red')
    fig.update_yaxes(title_text='<b>Yearly % Change</b>', secondary_y=True, color='blue')

    # Show the interactive plot
    fig.show()
    plotly_html_file = 'test_reports/timeSeries_02_01.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Cost of Living', attachment_type=allure.attachment_type.HTML)


@then('Perform Chow Breakpoint Test')
def chow_test_calculate(context):
    # calculate avg RPP yearly
    years = [str(year) for year in range(1998, 2023)]
    avg_rpp_yearly = context.rpp_data[years].mean()

    # avg RPP yearly as previous
    years = [str(year) for year in range(1998, 2023)]
    avg_rpp_yearly = context.macro_economic_data[years].mean()

    breakpoints = range(1, len(avg_rpp_yearly) - 1)

    # Store results
    results = []

    for bp in breakpoints:
        F, p_value = chow_test(avg_rpp_yearly, bp)
        results.append((context.years[bp], F, p_value))

    results_df = pd.DataFrame(results, columns=['Year', 'F-Statistic', 'P-Value'])
    print(results_df)

    # Create a figure with secondary y-axis setup
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add F-Statistic trace to the primary y-axis
    fig.add_trace(
        go.Scatter(x=results_df['Year'], y=results_df['F-Statistic'], name='F-Statistic', marker_color='red'),
        secondary_y=False,
    )

    # Add P-Value trace to the secondary y-axis
    fig.add_trace(
        go.Scatter(x=results_df['Year'], y=results_df['P-Value'], name='P-Value', marker_color='blue',
                   line=dict(dash='dash')),
        secondary_y=True,
    )

    # Update the layout of the figure
    fig.update_layout(
        title_text='Chow Breakpoint Test Results',
        xaxis_title='Year',
        xaxis=dict(tickmode='linear', tick0=1998, dtick=1),
        template='plotly_dark'
    )

    # Update Y-axes titles and colors
    fig.update_yaxes(title_text='<b>F-Statistic</b>', secondary_y=False, color='red')
    fig.update_yaxes(title_text='<b>P-Value</b>', secondary_y=True, color='blue')

    # Show the interactive plot
    fig.show()
    plotly_html_file = 'test_reports/timeSeries_02_02.html'
    fig.write_html(plotly_html_file)
    with allure.step('Attach Plotly plot'):
        allure.attach.file(plotly_html_file, name='Chow Breakpoint Test', attachment_type=allure.attachment_type.HTML)



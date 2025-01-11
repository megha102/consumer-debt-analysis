from behave import given, when, then
from steps.scoring_file_v_2_0_0_2 import init, run
import plotly.express as px
import pandas as pd
import allure
import webbrowser

input_path = 'utils/Classification_models/model_prediction/predictUtils/objective2/df_close_5yr_1stpay_predict.csv'
output_path = 'utils/Classification_models/model_prediction/predictUtils/objective2/results_df_close_5yr_1stpay_predict.csv'

@given('Conditional Probability | Load the pre-processed consumer data')
def load_data(context):
    context.df = pd.read_csv(input_path)
    context.input_data = {'data': context.df}


@given('Load the Model')
def step_impl(context):
    init()

@when('Run the predictions for conditional probability | AzureML Libraries')
def step_impl(context):
    context.result_predict = run(context.input_data, GlobalParameters={"method": "predict"})
    print(context.result_predict)
    context.result_prob = run(context.input_data, GlobalParameters={"method": "predict_proba"})
    print(context.result_prob)


@then('Extract the second probability for each prediction')
def step_impl(context):
    context.prob = [row[1] for row in context.result_prob['Results']]

@then('Add the predictions and probabilities to the dataframe')
def step_impl(context):
    df = context.df
    df['closed_w_max_pmt_within_5_yrs_of_min_pmt_predicted'] = context.result_predict['Results']
    df['subobj1_predicted_proba'] = context.prob
    columns = ['closed_w_max_pmt_within_5_yrs_of_min_pmt_predicted', 'subobj1_predicted_proba'] + list(df.columns[:-2])
    context.df = df[columns]

@then('Save the updated results to the output file and display the results from tableau link')
def step_impl(context):
    context.df.to_csv(output_path, index=False)
    context.output_file = output_path
    data = pd.read_csv(context.output_file)
    data_clean = data.dropna(subset=['subobj1_predicted_proba', 'region'])
    webbrowser.open('https://public.tableau.com/shared/98P836JDZ?:display_count=n&:origin=viz_share_link')
    webbrowser.open('https://public.tableau.com/app/profile/mark.chan8454/viz/shared/22SSP8HH3')
    allure.attach.file('utils/resources/classification_01.PNG', name='Actual vs Prediction',
                       attachment_type=allure.attachment_type.PNG)



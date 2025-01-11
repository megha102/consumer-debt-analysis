import webbrowser

from behave import given, when, then, step
import pandas as pd
from scoring_file_v_2_0_0 import run
import plotly.express as px
import allure

input_file = 'Data Analysis/data/df_1stpay_5yr_chargeoff_predict.csv'
output_file = 'Data Analysis/data/result.csv'

@given('Load the pre-processed consumer data')
def load_data(context):
    context.df = pd.read_csv(input_file)
    context.input_data = {'data': context.df}


@when('Predict Using the Model(AzureML Offline Libraries)')
def predict_model(context):
        result_predict = run(context.input_data, GlobalParameters={"method": "predict"})
        print(result_predict)
        result_prob = run(context.input_data, GlobalParameters={"method": "predict_proba"})
        print(result_prob)

        # Extract the second probability
        context.prob = [row[1] for row in result_prob['Results']]

        # Extract the prediction from the result dictionary
        context.df['min_payment_within_5_years_of_chargeoff_predicted'] = result_predict['Results']
        context.df['obj1_predicted_proba'] = context.prob

        # Reorder the columns
        columns = ['min_payment_within_5_years_of_chargeoff_predicted', 'obj1_predicted_proba'] + list(context.df.columns[:-2])
        context.df = context.df[columns]



@then('Save predictions to an output csv and display the results from tableau link')
def step_impl(context):
    context.df.to_csv(output_file, index=False)
    context.output_file = output_file
    data = pd.read_csv(context.output_file)
    data_clean = data.dropna(subset=['obj1_predicted_proba', 'region'])
    webbrowser.open('https://public.tableau.com/app/profile/mark.chan8454/viz/shared/22SSP8HH3')
    allure.attach.file('utils/resources/classification_01.PNG', name='Actual vs Prediction',
                       attachment_type=allure.attachment_type.PNG)
    webbrowser.open('https://public.tableau.com/shared/RC94CCTWC?:display_count=n&:origin=viz_share_link')




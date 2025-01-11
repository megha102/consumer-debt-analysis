from steps.scoring_file_v_2_0_0_2 import init, run
import pandas as pd

input_path = 'utils/Classification_models/model_prediction/predictUtils/objective2/df_close_5yr_1stpay_predict.csv'
output_path = 'utils/Classification_models/model_prediction/predictUtils/objective2/results_df_close_5yr_1stpay_predict.csv'

df = pd.read_csv(input_path)
input_data = {'data': df}

init() # Load the model
result_predict = run(input_data, GlobalParameters={"method": "predict"})
print(result_predict)
result_prob = run(input_data, GlobalParameters={"method": "predict_proba"})
print(result_prob)

# Extract the second prob
prob = [row[1] for row in result_prob['Results']]

# Extract the prediction from the result dictionary
df['closed_w_max_pmt_within_5_yrs_of_min_pmt_predicted'] = result_predict['Results']
df['subobj1_predicted_prob'] = prob
# Reorder the columns
columns = ['closed_w_max_pmt_within_5_yrs_of_min_pmt_predicted', 'subobj1_predicted_prob'] + list(df.columns[:-2])
df = df[columns]

# Save the updated DataFrame to a new CSV file
df.to_csv(output_path, index=False)
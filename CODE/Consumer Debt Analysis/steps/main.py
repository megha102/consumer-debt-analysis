from scoring_file_v_2_0_0 import init, run
import pandas as pd

input_file = 'Data Analysis/data/df_1stpay_5yr_chargeoff_predict.csv'
output_file = 'Data Analysis/data/results_df_1stpay_5yr_chargeoff_predict.csv'

df = pd.read_csv(input_file)
input_data = {'data': df}

init() # Load the model
result_predict = run(input_data, GlobalParameters={"method": "predict"})
print(result_predict)
result_prob = run(input_data, GlobalParameters={"method": "predict_proba"})
print(result_prob)

# Extract the second prob
prob = [row[1] for row in result_prob['Results']]

# Extract the prediction from the result dictionary
df['min_payment_within_5_years_of_chargeoff_predicted'] = result_predict['Results']
df['obj1_predicted_proba'] = prob
# Reorder the columns
columns = ['min_payment_within_5_years_of_chargeoff_predicted', 'obj1_predicted_proba'] + list(df.columns[:-2])
df = df[columns]

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)
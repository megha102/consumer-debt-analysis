1. Environment setup:
- Create a new environment using Conda
- Install the required dependencies
	conda env create -f conda_env_v_1_0_0.yml
- Activate the environment
	conda activate project_environment

2. Data preparation:
- Create a DataFrame that contains input data with same structure as data_sample defined in scoring_file_v_2_0_0.py
- Sample file: df_close_5yr_1stpay_predict.csv

3. Predictions:
- run main.py in the environment: python main.py
- output is results_df_close_5yr_1stpay_predict.csv

4. Visualization:
- You may join prediction output with original dataset for loading to Tableau file
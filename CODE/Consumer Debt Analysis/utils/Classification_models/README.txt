Team84 - Exploring Trends in Consumer Debt in the United States


***************************************************

1. DESCRIPTION

***************************************************
The purpose of this package is to allow user to replicate our project, which includes
a. Data cleaning
b. Classification models training on Azure Machine Learning Studio (AutoML), evaluation and model prediction
c. Time Series Analysis on Jupyter Notebook
d. Tableau visualization of the analysis


***************************************************

2. INSTALLATION

***************************************************

// b. Classification models //
Folder: Classification_models/data_preprocessing/
You will need Azure subscription to reproduce this work.

1. Create and go to your workspace on Azure Machine Learning Studio
2. Go to Notebook, upload consumer_debt_classification_preprocessing.ipynb
3. Go to Designer, create a new pipeline, then create a new data set named account_df in Tabular type from local files by uploading account_cleaned.csv (a 1% sample dataset is included)
4. Go to Data, locate account_df, click Consume, copy the below details
subscription_id = 'xxxxxx'
resource_group = 'xxxxxx'
workspace_name = 'xxxxx'
5. Go to Notebook, locate consumer_debt_classification_preprocessing.ipynb, paste the copied details to line 6-8
6. Create a new Compute if you do not already have one


***************************************************

3. EXECUTION

***************************************************


// b. Classification models //
---------------------------------------------------

                 data_preprocessing

---------------------------------------------------
0. Go to your workspace on Azure Machine Learning Studio
1. Go to Notebook, run all cells in consumer_debt_classification_preprocessing.ipynb notebook
2. Go to Data, Datastores, workspaceblobstore (Default), Browse, Datasets
The below files should be available
- preprocessed_account_df.csv
- df_1stpay_5yr_chargeoff.csv
- df_close_5yr_1stpay.csv
- df_1stpay_5yr_chargeoff_train.csv
- df_1stpay_5yr_chargeoff_predict.csv
- df_close_5yr_1stpay_train.csv
- df_close_5yr_1stpay_predict.csv
3. Download all files locally to /model_training except
   - Download below file locally to /model_prediction/obj1training40
	- df_1stpay_5yr_chargeoff_predict.csv
   - Download below file locally to /model_prediction/subobj1training40
	- df_close_5yr_1stpay_predict.csv

---------------------------------------------------

                 model_training

---------------------------------------------------
Folder: Classification_models/model_training/

0. Go to your workspace on Azure Machine Learning Studio
1. Go to Designer, create a new pipeline, then create new data sets in Tabular type from Azure storage workspaceblobstore/datasets/ or locally
- named df_1stpay_5yr_chargeoff_train from df_1stpay_5yr_chargeoff_train.csv
- named df_close_5yr_1stpay_train from df_close_5yr_1stpay_train.csv
- This should have created 2 new dataset under Data
2. Go to Automated ML, New Autmoated ML job, we need to run 2 jobs
- Job & ExperimentName: obj1 / subobj1
- Task Type: Classfication
- Data: df_1stpay_5yr_chargeoff_train / df_close_5yr_1stpay_train
- Target column: min_payment_within_5_years_of_chargeoff / closed_w_max_pmt_within_5_yrs_of_min_pmt
- View additional configuration settings: Enable emsemble stacking 
- Test data: Train-test split: 20%
3. When the jobs finish running, under each experiment:
- Go to Models + child jobs, select the best Algorithm 
- Under Model, click Download. This will download the zip file with the model
- Extract and reename the zip files to obj1training40 / subobj1training40 and put them under Classification_models/model_prediction

---------------------------------------------------

                 model_evaluation

---------------------------------------------------
Folder: Classification_models/model_evaluation/

0. Go to your workspace on Azure Machine Learning Studio
1. Go to Automated ML, we want to extract feature importance for both obj1/ subobj1 so go to both experiments respectively
2. Go to Models + child jobs, select the best Algorithm 
3. Click Explain model and run the job
4. When the job is completed, go to Explanations. The Explanations selected should be the lastest one.
5. On the chart with Aggregate feature importance, click on the hamburger icon -> Download csv
6. Rename the file to obj1-feature-importance.csv /  subobj1-feature-importance.csv respectively and save to /model_evaluation


---------------------------------------------------

                 model_prediction

---------------------------------------------------
Folder: Classification_models/model_prediction/obj1training40/

This part can be performed locally. The models are extracted based on full dataset training. sample prediction input are also from full dataset.

1. Environment setup:
- Create a new environment using Conda
- Install the required dependencies
	conda env create -f conda_env_v_1_0_0.yml
- Activate the environment
	conda activate project_environment

2. Data preparation:
- Create a DataFrame that contains input data with same structure as data_sample defined in scoring_file_v_2_0_0.py
- Sample file: df_1stpay_5yr_chargeoff_predict.csv

3. Predictions:
- run main.py using the command: python main.py
- output is results_df_1stpay_5yr_chargeoff_predict.csv

4. Visualization:
- Join prediction output (prediction and prob) with original dataset preprocessed_account_df.csv and rename to df_all.csv
- This df_all.csv can be used to refresh Connection of Data Source of Tableau file

....................................................
Folder: Classification_models/model_prediction/subobj1training40/

This part can be performed locally.

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
- run main.py using the command: python main.py
- output is results_df_close_5yr_1stpay_predict.csv

4. Visualization:
- Join prediction output (prediction and prob) with original dataset /model_training/preprocessed_account_df.csv and rename to df_all.csv
- This df_all.csv can be used to refresh Connection of Data Source of Tableau file




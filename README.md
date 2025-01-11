![image](https://github.com/user-attachments/assets/50d8f698-4304-4c97-9c18-43e2958582e0)


We have tried to analyze the consumer debt data in the US. The project is comprised of following objectives-(mapped with the respective code file names)
### 1) Classification Model
-> For Predicting the probability of a consumer beginning repayment within 5 years of charge off based on a set of features. | _01_classification_model_chargeOff_predict_1st_repay.feature
-> For Predicting in case of conditional probability that given a consumer has initiated first payment, what is the chance of account paid or settled in full within 5 years | _02_classification_model_conditionProb_chargeOff_predict_1st_repay.feature

### 2) Time Series Analysis 
-> Analysing trends pre-post covide for average between chargeOff and judgment date and then tried forecasting for chargeoff dates. | _03_chargeOff_JudgmentDate.feature
-> Analysing trends for cost of living using RPP, did Structural breakpoint analysis taking breakpoint year=2008. | _04_costOfLiving.feature

### 3) Tableau Visualization
-> Created a UI for classification model visualization both parts which includes
i) feature comparison
ii) Actual vs Predicted Values
iii) Geographical Mapping
-> Trend Analysis - Pre and Post COVID
i) Average between charge off and judgment date
ii) charge off and min pay date(first repayment date)
iii) Averge between pay across US regions
iv) Macro Economic Factors.



The project is tried and tested on windows(there were some errors for AzureML Libraries on M1 and M2 due to silicon architecture)

# INSTALLATION

1) Download Python: https://www.python.org/downloads/ 
2) Add Path to environment variables
	i) Open cmd 
	ii) Type command: rundll32 sysdm.cpl, EditEnviornmentVariables
	iii) Edit Path and add the address for python installation, it would look something like: C:\Users\meggulat\AppData\Local\Programs\Python\Python311
	iv) click on Ok and close the cmd.
	v) verify the installation by reopening the cmd and type:  python --version. 
3) Download Anaconda: Installer given in README folder.
	i) Add to Path in Environment Variables for example : C:\Users\meggulat\AppData\Local\anaconda3
	ii) Verify installation in cmd by typing: conda --version  
4) Download Allure: https://github.com/allure-framework/allure2/releases [Assets-> allure-2.28.0.zip]
	i) Extract the folder and follow the installation steps.
	ii) Add the bin folder to the Path in Environment Variables, for example: C:\Users\meggulat\Downloads\allure-2.28.0\allure-2.28.0\bin
	iii) Verify installation in cmd by typing: allure --version
5) Open cmd and go to project path and Go to Path: {User Directory}\Consumer Debt Analysis\envs>
6) Type command: conda env create -f env.yml[This process will take some time since it downloads all the required libraries and created a conda environment]
7) Type command: conda activate proj_env
	
	[The project can be run in CMD now]
	
### METHOD 2[PYCHARM] - Preferred for detailed view of all the modules and running all the scenarios separately.
7) Download PyCharm IDE: https://www.jetbrains.com/pycharm/download/?section=windows [Community Edition is free]
8) Open the project in PyCharm IDE
9) Wait for the dependencies to install
10) Go to Terminal which is inbuilt in Pycharm: Type in command: conda activate proj_env
11) If above command does not run, go to File | Settings | Project: <project name> | Python Interpreter | Add Interpreter | Add Local Interpreter | Conda Environment | {User Directory where anaconda3 saved}\anaconda3\Scripts\conda.exe | Load Environments
12) The list should load all the environments created by conda - click on projEnv
13) Wait for Updating Skeletons, Indexing.


# EXECUTION
Method 1: CMD 

1) Open CMD and go to Project Path, for example: C:\Users\meggulat\Documents\team084final\CODE\Consumer Debt Analysis
2) Assuming, conda env is activated as mentioned in Installation steps
3) Type in command: behave -f allure_behave.formatter:AllureFormatter -o test_reports/ features [Wait for 20-30 seconds for it to run]
4) It will start running, some results in CMD -> ignore the duplicate error.
5) Multiple browser windows will start opening up which are the result to all the scenarios running at once.
6) To view a consolidated run report. Type in command: allure serve test_reports
7) An Interactive report will be generated and opened in a Web Browser.

### METHOD 2: PYCHARM

The code is run from the feature files present in features folder. 
C:\Users\meggulat\Documents\team084final\CODE\Consumer Debt Analysis\features

1) Run _01_classification_model_chargeOff_predict_1st_repay.feature
Possible Env/Intermittent error(from AzureML Library) :
Fix: schema_decorators.py -> edit mode -> if OUTPUT_SCHEMA_ATTR in __functions_schema__[base_func_name].keys():
        print('Error, output schema already defined for function: {}.'.format(base_func_name))

2) Run _02_classification_model_conditionProb_chargeOff_predict_1st_repay
ii) Run features/_02_classification_model_conditionProb_chargeOff_predict_1st_repay.feature
Possible Env/Intermittent error(from AzureML Library) :
Fix: schema_decorators.py -> edit mode -> if OUTPUT_SCHEMA_ATTR in __functions_schema__[base_func_name].keys():
        print('Error, output schema already defined for function: {}.'.format(base_func_name))

Run each scenario one by one for  better clarity in below-
3) Run _03_chargeOff_JudgmentDate.feature | Time Series Analysis
4) Run _04_costOfLiving.feature | Time Series Analysis
5) Run _05_tableau_visualization.feature | Tableau Visualization Published to Public Tableau



Feature: Classification Model when conditional probability that given a customer has initiated first payment,
  what is the chance of account paid or settled in full within 5 years.
  We used AzureML to predict from data using different models and saving the output to a csv file.


  Scenario: Predicting the probability of account paid or settled in full within 5 years
    Given Conditional Probability | Load the pre-processed consumer data
    Given Load the Model
    When Run the predictions for conditional probability | AzureML Libraries
    Then Extract the second probability for each prediction
    Then Add the predictions and probabilities to the dataframe
    Then Save the updated results to the output file and display the results from tableau link


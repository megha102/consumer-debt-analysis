Feature: Classification Model for predicting the probability of a consumer beginning repayment within 5 years of charge-off based on a set of features.
  We used AzureML to predict from data using different models and saving the output to a csv file.

  Scenario: Predicting payment within 5 years of chargeoff
    Given Load the Data
    When I predict using the model
    Then Save predictions to an output csv and display basic plot


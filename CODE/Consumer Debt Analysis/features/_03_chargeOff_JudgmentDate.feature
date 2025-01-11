Feature: Time Series Analysis of Consumer Debt Objective 1 (ChargeOff Date and Judgment Date)
  We want to analyze the consumer debt data while examining the average in days between chargeoff and judgment dates being acquired
  to understand the trends in chargeoff and judgment dates before and after COVID-19.

  Background:
    Given the consumer debt data is loaded
    When we aggregate the monthly chargeoff and judgment data

    Scenario Outline: Analyze debt data trends Pre and Post COVID 19 - Basic Time Series Analysis
    When we calculate the average days between chargeoff and judgment for "<period>"
    Then plot for Isolated fields the simple time series trend for "<period>"
    Examples:
      | period    |
      | pre-COVID |
      | post-COVID|


  Scenario: Combined Basic Time Series Analysis
    When we aggregate the monthly chargeoff and judgment data
    Then Combined Plot for the Base Analysis


  Scenario Outline: Advanced Time Series Analysis with Seasonal Decomposition
    When perform seasonal decomposition of the data
    Then plot the seasonal decomposition for "<field>"
    Examples:
    |field|
    |num_chargeoffs|
    |num_judgments |


  Scenario Outline: Forecast Monthly Charge-offs using SARIMAX
    When Calculate SARIMAX forecast results for "<params>"
    Then plot the SARIMAX forecast results
    Examples:
    |params|
    |1,1,1 |
    |1,1,0 |
    |1,0,0 |


  Scenario: Perform Dickey-Fuller Test to check data stationarity
    When perform the Dickey-Fuller Test
    Then report the Dickey-Fuller Test results



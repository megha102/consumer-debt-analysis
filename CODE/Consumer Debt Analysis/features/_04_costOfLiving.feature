Feature: To conduct a detailed time series analysis on the cost of living indices using Regional Price Parities (RPPs) as a proxy.
  Breaking down the process below-
  1) Base Time Series Analysis - To see the combined plot of Average RPP and yearly % change from the data.
  2) Structural Break Analysis - To detect any potential breakpoints in the RPPs time series, which may indicate significant
  shifts in the cost of living due to events like the 2008 financial crisis or the onset of the COVID-19 pandemic

   Background:
    Given Subset of Consumer Debt Data: Macro Economic Data is loaded
     When calculate RPP values

  Scenario: Base Analysis for Average Regional Price Parities (RPPs) and Yearly % Change
    Then plot Average RPP and %yearly change accordingly

  Scenario: Structural Break Analysis
    Then Perform Chow Breakpoint Test




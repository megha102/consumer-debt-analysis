Feature: Interactive Visualization done via Tableau for -
  1) Classification Models developed with Azure ML
  2) Pre-Post Covid Trends_01: chargeoff and judgment date.
  3) Pre-Post Covid Trends_02: chargeoff and min payment date(first repayment date).
  4) Pre-Post Covid Trends_03: avg number of days between payments across US regions.
  5) Pre-Post Covid Trends_04: Variation in macro economic factors for regions across US


  Scenario: Exploring Consumer Debt in the US with Classification Models
    Given Classification Models | The URL of the Tableau Public dashboard
    Then Classification Models | Navigate to the Tableau Public URL


  Scenario: Average number of days between chargeoff and judgement date across US states pre and post covid.
    Given Pre-Post Covid Trends_01 - URL of the Tableau Public dashboard
    Then Pre-Post Covid Trends_01 - Navigate to Tableau Public URL


  Scenario: Average number of days between chargeoff and min payment (first payment) date across US states pre and post covid.
    Given Pre-Post Covid Trends_02 - URL of the Tableau Public dashboard
    Then Pre-Post Covid Trends_02 - Navigate to Tableau Public URL


  Scenario: Average of avg number of days between payments across US regions pre and post covid.
    Given Pre-Post Covid Trends_03 - URL of the Tableau Public dashboard
    Then Pre-Post Covid Trends_03 - Navigate to Tableau Public URL


  Scenario: Variation in macro economic factors for regions across US pre and post covid.
    Given Pre-Post Covid Trends_04 - URL of the Tableau Public dashboard
    Then Pre-Post Covid Trends_04 - Navigate to Tableau Public URL



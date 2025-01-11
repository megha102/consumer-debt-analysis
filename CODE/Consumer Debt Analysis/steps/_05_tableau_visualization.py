from behave import given, when, then
import selenium.webdriver
import webbrowser
import allure

@given('Classification Models | The URL of the Tableau Public dashboard')
def step_impl(context):
    context.url = "https://public.tableau.com/app/profile/mark.chan8454/viz/consumer_debt_classification_modelsv3/Story1"


@then('Classification Models | Navigate to the Tableau Public URL')
def step_impl(context):
    webbrowser.open(context.url)


@given('Pre-Post Covid Trends_01 - URL of the Tableau Public dashboard')
def step_impl(context):
    context.url = "https://public.tableau.com/app/profile/megha.gulati/viz/Pre-PostCovidTrends/Chargeoff_Judgement?publish=yes"


@then('Pre-Post Covid Trends_01 - Navigate to Tableau Public URL')
def step_impl(context):
    webbrowser.open(context.url)
    allure.attach.file('utils/resources/tableau_02.PNG', name='pre_post_covid_trends',
                       attachment_type=allure.attachment_type.PNG)


@given('Pre-Post Covid Trends_02 - URL of the Tableau Public dashboard')
def step_impl(context):
    context.url = "https://public.tableau.com/app/profile/megha.gulati/viz/Chargeoff_minPay_Pre-PostCovidTrends/Chargeoff_minPay?publish=yes"


@then('Pre-Post Covid Trends_02 - Navigate to Tableau Public URL')
def step_impl(context):
    webbrowser.open(context.url)
    allure.attach.file('utils/resources/tableau_03.PNG', name='Avg_between_pay_pre_post_covid_trends',
                       attachment_type=allure.attachment_type.PNG)

@given('Pre-Post Covid Trends_03 - URL of the Tableau Public dashboard')
def step_impl(context):
    context.url = "https://public.tableau.com/app/profile/megha.gulati/viz/Avg_between_Pay_Pre-PostCovidTrends/Avg_between_Pay?publish=yes"


@then('Pre-Post Covid Trends_03 - Navigate to Tableau Public URL')
def step_impl(context):
    webbrowser.open(context.url)
    allure.attach.file('utils/resources/tableau_04.PNG', name='Avg_between_pay_pre_post_covid_trends',
                       attachment_type=allure.attachment_type.PNG)


@given('Pre-Post Covid Trends_04 - URL of the Tableau Public dashboard')
def step_impl(context):
    context.url = "https://public.tableau.com/app/profile/megha.gulati/viz/Macro_Eco_Factors_Pre-PostCovidTrends/Macro_Eco_Factors?publish=yes"


@then('Pre-Post Covid Trends_04 - Navigate to Tableau Public URL')
def step_impl(context):
    webbrowser.open(context.url)
    allure.attach.file('utils/resources/tableau_05.PNG', name='Avg_between_pay_pre_post_covid_trends',
                       attachment_type=allure.attachment_type.PNG)


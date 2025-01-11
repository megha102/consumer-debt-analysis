import numpy as np
import statsmodels.api as sm
from scipy.stats import f


def chow_test(timeseries, breakpoint):
    # Data before and after the breakpoint
    data_pre = timeseries[:breakpoint]
    data_post = timeseries[breakpoint:]

    # Ensure arrays for OLS fit have the correct shape
    X_full = sm.add_constant(np.arange(len(timeseries)).reshape(-1, 1))
    X_pre = sm.add_constant(np.arange(len(data_pre)).reshape(-1, 1))
    X_post = sm.add_constant(np.arange(len(data_post)).reshape(-1, 1))

    # OLS regressions
    model_full = sm.OLS(timeseries.values, X_full).fit()
    model_pre = sm.OLS(data_pre.values, X_pre).fit()
    model_post = sm.OLS(data_post.values, X_post).fit()

    # Calculate SSRs
    SSR_full = model_full.ssr
    SSR_pre = model_pre.ssr
    SSR_post = model_post.ssr

    # Calculate the F-statistic correctly
    N = len(timeseries)
    p = 2  # Assuming a simple model with intercept + slope
    F = ((SSR_full - (SSR_pre + SSR_post)) / p) / ((SSR_pre + SSR_post) / (N - 2 * p))
    p_value = f.sf(F, p, N - 2 * p)

    return F, p_value

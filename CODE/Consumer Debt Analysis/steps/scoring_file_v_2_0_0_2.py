# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType

data_sample = PandasParameterType(pd.DataFrame({"region": pd.Series(["example_value"], dtype="object"), "working_age": pd.Series([0], dtype="int8"), "purchasegroup": pd.Series(["example_value"], dtype="object"), "chargeoffamt": pd.Series([0.0], dtype="float32"), "chargeoffamt_present": pd.Series([0], dtype="int8"), "judgment_active": pd.Series([0], dtype="int8"), "acct_post_judgment": pd.Series([0], dtype="int8"), "judgment_amount": pd.Series([0.0], dtype="float32"), "judgment_amount_present": pd.Series([0], dtype="int8"), "days_between_chargeoff_and_judgment": pd.Series([0.0], dtype="float32"), "agency_ever": pd.Series([0], dtype="int8"), "legal_ever": pd.Series([0], dtype="int8"), "wage_garnishable_state": pd.Series([0], dtype="int8"), "bank_account_found": pd.Series([0], dtype="int8"), "FT_job_found": pd.Series([0], dtype="int8"), "PT_job_found": pd.Series([0], dtype="int8"), "verification_completed": pd.Series([0], dtype="int8"), "contains_judgment_image": pd.Series([0], dtype="int8"), "days_between_chargeoff_and_min_pay_date": pd.Series([0], dtype="int16"), "days_between_judgment_and_min_pay_date": pd.Series([0.0], dtype="float32"), "avg_days_between_payments": pd.Series([0.0], dtype="float32"), "avg_monthly_payment(duration>=365days)": pd.Series([0.0], dtype="float32"), "avg_pay_to_chargeoff_ratio": pd.Series([0.0], dtype="float32"), "avg_pay_to_judgment_ratio": pd.Series([0.0], dtype="float32")}))
input_sample = StandardPythonParameterType({'data': data_sample})
method_sample = StandardPythonParameterType("predict")
sample_global_params = StandardPythonParameterType({"method": method_sample})

result_sample = NumpyParameterType(np.array([0]))
output_sample = StandardPythonParameterType({'Results':result_sample})

try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script_v2')
except:
    pass


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = 'utils/Classification_models/model_prediction/predictUtils/objective2/model.pkl'
    # model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    # path = os.path.normpath(model_path)
    # path_split = path.split(os.sep)
    # log_server.update_custom_dimensions({'model_name': path_split[-3], 'model_version': path_split[-2]})
    try:
        logger.info("Loading model from path.")
        model = joblib.load(model_path)
        logger.info("Loading successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise

@input_schema('GlobalParameters', sample_global_params, convert_to_provided_type=False)
@input_schema('Inputs', input_sample)
@output_schema(output_sample)
def run(Inputs, GlobalParameters={"method": "predict"}):
    data = Inputs['data']
    if GlobalParameters.get("method", None) == "predict_proba":
        result = model.predict_proba(data)
    elif GlobalParameters.get("method", None) == "predict":
        result = model.predict(data)
    else:
        raise Exception(f"Invalid predict method argument received. GlobalParameters: {GlobalParameters}")
    if isinstance(result, pd.DataFrame):
        result = result.values
    return {'Results':result.tolist()}

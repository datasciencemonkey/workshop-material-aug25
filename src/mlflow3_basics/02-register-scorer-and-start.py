from mlflow.genai.scorers import Safety, ScorerSamplingConfig
from mlflow.genai.scorers import Guidelines
import mlflow
from mlflow.genai.scorers import scorer
from rich import print
import os
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")

load_dotenv()

# Databricks Foundation Model APIs use Databricks authentication.

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment(experiment_id=os.environ.get("MLFLOW_EXPERIMENT_ID"))

SAMPLE_RATE = 0.7

# out of the box safety scorer
safety = Safety().register(name="safety_check")
safety = safety.start(sampling_config=ScorerSamplingConfig(sample_rate=SAMPLE_RATE))
print("Safety scorer registered & Started")

# Create and register the guidelines scorer
english_scorer = Guidelines(
  name="english",
  guidelines=["The response must be in English"]
).register(name="is_english")  # name must be unique to experiment

# Start monitoring with the specified sample rate
english_scorer = english_scorer.update(sampling_config=ScorerSamplingConfig(sample_rate=SAMPLE_RATE))
print("English scorer registered & Started")

# custom scorer
@scorer
def response_length(outputs):
    return len(str(outputs.get("response", "")))

length_scorer = response_length.register(name="length_check")
length_scorer = length_scorer.start(
    sampling_config=ScorerSamplingConfig(sample_rate=SAMPLE_RATE,
    filter_string="trace.status = 'OK'"),
)

print("Length scorer registered & Started")




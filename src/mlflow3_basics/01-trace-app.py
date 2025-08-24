import mlflow
import os
from openai import OpenAI
from rich import print
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

# Databricks Foundation Model APIs use Databricks authentication.

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment(experiment_id=os.environ.get("MLFLOW_EXPERIMENT_ID"))

# Enable auto-tracing for OpenAI (which will trace Databricks Foundation Model API calls)
mlflow.openai.autolog()

# Create OpenAI client configured for Databricks
client = OpenAI(
    api_key=os.environ.get("DATABRICKS_TOKEN"),
    base_url=f"{os.environ.get('DATABRICKS_HOST')}/serving-endpoints"
)

# Query Llama 4 Maverick using OpenAI client
response = client.chat.completions.create(
    model="databricks-gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the key features of MLflow Tracing?"}
    ],
    max_tokens=150,
    temperature=0.7
)

print(response.choices[0].message.content)
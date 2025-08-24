import mlflow
import os
from fastapi import FastAPI, Request
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import warnings


warnings.filterwarnings("ignore")

load_dotenv()
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment(experiment_id=os.environ.get("MLFLOW_EXPERIMENT_ID"))
mlflow.openai.autolog()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
@mlflow.trace   # Inner decorator
def handle_chat(request: Request, chat_request: ChatRequest):
    # Retrieve all context from request headers
    client_request_id = request.headers.get("X-Request-ID")
    session_id = request.headers.get("X-Session-ID")
    user_id = request.headers.get("X-User-ID")
    
    print(f"Client request ID: {client_request_id}")
    print(f"Session ID: {session_id}")
    print(f"User ID: {user_id}")

    mlflow.update_current_trace(
        metadata={
            # Standard metadata fields for user and session tracking
            "mlflow.trace.session": session_id,
            "mlflow.trace.user": user_id,
            # Client request ID as metadata since it's immutable
            "client_request_id": client_request_id,
        }
    )

    def query_model(user_message):
        client = OpenAI(
            api_key=os.environ.get("DATABRICKS_TOKEN"),
            base_url=f"{os.environ.get('DATABRICKS_HOST')}/serving-endpoints"
        )
        
        response = client.chat.completions.create(
            model="databricks-gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Return the actual text content, not the response object
        return response.choices[0].message.content
    
    # Get the response text
    response_text = query_model(chat_request.message)
    
    # Return response
    return {
        "response": response_text
    }
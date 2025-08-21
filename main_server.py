from DocManager.chatbot_backend.chatbot_feature import ChatbotFeature, ConversationMessage
from DocManager.chatbot_backend.temp_database import TempDatabase
from model_client import get_model_client, get_small_model_client

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="DocManager Server with configurable content directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_server.py -d test
        """
    )
    
    parser.add_argument(
        "-d", "--content-dir",
        help="Path to the HTML content directory",
        required=True,
    )
    
    return parser.parse_args()

args = parse_arguments()

load_dotenv()
api_key = os.getenv("LLM_API_KEY")
api_base = os.getenv("LLM_BASE_URL")

if api_key is None or api_base is None:
    raise ValueError("LLM_API_KEY and LLM_BASE_URL must be set")

model_client = get_model_client()
small_model_client = get_small_model_client()

content_path = args.content_dir + "final.html" if args.content_dir.endswith("/") else args.content_dir + "/final.html"

temp_database = TempDatabase(
    db_path="temp_chroma_db",
    collection_name=content_path.split("/")[-2].split(".")[0],
    content_path=content_path,
    overwrite=True
)
chatbot_feature = ChatbotFeature(model_client, small_model_client, temp_database)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.post("/chat", response_model=ConversationMessage)
async def chat(request: ConversationMessage) -> ConversationMessage:
    return await chatbot_feature.chat(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)

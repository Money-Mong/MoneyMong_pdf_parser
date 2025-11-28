
import os
from langchain_upstage import ChatUpstage
from dotenv import load_dotenv

load_dotenv()

def get_upstage_llm():
    return ChatUpstage(
        api_key=os.getenv("UPSTAGE_API_KEY"),
        model_name="solar-pro2",
        temperature=0.3,
        max_tokens=1024,
    )

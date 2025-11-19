# llm/upstage_summary.py
import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage

load_dotenv()

def get_summary_llm():
    return ChatUpstage(
        api_key=os.getenv("UPSTAGE_API_KEY"),
        model_name="solar-pro2",         
        temperature=0.3,
        max_tokens=1024
    )

import openai
import pinecone


def load_env():
    """Loads the environment variables from the .env file and sets up api keys if needed"""
    from dotenv import load_dotenv
    load_dotenv()
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))

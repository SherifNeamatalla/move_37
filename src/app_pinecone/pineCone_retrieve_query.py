limit = 3750
import openai
import os
from dotenv import load_dotenv
from pincecone_db_manager import PineCone
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def retrieve(query):

    pine = PineCone()

    res = openai.Embedding.create(
        input=[query],
        engine="text-embedding-ada-002"
    )

    # retrieve from Pinecone
    xq = res['data'][0]['embedding']

    # get relevant contexts

    index = pine.getIndex("commadIndex")
    res = pine.query(index,xq,3,True)
    contexts = [
        x['metadata']['text'] for x in res['matches']
    ]

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(1, len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )
    return prompt
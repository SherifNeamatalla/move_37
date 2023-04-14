import ssl

import nltk
from langchain.document_loaders import UnstructuredURLLoader
from langchain.indexes import VectorstoreIndexCreator

from src.config.env_loader import load_env

load_env()
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')
urls = [
    "https://github.com/yoheinakajima/babyagi",
]

loader = UnstructuredURLLoader(urls=urls)

index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query("What's the repo about?"))


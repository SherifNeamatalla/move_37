import pinecone
import os
from dotenv import load_dotenv
load_dotenv()
# pinecone.init(api_key=os.getenv("PINE_CONE_KEY"), environment=os.getenv("PINE_CONE_ENV"))

class PineCone:

    def __init__(self):
        # Initialize Pinecone with a name and vector dimension
        pinecone.init(api_key=os.getenv("PINE_CONE_KEY"), environment=os.getenv("PINE_CONE_ENV"))


    def createIndex(self,indexName,dimension):
        pinecone.create_index(indexName, dimension=dimension, metric="euclidean", pod_type="p2")

    def getIndex(self,indexName):
        return pinecone.Index(indexName)
    
    def addVectors(self,vectorArray,idx):
        idx.upsert(vectorArray)

    def getIndexStats(self,idx):
        return idx.describe_index_stats()

    def query(self,idx,vector,topK=1,meta=False,filter={}):
        return idx.query(
            vector=vector,
            top_k=topK,
            include_values=True,
            include_metadata=meta,
            filter=filter
        )
    def delete(self,idx,ids,deleteAll=False,filter=''):
        return idx.delete(ids=ids, deleteAll=deleteAll,filter=filter)

# print(pinecone.list_indexes())
# pinecone.delete_index("quickstart")

# index = pinecone.Index("quickstart")

# # Upsert sample data (5 8-dimensional vectors)
# index.upsert([
#     ("F", [0.1, 0.1, 0.1, 0.1, 0.1, 0.7, 0.8, 0.5])
# ])

# print(index.describe_index_stats())

# print(index.query(
#   vector=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.8, 0.3],
#   top_k=3,
#   include_values=True
# )
# )

# pine=PineCone()
# pine.getIndex
# pine.createIndex("quickstart",4096)
# i=pine.getIndex("quickstart")
# print(pine.getIndexStats(i))
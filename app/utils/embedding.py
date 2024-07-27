import os
import pandas as pd
import numpy as np
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config import get_settings

settings = get_settings()


client = OpenAI(api_key=settings.openai_api_key)

def get_embedding(text, model="text-embedding-3-small"):
   res = client.embeddings.create(input = text, model=model)
   x_embed = np.array([e.embedding for e in res.data])
   return x_embed

# def compute_embeddings_for_document(doc, doc_index):
#     chunks = doc.page_content
#     if len(chunks) == 0:
#         return None

#     try:
#         chunk_embeddings = get_embedding([chunks])
#     except Exception as e:
#         print(f"Error computing embeddings for document {doc_index}: {e}")
#         return None

#     # Create a DataFrame for the embeddings
#     page_df = pd.DataFrame({
#         "chunk_id": list(range(chunk_embeddings.shape[0])),
#         "chunk": chunks,
#         "embedding": chunk_embeddings.tolist(),
#         "page": f"document_{doc_index}"
#     })
    
#     return page_df

# def compute_embeddings_from_documents(documents, cache_file, max_workers=4):
#     if os.path.exists(cache_file):
#         os.remove(cache_file)

#     results = []

#     # Use ThreadPoolExecutor to process documents concurrently
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         future_to_doc_index = {executor.submit(compute_embeddings_for_document, doc, i): i for i, doc in enumerate(documents)}
#         for future in as_completed(future_to_doc_index):
#             doc_index = future_to_doc_index[future]
#             try:
#                 result = future.result()
#                 if result is not None:
#                     results.append(result)
#             except Exception as e:
#                 print(f"Error processing document {doc_index}: {e}")

#     # Write all results to the cache file
#     with open(cache_file, 'a') as f:
#         for result in results:
#             f.write(result.to_json(orient="records", lines=True))
#             f.write('\n')
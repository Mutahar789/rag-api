import os
import magic
import nltk
import queue
import threading
import time

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

import vectorstore
from load import load
from split import split
import hashlib

app = FastAPI()

origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorDB = vectorstore.milvus()
hashes = {}

@app.post("/upload/")
async def upload(user_id: int, files: List[UploadFile] = File(...)):
    successfull = []
    failed = []

    user_upload_dir = f"./uploads/{user_id}/"
    if not os.path.exists(user_upload_dir):
        os.makedirs(user_upload_dir)

    for file in files:
        try:
            file_bytes = await file.read()
            
            sha256_hash = hashlib.sha256()
            sha256_hash.update(file_bytes)
            hash_hex = sha256_hash.hexdigest()
            
            if hashes.get(user_id) == None:
                hashes[user_id] = set()

            elif hash_hex in hashes[user_id]:
                successfull.append(file.filename)
                continue

            hashes[user_id].add(hash_hex)

            filepath = user_upload_dir+file.filename
            with open(filepath, 'wb') as f:
                f.write(file_bytes)
            
            
            _, ext = os.path.splitext(file.filename)
            docs = load(user_id, filepath, ext)
            split_docs = split(docs, ext)
            vectorDB.index(split_docs)
            successfull.append(file.filename)

        except Exception:
            failed.append(file.filename)
            raise HTTPException(status_code=400)
        
        finally:
            file.file.close()

    return {"successfull": successfull, "failed": failed}   

@app.post("/search/")
async def search(user_id: int, question: str, top_k: int = 3):
    context = vectorDB.search(user_id, question, top_k)
    return {"context": context}

@app.post("/clear_docs/")
async def clear_docs(user_id: int):
    if hashes.get(user_id) != None:
        vectorDB.clear_docs(user_id)
        del hashes[user_id]
    return {"success"}

@app.post("/get_text/")
async def get_text(user_id: int, file: UploadFile = File(...)):
    try:
        timestamp = int(time.time())
        filepath = f"./temp/{timestamp}_{file.filename}"
        contents = await file.read()
        with open(filepath, 'wb') as f:
            f.write(contents)

        _, ext = os.path.splitext(file.filename)
        docs = load(user_id, filepath, ext)
        texts = [doc.page_content for doc in docs]
        txt_doc = "\n".join(texts)

    except:
        raise HTTPException(status_code=400)

    finally:
        os.remove(filepath)

    return {"text": txt_doc}


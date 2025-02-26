from datetime import datetime

import openai
from langchain.schema import Document
import config
import src.data_utils
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone

openai.api_key = config.OPEN_API_KEY

def get_pc():
    pc = Pinecone(api_key="")
    return pc


def get_openai_embedding(text: str, model="text-embedding-ada-002") -> list:
    response = openai.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def save_to_pinecone(chunks: list[Document]):
    pc = get_pc()
    index = pc.Index(name="maxent")
    data = []
    for inx in range(len(chunks)):
        print(inx)
        chunk = chunks[inx]
        metadata = chunk.metadata
        metadata["text"] = chunk.page_content
        row = dict(id=str(inx), values=get_openai_embedding(chunk.page_content), metadata=metadata)
        index.upsert([row])
        data.append(row)


def split_documents_to_chunks(documents: list[Document]):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=120,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    for inx in range(len(chunks)):
        print(inx, len(chunks[inx].page_content))
    return chunks

def main():

    container = src.data_utils.fed_speech_collection()
    result = []

    for document in container.find():

        if document["date"] <= datetime(2023, 1, 1):
            continue

        date = datetime.strftime(document["date"], "%Y-%m-%d")
        author = document["author"]
        title = document["title"]
        link = document["url"]
        text = document["full_text"]

        metadata = dict(author=author, date=date, title=title, link=link)
        doc = Document(page_content=text, metadata=metadata)
        result.append(doc)

    print(len(result))
    chunks = split_documents_to_chunks(result)
    save_to_pinecone(chunks)

if __name__ == "__main__":
    main()
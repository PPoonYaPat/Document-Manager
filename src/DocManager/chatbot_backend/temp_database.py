import chromadb
import os
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from chromadb import EmbeddingFunction

import voyageai

class VoyageEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = "voyage-context-3"):
        self.client = voyageai.Client() # default api key is in the .env file
        self.model = model

    def __call__(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.client.contextualized_embed(
            inputs = [texts],
            model = self.model,
            input_type = "document"
        )
        assert len(embeddings.results) == 1
        return embeddings.results[0].embeddings

class TempDatabase:
    def __init__(
            self,
            db_path: str,
            collection_name: str,
            content_path: str,
            chunk_size: int = 500,
            overwrite: bool = False
        ):

        if not os.path.exists(content_path):
            raise FileNotFoundError(f"Content file not found: {content_path}")
        
        self.chunk_size = chunk_size
        self.content_path = content_path
        self.embedding_function = VoyageEmbeddingFunction()

        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)

        if overwrite:
            try:
                print(f"Overwriting and deleting existing collection: {collection_name}")
                self.client.delete_collection(collection_name)
            except:
                pass
        
        try:
            print(f"Try getting existing collection: {collection_name}")
            self.collection = self.client.get_collection(
                name=collection_name, 
                embedding_function=self.embedding_function
            )
        except:
            print(f"Collection {collection_name} does not exist, creating a new one.")
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
            self.load_initial_content()

    def _split_text(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size):
            chunk = text[i : i + self.chunk_size]
            chunks.append(chunk.strip())
        return chunks

    def _generate_chunk_id(self, page: int, class_name: str, chunk_index: int) -> str:
        return f"page_{page}_{class_name}_chunk_{chunk_index}"

    def check_memory_exists(self, memory_id: str) -> bool:
        try:
            result = self.collection.get(ids=[memory_id])
            return len(result['ids']) > 0
        except Exception as e:
            print(f"Error checking if memory {memory_id} exists: {e}")
            return False

    def load_initial_content(self):
        try:
            if not os.path.exists(self.content_path):
                print(f"Content file not found: {self.content_path}")
                return

            with open(self.content_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            pages = soup.find_all('div', class_='background-page')
            data = []
            print(f"Found {len(pages)} pages in the content file")

            for page_div in pages:
                page_id = page_div.get('id', '')
                page_match = re.search(r'page_(\d+)', page_id)
                page_number = int(page_match.group(1)) if page_match else 0
                
                component_divs = page_div.find_all('div', class_=re.compile(r'^component_\d+_\d+$'))

                for component_div in component_divs:
                    class_name = component_div.get('class')[0]  # Get the first class
                    raw_text = component_div.get_text()
                    
                    if raw_text.strip():  # Only add non-empty content
                        data.append({
                            "content": raw_text,
                            "page": page_number,
                            "class_name": class_name
                        })
            print(f"Found {len(data)} components in the content file")
            chunks_added = self.add_memory(data)
            
        except Exception as e:
            print(f"Warning: Could not load initial content: {e}")

    def add_memory_from_html(self, html: str, page: int):
        soup = BeautifulSoup(html, 'html.parser')
        components = soup.find_all('div', class_=re.compile(r'^component_\d+_\d+$'))
        data = []
        for component in components:
            class_name = component.get('class')[0]
            raw_text = component.get_text()
            if raw_text.strip():
                data.append({
                    "content": raw_text,
                    "page": page,
                    "class_name": class_name
                })
        self.add_memory(data)

    def delete_memory_from_html(self, html: str, page: int):
        soup = BeautifulSoup(html, 'html.parser')
        components = soup.find_all('div', class_=re.compile(r'^component_\d+_\d+$'))
        for component in components:
            class_name = component.get('class')[0]
            self.delete_memory(page, class_name)

    def add_memory(self, data: List[Dict[str, Any]]) -> int:
        try:
            ids = []
            documents = []
            metadatas = []

            for item in data:
                content = item["content"]
                page = item["page"]
                class_name = item["class_name"]
                text_chunks = self._split_text(content)

                for chunk_index, chunk in enumerate(text_chunks):
                    if not chunk.strip():
                        continue
                    
                    memory_id = self._generate_chunk_id(page, class_name, chunk_index)

                    if self.check_memory_exists(memory_id):
                        continue
                    
                    ids.append(memory_id)
                    documents.append(chunk)
                    metadatas.append({
                        "page": page,
                        "class_name": class_name,
                        "chunk_index": chunk_index
                    })

            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

            if len(documents) > 0:
                print(f"Successfully added {len(documents)} chunks")

            return len(documents)

        except Exception as e:
            print(f"Error adding memory: {e}")
            raise


    def delete_memory(self, page: int, class_name: str) -> None:
        try:
            results = self.collection.get(
                where={
                    "$and": [
                        {"page": {"$eq": page}},
                        {"class_name": {"$eq": class_name}}
                    ]
                }
            )
            
            if results['ids']:
                print(f"Deleting {len(results['ids'])} memories for page {page}, class {class_name}")
                self.collection.delete(ids=results['ids'])
            else:
                print(f"No memories found for page {page}, class {class_name}")
                
        except Exception as e:
            print(f"Error deleting memory: {e}")
            raise

    def query_memory(self, query: str, page: List[int] | None = None) -> List[Dict[str, Any]]:
        print(f"Querying memory for query: '{query}'")
        try:
            # Build where clause for filtering
            where_clause = {}
            if page is not None:
                where_clause = {"page": {"$in": page}}

            if where_clause:
                results = self.collection.query(
                    query_texts=[query],
                    #n_results=2,
                    where=where_clause
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    #n_results=2
                )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        "page": results['metadatas'][0][i]['page'],
                        "class_name": results['metadatas'][0][i]['class_name'],
                    })
                    print(f"Found {results['metadatas'][0][i]['page']} {results['metadatas'][0][i]['class_name']}")
            
            unique_tuples = list(set((item['page'], item['class_name']) for item in formatted_results))
            unique_results = [{"page": page, "class_name": class_name} for page, class_name in unique_tuples]
            
            print(f"Found {len(unique_results)} unique memories matching query: '{query}'")
            return unique_results
            
        except Exception as e:
            print(f"Error querying memory: {e}")
            raise
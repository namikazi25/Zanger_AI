# Placeholder for a vector database implementation
# This file provides stubs for add(doc) and query(vec)
# to shape I/O for easy swapping to a real vector DB (e.g., Pinecone) later.

from typing import List, Any, Dict

class PlaceholderVectorDB:
    def __init__(self):
        """Initializes the placeholder vector database."""
        self.documents = []
        print("Initialized PlaceholderVectorDB")

    def add(self, doc: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Adds a document to the placeholder database.
        In a real implementation, this would involve creating embeddings and storing them.
        Args:
            doc: The document content (e.g., text).
            metadata: Optional metadata associated with the document.
        """
        # In a real vector DB, you'd embed the document here.
        # For this placeholder, we'll just store it along with any metadata.
        entry = {"document": doc, "metadata": metadata or {}}
        self.documents.append(entry)
        print(f"PlaceholderVectorDB: Added document. Total documents: {len(self.documents)}")
        # print(f"Added document: {str(doc)[:100]}... with metadata: {metadata}")

    def query(self, vec: List[float], top_k: int = 5, filter_criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Queries the placeholder database with a vector.
        In a real implementation, this would perform a similarity search.
        Args:
            vec: The query vector.
            top_k: The number of top similar documents to return.
            filter_criteria: Optional criteria to filter results.
        Returns:
            A list of dummy results, mimicking a real vector DB response.
        """
        print(f"PlaceholderVectorDB: Received query vector (first 3 elements): {vec[:3]}..., top_k: {top_k}, filter: {filter_criteria}")
        # This is a stub, so it returns dummy data.
        # A real implementation would search for similar vectors.
        if not self.documents:
            print("PlaceholderVectorDB: No documents in store to query.")
            return [{"id": "dummy_id_no_docs", "score": 0.0, "metadata": {"message": "No documents in store."}}]
        
        # Simulate returning some documents if they exist, otherwise a placeholder
        num_to_return = min(top_k, len(self.documents))
        dummy_results = []
        for i in range(num_to_return):
            dummy_results.append({
                "id": f"dummy_id_{i+1}",
                "score": 1.0 - (i * 0.1),  # Dummy score
                "document_content_preview": str(self.documents[i]["document"])[:50] + "...",
                "metadata": self.documents[i]["metadata"]
            })
        
        print(f"PlaceholderVectorDB: Returning {len(dummy_results)} dummy results.")
        return dummy_results

# Example Usage (for testing purposes):
if __name__ == '__main__':
    db = PlaceholderVectorDB()

    # Add some documents
    db.add("This is the first document about AI.", metadata={"source": "doc1.txt"})
    db.add("Another document discussing machine learning.", metadata={"source": "doc2.txt", "topic": "ML"})
    db.add("A final document on neural networks.", metadata={"topic": "NN"})

    # Query the database
    dummy_query_vector = [0.1, 0.2, 0.3] # A real vector would be high-dimensional
    results = db.query(dummy_query_vector, top_k=2)

    print("\n--- Query Results ---")
    if results:
        for res in results:
            print(f"ID: {res['id']}, Score: {res['score']:.2f}, Preview: '{res['document_content_preview']}', Metadata: {res['metadata']}")
    else:
        print("No results returned from query.")

    results_filtered = db.query(dummy_query_vector, top_k=1, filter_criteria={"topic": "ML"})
    print("\n--- Filtered Query Results (simulation, filter not actually applied by placeholder) ---")
    if results_filtered:
        for res in results_filtered:
            print(f"ID: {res['id']}, Score: {res['score']:.2f}, Preview: '{res['document_content_preview']}', Metadata: {res['metadata']}")
    else:
        print("No results returned from filtered query.")
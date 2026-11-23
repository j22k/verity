from abc import ABC, abstractmethod

class BlobStore(ABC):
    @abstractmethod
    def put(self, key:str, obj:bytes)-> str:
        """Store a blob in the blob store and return its key."""
        pass
    
    @abstractmethod
    def get(self, key:str)-> bytes:
        """Retrieve a blob from the blob store."""
        pass

    @abstractmethod
    def delete(self, key:str)-> None:
        """Delete a blob from the blob store."""
        pass

    @abstractmethod
    def exists(self, key:str)-> bool:
        """Check if a blob exists in the blob store."""
        pass
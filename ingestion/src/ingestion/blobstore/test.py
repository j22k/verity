from .local import LocalBlobStore

class TestLocalBlobStore:
    def __init__(self,name,age):
        self.name = name
        self.age = age

v1= TestLocalBlobStore("Alice", 30)

def test_local_blobstore():
    # Create a LocalBlobStore instance with a temporary directory
    blobstore = LocalBlobStore(root="temp_blobstore")
    # blobstore.put("test_key", v1.name.encode('utf-8'))  # Store the name as bytes

    print(blobstore.exists("test_key"))  # Should print True
    print(blobstore.get("test_key").decode('utf-8'))  # Should print "Alice"
    blobstore.delete("test_key")
    # Clean up the temporary directory after the test
    # blobstore.root.rmdir()

if __name__ == "__main__":
    test_local_blobstore()
    print("All tests passed.")

# Class to write to file.
# Shared between processes to avoid concurrency.
class Writer:
    def __init__(self, path="output.txt"):
        # Clear existing output if it exists.
        with open(path, "w") as f:
            f.write("")
            f.close()

        # Open file to be used.
        self.file = open(path, "a")

    # Write to file.
    def write(self, text):
        self.file.write(text)
    
    # Close the file.
    # Should be called at the end.
    def close(self):
        self.file.close()

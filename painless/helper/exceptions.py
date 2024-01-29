class PathDoesNotExist(Exception):
    """Custom exception for non-existing paths or invalid path types."""
    def __init__(self, message:str = "The specified path doesn't exist"):
        self.message = message
        super().__init__(self.message)

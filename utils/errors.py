class RTLScriptError(Exception):
    """Represents an error with a script (the source text)."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return f"Error building script: {self.message}"

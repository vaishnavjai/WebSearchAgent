"""Model selection variables.

Define the models used by the application. Example model string:
    'llama3.1:8b'
"""

# Main model used for primary tasks
mainModel: str = "llama3.1:8b"

# Worker model used for background/auxiliary tasks
workerModel: str = "gemma3:270m"

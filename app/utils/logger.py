import logging

# Create logger
logger = logging.getLogger("agentic-ai")

# Set level
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add handler
logger.addHandler(console_handler)
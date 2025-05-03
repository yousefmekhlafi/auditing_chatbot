# src/utils/logging_config.py
import logging
import sys

def setup_logging(level=logging.INFO):
    """Sets up basic logging to console."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)] # Log to standard output
    )
    # You can suppress overly verbose logs from libraries here if needed
    # logging.getLogger("some_library").setLevel(logging.WARNING)
    print("Logging configured.")

# Example usage (you'll call this from your main scripts/apps)
# if __name__ == "__main__":
#     setup_logging()
#     logging.info("This is an info message.")
#     logging.warning("This is a warning message.")
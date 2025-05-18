import os
from loguru import logger

def execute_command(cmd: str) -> str:
    import subprocess
    """Execute a shell command and return the output."""
    try:
        logger.info(f"Executing command: {cmd}")
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
        logger.info(f"Command executed successfully: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}: {e.stderr}")
        raise e

def cleanup_dylib(name: str) -> None:
    """Remove the specified .dylib file if it exists."""
    try:
        os.remove(f"{name}.dylib")
        logger.info(f"Successfully removed {name}.dylib")
    except FileNotFoundError:
        logger.warning(f"File {name}.dylib not found")

def cleanup_file(name: str) -> None:
    """Remove the specified file if it exists."""
    try:
        os.remove(name)
        logger.info(f"Successfully removed {name}")
    except FileNotFoundError:
        logger.warning(f"File {name} not found")
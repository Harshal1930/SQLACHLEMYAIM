from dotenv import load_dotenv
from pathlib import Path
import os
 
 
__BASE_DIR = Path(__file__).resolve().parent.parent
__PARENT_DIR = os.path.dirname(__BASE_DIR)
__ENV_PATH = os.path.join(__PARENT_DIR,".env")
 
def env_get(var: str, default = None) -> str:
    load_dotenv(__ENV_PATH)
    val = os.getenv(var, default=default)
    return val
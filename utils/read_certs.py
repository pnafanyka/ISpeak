from pathlib import Path
import os 
from dotenv import load_dotenv

load_dotenv()
CERT_PATH = os.getenv('RUS_CERT')

CA_BUNDLE = str(Path(CERT_PATH).resolve())
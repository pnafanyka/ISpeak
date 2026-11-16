from pathlib import Path
import os

CERT_PATH = os.getenv("RUS_CERT")

CA_BUNDLE = str(Path(CERT_PATH).resolve())
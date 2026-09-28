import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.wsgi import application

app = application
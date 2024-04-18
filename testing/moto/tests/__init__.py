import sys
from pathlib import Path

dir_path = Path(__file__).parent.parent
sys.path.append(Path(dir_path, "src").as_posix())

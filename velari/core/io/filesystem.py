from pathlib import Path

get_username  = lambda: Path.home().name
get_user_home = lambda: str(Path.home())

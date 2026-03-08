import  logging
import  os
from    pathlib import Path
from    appdirs import user_cache_dir
from    dotenv import dotenv_values, find_dotenv, load_dotenv

logger = logging.getLogger(__name__)


def read_root_dir(project_file: str = "pyproject.toml") -> str:
    """Locate the project root by searching parent directories for a marker file.

    Walks up from the current file's location until it finds a directory containing
    the specified marker file, falling back to the filesystem root if none is found.

    Args:
        project_file: Filename whose presence identifies the project root directory.
            Defaults to ``"pyproject.toml"``.

    Returns:
        Absolute path string of the first ancestor directory that contains
        ``project_file``, or the filesystem root if no match is found.

    Examples:
        >>> root = read_root_dir()

        Use the root to build derived paths for config and data:

        >>> from pathlib import Path
        >>> root = read_root_dir()
        >>> config_dir = Path(root) / "config"
        >>> data_dir   = Path(root) / "data" / "catalog"
    """
    path = Path(__file__).resolve()
    while path != path.parent:
        if (path / project_file).exists():
            return str(path)
        path = path.parent
    # fallback to filesystem root
    return str(path)


def read_env(path: str = ".env", verbose: bool = False) -> dict:
    """Load environment variables from a dotenv file and return them as a dictionary.

    Searches for the file by name starting from the current working directory,
    loads it into the process environment, then returns a snapshot of its key-value
    pairs. Logs an exception and returns None if the file is not found.

    Args:
        path: Filename of the dotenv file to locate and load. Defaults to ``".env"``.
        verbose: When True, prints diagnostic information about the loading process.
            Defaults to False.

    Returns:
        Dictionary mapping each environment variable name to its string value,
        or None if the file could not be found or parsed.

    Examples:
        >>> config = read_env()

        Load a shared environment file and retrieve a specific API key:

        >>> config = read_env(".env.shared", verbose=True)
        >>> openai_key = config.get("OPENAI_API_KEY")
        >>> mlflow_uri = config.get("MLFLOW_TRACKING_URI")
    """
    try:
        load_dotenv(find_dotenv(filename=path, raise_error_if_not_found=True), verbose=verbose)
        config: dict = dotenv_values(path)
        return config
    except Exception as e:
        logger.exception(f"Exception Occured Reading DotFile:{e}")


def read_cache_dir(author: str = None, app: str = None) -> str:
    """Retrieve the platform-specific cache directory, creating it if it does not exist.

    Args:
        author: Author or organisation name used to namespace the cache path on Windows.
            Ignored on macOS and Linux. Defaults to None.
        app: Application or project name used to namespace the cache directory.
            Defaults to None.

    Returns:
        Absolute path string of the resolved cache directory, which is guaranteed
        to exist after this call returns.

    Examples:
        >>> cache = read_cache_dir(app="velari-aistudio")

        Resolve the Hugging Face hub cache and pass it to a model loader:

        >>> import os
        >>> cache = read_cache_dir(author="akamlani", app="huggingface/hub")
        >>> os.environ["HF_HOME"] = cache  # point HF_HOME to the managed cache dir
    """
    cache_dir = user_cache_dir(app, author)
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    return cache_dir

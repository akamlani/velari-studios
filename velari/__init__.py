import  os
import  logging
from    typing import Any, Dict
from    pathlib import Path
from    omegaconf import OmegaConf, DictConfig

# Local Files
from    .core import read_root_dir
from    .core.io.partition.hydra import read_hydra_defaults, read_hydra
from    .version import __version__, watermark


def setup_logging():
    """Configure the root logger using a Hydra-managed logging configuration file.

    Reads the logging filename from the project's main Hydra config, loads the
    corresponding YAML logging config, resolves the log file path relative to the
    project root, creates the ``logs/`` directory if absent, and applies the
    full configuration via ``logging.config.dictConfig``.

    Skips logging configuration if running in a Jupyter notebook or IPython environment.

    Examples:
        >>> setup_logging()  # called automatically on package import

        Manually reinitialise logging then retrieve a named child logger:

        >>> import logging
        >>> setup_logging()
        >>> logger = logging.getLogger("velari.studios.aistudio")
        >>> logger.info("Logging initialised for this session.")
    """
    # Check if running in a notebook environment
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            return
    except ImportError:
        pass

    filename: DictConfig = read_hydra_defaults(config_dir=Path(read_root_dir()).joinpath("config").resolve(), config_name="config").logging
    logging_config = read_hydra(Path(read_root_dir()).joinpath("config").joinpath(filename).resolve())
    # create /logs directory
    log_dir = Path(read_root_dir()).joinpath("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    # configure root logger
    log_filename = logging_config.handlers.file_handler.filename
    logging_config.handlers.file_handler.filename = str(Path(read_root_dir()).joinpath(log_filename).resolve())
    logger_dict: Dict[str, Any] = OmegaConf.to_container(logging_config, resolve=True)
    logging.config.dictConfig(logger_dict)


logger = logging.getLogger("root")
setup_logging()

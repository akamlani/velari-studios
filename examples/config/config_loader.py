import  hydra
import  logging
from    omegaconf import DictConfig, OmegaConf
# package modules
from    velari.core import Experiment

logger = logging.getLogger(__name__)
exp    = Experiment()


@hydra.main(config_path=str(exp.conf_dir), config_name="config", version_base=None)
def main(cfg: DictConfig):
    # Access specific config values
    logger.info(f"Provider Config:\n{OmegaConf.to_yaml(cfg.experimentation)}")

if __name__ == "__main__":
    main()
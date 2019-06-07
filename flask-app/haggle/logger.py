import os
import yaml
import logging.config


logging_level_dict = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG
}

DEFAULT_LEVEL = 2  # logging.DEBUG


def setup_logging(log_dir='/tmp/logs', log_config='logging.yml', default_level=DEFAULT_LEVEL):
    """
    Setup logging configuration
    """
    if os.path.exists(log_config):
        with open(log_config, 'rt') as f:
            config = yaml.safe_load(f.read())

        # prepend log_dir to log filenames
        for _, handler in config['handlers'].items():
            if 'filename' in handler:
                handler['filename'] = os.path.join(log_dir, handler['filename'])

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def setup_logger(name, verbose=DEFAULT_LEVEL):

    logger = logging.getLogger(name)

    if verbose not in logging_level_dict:
        raise KeyError(f'Verbose option {verbose} for {name} not valid. '
                       f'Valid options are {logging_level_dict.keys()}.')
    logger.setLevel(logging_level_dict[verbose])
    return logger

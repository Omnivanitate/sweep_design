"""The configuration of project.

> The configuration is defined by three classes: Config (config.config.Config), 
SweepConfig (config.sweep_config.SweepConfig) and NamedConfig (config.sweep_config.NamedConfig).

> Using three config files to avoid the circular import error.

> Detailed description of the attributes in each of the files.
"""

from .config import Config as Config

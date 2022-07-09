"""The configuration of project.

> The configuration is defined by three classes: `Config`
(`sweep_design.config.config.Config`),
`SweepConfig` (`sweep_design.config.sweep_config.SweepConfig`) and `NamedConfig` 
(`sweep_design.config.named_config.NamedConfig`).

> Using three config files to avoid the circular import error.

> Detailed description of the attributes in each of the files.
"""

from .config import Config as Config

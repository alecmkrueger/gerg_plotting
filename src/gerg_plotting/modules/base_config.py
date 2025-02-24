from attrs import define, asdict
from pprint import pformat

@define
class BaseConfig:
    """Base configuration class providing common functionality."""
    
    def __repr__(self) -> str:
        """Return detailed string representation of config."""
        return pformat(asdict(self))
    
    def __str__(self) -> str:
        """Return readable string representation of config."""
        return pformat(asdict(self), width=1)
    
    def __getitem__(self, key: str):
        """Enable dictionary-style access to config attributes."""
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Config has no attribute '{key}'")
    
    def __setitem__(self, key: str, value) -> None:
        """Enable dictionary-style setting of config attributes."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Config has no attribute '{key}'")
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return asdict(self)
    
    def get_attrs(self) -> set:
        """Get all configuration attributes."""
        return set(asdict(self).keys())

from typing import Protocol, Optional, List, Union, Tuple, Sequence
from pymongo import IndexModel

IndexKey = Tuple[str, int]
IndexSpec = Union[str, IndexKey, Sequence[IndexKey], IndexModel]

class BeanieSettingsProtocol(Protocol):
    validate_on_save: Optional[bool]
    use_state_management: Optional[bool]
    keep_nulls: Optional[bool]
    name: Optional[str]
    indexes: Optional[List[IndexSpec]]
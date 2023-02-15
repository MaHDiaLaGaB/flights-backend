# pylint: disable=W0511
from subprocess import CompletedProcess
from typing import Any, Dict, List, Tuple, Union

# TODO ApiResponse should be typed properly not as Any
ApiResponse = Tuple[Union[List[Any], Dict[str, Any]], int]
Entity = Dict[str, Any]
EntityList = List[Entity]


# another typeshed problem
try:
    CompletedProcessAny = CompletedProcess[Any]
except TypeError:
    CompletedProcessAny = CompletedProcess  # type: ignore

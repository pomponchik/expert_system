from dataclasses import dataclass

from srcs.string import String


@dataclass
class Fact:
    value: bool
    string: String

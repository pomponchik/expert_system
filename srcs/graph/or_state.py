from dataclasses import dataclass

from srcs.expression_block import ExpressionBlock
from srcs.expression import Expression


@dataclass
class OrState:
    block: ExpressionBlock
    expression: Expression


@dataclass
class OrStates:
    states: list[OrState]

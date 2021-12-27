from dataclasses import dataclass

from srcs.expression_block import ExpressionBlock
from srcs.expression import Expression


@dataclass
class Link:
    block: ExpressionBlock
    expression: Expression
    or_block: ExpressionBlock = None

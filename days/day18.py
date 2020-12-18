from helpers import *
import ast


test_case(1, """2 * 3 + (4 * 5)""", 26)
test_case(2, """2 * 3 + (4 * 5)""", 46)

# How to attack this advanced math?! With more advanced math.
# in part 1 we need to have same precedence for * and +, so we
# replace * with -, which now means multiplication but at same
# precedence level as addition, and then parse the tree to ast,
# then transform the operators back to their Python equivalents
# and compile, eval, run.

# in part 2 we need the precedences reversed so we use / for +.

operator_mapping = {
    ast.Sub: ast.Mult,
    ast.Div: ast.Add,
    ast.Add: ast.Add,
    ast.Mult: ast.Mult,
}


class RewriteBinOps(ast.NodeTransformer):
    def visit_BinOp(self, node):
        return ast.BinOp(
            self.visit(node.left),
            operator_mapping[type(node.op)](),
            self.visit(node.right)
        )


def eval_it(d: str) -> int:
    result = 0
    for expression in Data(d).lines:
        tree = ast.parse(expression, mode='eval')
        new_tree = ast.fix_missing_locations(RewriteBinOps().visit(tree))
        result += eval(compile(new_tree, '<string>', 'eval'))

    return result


def part1(d: Data, ans: Answers) -> None:
    ans.part1 = eval_it(d.replace('*', '-'))


def part2(d: Data, ans: Answers) -> None:
    ans.part2 = eval_it(d.replace('*', '-').replace('+', '/'))


run([1, 2], day=18, year=2020)

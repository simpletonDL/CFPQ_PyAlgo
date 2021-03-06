from pathlib import Path

from src.algo.algo_interface import CFPQAlgo

from src.grammar.cnf_grammar import CnfGrammar
from src.graph.label_graph import LabelGraph
from pygraphblas import BOOL


class MatrixBaseSolver(CFPQAlgo):
    def __init__(self, path_to_graph: Path, path_to_grammar: Path):
        super().__init__(path_to_graph, path_to_grammar)
        self.graph = LabelGraph.from_txt(str(path_to_graph) + ".txt")
        self.grammar = CnfGrammar.from_cnf(str(path_to_grammar) + ".cnf")

    def solve(self):
        pass


class MatrixBaseAlgo(MatrixBaseSolver):
    
    def solve(self):
        m = LabelGraph(self.graph.matrices_size)
        for l, r in self.grammar.simple_rules:
            m[l] += self.graph[r]
        changed = True
        while changed:
            changed = False
            for l, r1, r2 in self.grammar.complex_rules:
                old_nnz = m[l].nvals
                m[l] += m[r1].mxm(m[r2], semiring=BOOL.LOR_LAND)
                new_nnz = m[l].nvals
                changed |= not old_nnz == new_nnz
        return m[self.grammar.start_nonterm]

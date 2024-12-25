from typing import Any

from qiskit import QuantumCircuit  # type: ignore[import-untyped]
from qiskit import transpile as qiskit_transpile  # type: ignore[import-untyped]

from tranqu.transpile_result import TranspileResult

from .qiskit_layout_mapper import QiskitLayoutMapper
from .qiskit_stats_extractor import QiskitStatsExtractor
from .transpiler import Transpiler


class QiskitTranspiler(Transpiler):
    """Transpile quantum circuits using Qiskit.

    It optimizes quantum circuits using Qiskit's `transpile()` function.
    """

    def __init__(self) -> None:
        self._stats_extractor = QiskitStatsExtractor()
        self._layout_mapper = QiskitLayoutMapper()

    def transpile(
        self,
        program: QuantumCircuit,
        options: dict | None = None,
        device: Any | None = None,  # noqa: ANN401
    ) -> TranspileResult:
        """Transpile the specified quantum circuit and return a TranspileResult.

        Args:
            program (QuantumCircuit): The quantum circuit to transpile.
            options (dict, optional): Transpilation options.
                Defaults to an empty dictionary.
            device (Any, optional): The target device for transpilation.
                Defaults to None.

        Returns:
            TranspileResult: An object containing the transpilation result,
                including the transpiled quantum circuit, statistics,
                and the mapping of virtual qubits to physical qubits.

        """
        _options = options or {}
        if device is not None:
            _options["backend"] = device

        transpiled_program = qiskit_transpile(program, **_options)

        stats = {
            "before": self._stats_extractor.extract_stats_from(program),
            "after": self._stats_extractor.extract_stats_from(transpiled_program),
        }
        mapping = self._layout_mapper.create_mapping_from_layout(transpiled_program)

        return TranspileResult(transpiled_program, stats, mapping)

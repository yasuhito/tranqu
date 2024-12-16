from typing import Any

from tranqu.tranqu_error import TranquError


class TranspilerError(TranquError):
    """Base exception for transpiler-related errors."""


class DefaultTranspilerLibAlreadyRegisteredError(TranspilerError):
    """Raised when a default transpiler_lib is already registered."""


class TranspilerAlreadyRegisteredError(TranspilerError):
    """Raised when attempting to register a transpiler that already exists."""


class TranspilerNotFoundError(TranspilerError):
    """Raised when the requested transpiler is not found."""


class TranspilerManager:
    """Manages the registration and retrieval of transpilers.

    This class allows for the registration of different transpiler instances
    and provides methods to fetch them by their library names.
    """

    def __init__(self) -> None:
        self._transpilers: dict[str, Any] = {}
        self._default_transpiler_lib: str | None = None

    def register_default_transpiler_lib(
        self,
        default_transpiler_lib: str,
    ) -> None:
        """Register the default transpiler library.

        Args:
            default_transpiler_lib (str): The name of the default transpiler library
                to register.

        Raises:
            DefaultTranspilerLibAlreadyRegisteredError: If a transpiler
                with the same name is already registered.

        """
        if self._default_transpiler_lib is not None:
            msg = (
                f"Default transpiler_lib '{self._default_transpiler_lib}' "
                "is already registered."
            )
            raise DefaultTranspilerLibAlreadyRegisteredError(msg)

        self._default_transpiler_lib = default_transpiler_lib

    def fetch_default_transpiler_lib(self) -> str | None:
        """Fetch the default transpiler library.

        Returns:
            str: The default transpiler library.

        """
        return self._default_transpiler_lib

    def register_transpiler(
        self,
        transpiler_lib: str,
        transpiler: Any,  # noqa: ANN401
    ) -> None:
        """Register a new transpiler.

        Args:
            transpiler_lib (str): The name of the transpiler library to register.
            transpiler (Any): An instance of the Transpiler to register.

        Raises:
            TranspilerAlreadyRegisteredError: If a transpiler with the same name
                is already registered.

        """
        if transpiler_lib in self._transpilers:
            msg = f"Transpiler '{transpiler_lib}' is already registered."
            raise TranspilerAlreadyRegisteredError(msg)

        self._transpilers[transpiler_lib] = transpiler

    def fetch_transpiler(
        self,
        transpiler_lib: str,
    ) -> Any:  # noqa: ANN401
        """Fetch a registered transpiler by its library name.

        Args:
            transpiler_lib: The name of the transpiler library to fetch.

        Returns:
            Any: An instance of the requested transpiler.

        Raises:
            TranspilerNotFoundError: If no transpiler with the given name is found.

        """
        transpiler = self._transpilers.get(transpiler_lib)
        if transpiler is None:
            msg = f"Unknown transpiler: {transpiler_lib}"
            raise TranspilerNotFoundError(msg)

        return transpiler

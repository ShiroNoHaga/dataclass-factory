import sys
from typing import Tuple


def _true():
    return True


def _false():
    return False


class PythonVersionRequirement:
    __slots__ = ('ver', 'is_meet', '__bool__')

    @classmethod
    def make(cls, *ver: int):
        return cls(ver)

    def __init__(self, ver: Tuple[int, ...]):
        self.ver = ver
        self.is_meet = sys.version_info >= ver
        self.__bool__ = _true if self.is_meet else _false

    def __call__(self, func):
        import pytest

        ver_str = '.'.join(map(str, self.ver))

        return pytest.mark.skipif(
            not self.is_meet,
            reason=f'Need Python >= {ver_str}'
        )(func)

    def __repr__(self):
        return f"<{type(self).__qualname__} ver={self.ver} is_meet={self.is_meet}>"


has_py_38 = PythonVersionRequirement.make(3, 8)
has_py_39 = PythonVersionRequirement.make(3, 9)

has_pos_only_params = has_py_38
has_protocol = has_py_38
has_literal = has_py_38
has_final = has_py_38
has_typed_dict = has_py_38

has_annotated = has_py_39

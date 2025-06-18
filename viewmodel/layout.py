from typing import Optional, List

from generate_layout import select_layout, init_layout, verify_layout

class LayoutViewModel:
    """ViewModel wrapping layout generation utilities."""

    def select_layout(self, name: Optional[str]) -> tuple[str, List[List[str]]]:
        return select_layout(name)

    def init_layout(self, name: str, groups: List[List[str]], out_dir: str) -> None:
        init_layout(name, groups, out_dir)

    def verify_layout(self, name: str, groups: List[List[str]], out_dir: str) -> None:
        verify_layout(name, groups, out_dir)
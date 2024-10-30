"""Provide a class for a percentage bar that is linked to a tree view node.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from apptk.widgets.percentage_bar import PercentageBar


class LinkedPercentageBar(PercentageBar):
    """Going to the linked node in the tree view on double-click."""
    treeView = None
    # this class constant must be set from outsides.

    def __init__(self, parent, node, text='', value=None, lblWidth=None, lblDist=0, anchor='e', **kwargs):
        super().__init__(parent, text, value, lblWidth, lblDist, anchor, **kwargs)
        self._node = node
        self.label.bind('<Double-Button-1>', self._on_double_click)
        self.progressBar.bind('<Double-Button-1>', self._on_double_click)

    def _on_double_click(self, event=None):
        """Select the node in the project tree that is linked to the double-clicked element."""
        if self.treeView is None:
            return

        try:
            self.treeView.go_to_node(self._node)
        except:
            pass


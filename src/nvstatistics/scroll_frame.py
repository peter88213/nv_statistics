"""Provide a tkinter frame.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvstatistics.platform.platform_settings import MOUSE
from nvstatistics.platform.platform_settings import PLATFORM
import tkinter as tk


class ScrollFrame(ttk.Frame):

    def __init__(self, parent, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(
            self,
            orient='vertical',
            command=self.yview,
        )
        scrollY.pack(fill='y', side='right', expand=False)

        self.canvas = tk.Canvas(
            self,
            borderwidth=0,
            highlightthickness=0
            )
        self.canvas.configure(yscrollcommand=scrollY.set)
        self.canvas.pack(
            anchor='n',
            fill='both',
            expand=True
            )
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        if PLATFORM == 'ix':
            # Vertical scrolling
            self.canvas.bind(MOUSE.BACK_SCROLL, self.on_mouse_wheel)
            self.canvas.bind(MOUSE.FORWARD_SCROLL, self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)

        self._yscrollincrement = self.canvas['yscrollincrement']

    def destroy(self):
        """Destructor for deleting event bindings."""
        if PLATFORM == 'ix':
            # Vertical scrolling
            self.canvas.unbind_all(MOUSE.BACK_SCROLL)
            self.canvas.unbind_all(MOUSE.FORWARD_SCROLL)
        else:
            # Vertical scrolling
            self.canvas.unbind_all('<MouseWheel>')
        super().destroy()

    def on_mouse_wheel(self, event):
        """Event handler for vertical scrolling."""
        if PLATFORM == 'win':
            self.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        elif PLATFORM == 'mac':
            self.yview_scroll(int(-1 * event.delta), 'units')
        else:
            if event.num == 4:
                self.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.yview_scroll(1, 'units')

    def xview(self, *args):
        self.canvas.xview(*args)

    def yview(self, *args):
        self.canvas.yview(*args)

    def yview_scroll(self, *args):
        if self.canvas.yview() == (0.0, 1.0):
            return

        self.canvas.yview_scroll(*args)


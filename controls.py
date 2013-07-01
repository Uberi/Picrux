from tkinter import *
from tkinter.ttk import *

def bind_tag(tag, *widgets):
    """Bind a given tag as the first bindtag for each given widget"""
    for widget in widgets:
        widget.bindtags((tag,) + widget.bindtags())

def entry_active(event): # called upon hovering or focusing on an entry
    event.widget.config(style="Active.Entry.TFrame") # set frame as active
    children = event.widget.winfo_children()
    label = [x for x in children if x.winfo_class() == "TLabel"][0] # find label in the frame
    label.config(style="Active.Entry.TLabel") # set label as active

def entry_inactive(event): # called upon stopping of hovering or focusing on an entry
    event.widget.config(style="Entry.TFrame") # set frame as active
    children = event.widget.winfo_children()
    label = [x for x in children if x.winfo_class() == "TLabel"][0] # find label in the frame
    label.config(style="Entry.TLabel") # set label as active

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the "interior" attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas"s width to fit the inner frame
                canvas["width"] = interior.winfo_reqwidth()

        def configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        interior.bind("<Configure>", configure_interior)
        canvas.bind("<Configure>", configure_canvas)
        return
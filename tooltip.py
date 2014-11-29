from tkinter import *
from time import time

class ToolTip(Toplevel):
    """
    widget: tooltip is applied to this object
    text: tooltip display message
    text_funct: function reference that updates tooltip text
    color: background color of the tool tip
    delay: amount of time in seconds before the tooltip displays
    follow: If false, the tool tip won't follow the mouse movement
    """
    def __init__(self, widget, text, text_funct=None, color=None, delay=0.25, follow=True):
        self.widget = widget

        # parent of the widget object
        self.parent = self.widget.master
        Toplevel.__init__(self, self.parent, background='black', padx=2, pady=2)
        
        # hide tooltip initially
        self.withdraw()
        
        # no frame or title bar for the tool tip
        self.overrideredirect(True)
    
        self.text_funct = text_funct
        self.text = StringVar()
        if (self.text_funct != None):
            self.text.set(self.text_funct())
        else:
            self.text.set(text)

        self.visible = 0
        self.last_movement = 0
        self.delay = delay
        self.follow = follow
        
        bg_color = '#FFFB9F'
        if color != None:
            bg_color = color
            
        self.tip = Label(self, textvariable=self.text, padx=5, pady=5, wraplength=350,
                         background=bg_color, foreground='black', font='arial 12 bold')
        self.tip.grid()
        
        self.widget.bind('<Enter>', self.allow_for_display)
        self.widget.bind('<Leave>', self.hide_tip)
        
    def allow_for_display(self, event=None):
        self.widget.bind_all('<Motion>', self.move_tip)
        self.visible = 1
        self.after(int(self.delay * 1000), self.display_tip)
        
    def display_tip(self):
        if self.visible == 1 and time() - self.last_movement > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
            
    def move_tip(self, event):
        self.last_movement = time()
        
        # tooltip will disappear on motion
        if self.follow == False:
            self.withdraw()
            self.visible = 1

        # offset the tooltip message from mouse pointer
        self.geometry('+%i+%i' % (event.x_root + 15, event.y_root))
        try:
            self.text.set(self.text_funct())
        except:
            pass
        
        self.after(int(self.delay * 1000), self.display_tip)

    def hide_tip(self, event=None):
        self.visible = 0
        self.withdraw()

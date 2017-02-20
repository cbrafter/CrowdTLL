import Tkinter as tkinter
import tkFont


class MessageBox(object):
    # Based on
    # https://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
    def __init__(self, msg, b1, b2, frame, t, entry):

        root = self.root = tkinter.Tk()
        # Window Colors
        root.tk_setPalette(background='#F0F0F0',
                           foreground='black',
                           activeBackground='#005A87',
                           activeForeground='white')
        # Font Style
        self.customFont = tkFont.Font(family="Arial", size=11, weight='bold')

        root.title('SCORE BOX!')
        self.msg = str(msg)

        # ctrl+c to copy self.msg
        root.bind('<Control-c>', func=self.to_clip)

        # remove the outer frame if frame=False
        if not frame:
            root.overrideredirect(True)

        # default values for the buttons to return
        self.b1_return = True
        self.b2_return = False

        # if b1 or b2 is a tuple unpack into the button text & return value
        if isinstance(b1, tuple):
            b1, self.b1_return = b1
        if isinstance(b2, tuple):
            b2, self.b2_return = b2

        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)

        # the message
        message = tkinter.Label(frm_1, text=self.msg, font=self.customFont)
        message.pack(padx=8, pady=8)

        # if entry=True create and set focus
        if entry:
            self.entry = tkinter.Entry(frm_1)
            self.entry.pack()
            self.entry.focus_set()

        # button frame
        frm_2 = tkinter.Frame(frm_1)
        frm_2.pack(padx=4, pady=4)

        # buttons
        btn_1 = tkinter.Button(frm_2, width=8, text=b1, font=self.customFont)
        btn_1['command'] = self.b1_action
        btn_1.pack(side='left')
        if not entry:
            btn_1.focus_set()
        btn_2 = tkinter.Button(frm_2, width=8, text=b2, font=self.customFont)
        btn_2['command'] = self.b2_action
        btn_2.pack(side='left')

        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        btn_2.bind('<KeyPress-Return>', func=self.b2_action)

        # roughly center the box on screen
        # for accuracy see: http://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        xp = (root.winfo_screenwidth() // 4) - (root.winfo_width() // 4)
        yp = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        geom = (root.winfo_width(), root.winfo_height(), xp, yp)
        root.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # a trick to activate the window (on windows 7)
        root.deiconify()

        # if t is specified: call time_out after t seconds
        if t:
            root.after(int(t*1000), func=self.time_out)

    def b1_action(self, event=None):
        try:
            x = self.entry.get()
        except AttributeError:
            self.returning = self.b1_return
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()

    def b2_action(self, event=None):
        self.returning = self.b2_return
        self.root.quit()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        pass

    def time_out(self):
        try:
            x = self.entry.get()
        except AttributeError:
            self.returning = None
        else:
            self.returning = x
        finally:
            self.root.quit()

    def to_clip(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.msg)


def mbox(msg, b1='OK', b2='Cancel', frame=True, t=False, entry=False):
    """Create an instance of MessageBox, and get data back from the user.
    msg = string to be displayed
    b1 = text for left button, or a tuple (<text for button>, <to return on press>)
    b2 = text for right button, or a tuple (<text for button>, <to return on press>)
    frame = include a standard outerframe: True or False
    t = time in seconds (int or float) until the msgbox automatically closes
    entry = include an entry widget that will have its contents returned: True or False
    """
    msgbox = MessageBox(msg, b1, b2, frame, t, entry)
    msgbox.root.mainloop()
    # the function pauses here until the mainloop is quit
    msgbox.root.destroy()
    return msgbox.returning

if __name__ == "__main__":
    user = {}
    mbox('starting in 1 second...', t=0.001)
    time = 5
    user['name'] = mbox('Your time is {} s!\n Please enter your INITIALS:'.format(time), entry=True)
    print(user)
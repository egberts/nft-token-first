#!/usr/bin/env python3

"""dhparser_projectApp.py - a simple GUI for the compilation of dhparser_project-files"""

import sys
import os
import threading

import tkinter
import webbrowser
from tkinter import ttk
from tkinter import filedialog, messagebox

try:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    scriptdir = ''
if scriptdir and scriptdir not in sys.path: sys.path.append(scriptdir)

import dhparser_projectParser


class dhparser_projectApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title('dhparser_project App')
        self.minsize(480, 320)
        self.geometry("800x600")
        self.option_add('*tearOff', False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # window content resizes with window:
        # win = self.winfo_toplevel()
        # win.rowconfigure(0, weight=1)
        # win.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)

        if 'html' in dhparser_projectParser.targets or 'HTML' in dhparser_projectParser.targets:
            self.target = 'html'
        elif len(dhparser_projectParser.targets) == 1:
            self.target = list(dhparser_projectParser.targets)[0]
        else:
            self.target = ''

        # widget-variables
        self.num_sources = 0
        self.num_compiled = 0
        self.progress = tkinter.IntVar()
        self.progress.set(0)

        self.create_widgets()
        self.connect_events()
        self.place_widgets()

        self.lock = threading.Lock()
        self.worker = None
        self.cancel_flag = False

        self.outdir = ''
        self.names = []

        self.deiconify()

    def create_widgets(self):
        self.pick_source = ttk.Button(self, text="Pick source(s)...", command=self.on_pick_src)
        self.progressbar = ttk.Progressbar(self, orient="horizontal", variable=self.progress)
        self.cancel = ttk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel['state'] = tkinter.DISABLED
        self.result_info = ttk.Label(self, text='Result:')
        self.result = tkinter.Text(self, bg="white")
        self.exit = ttk.Button(text="Quit", command=self.on_close)

    def connect_events(self):
        pass

    def place_widgets(self):
        padW = dict(sticky=(tkinter.W,), padx="5", pady="5")
        padE = dict(sticky=(tkinter.E,), padx="5", pady="5")
        padWE = dict(sticky=(tkinter.W, tkinter.E), padx="5", pady="5")
        padAll = dict(sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E), padx="5", pady="5")
        padNW = dict(sticky=(tkinter.W, tkinter.N), padx="5", pady="5")
        self.pick_source.grid(row=0, column=0, columnspan=2)
        self.progressbar.grid(row=1, column=0, **padWE)
        self.cancel.grid(row=1, column=1, **padE)
        self.result_info.grid(row=2, column=0, **padW)
        self.result.grid(row=3, column=0, columnspan=2, **padAll)
        self.exit.grid(row=4, column=1, **padE)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=9)

    def clear_result(self):
        with self.lock:
            self.result.delete("1.0", tkinter.END)
            self.update()

    def log_callback(self, txt):
        self.result.insert(tkinter.END, txt + '\n')
        self.result.yview_moveto(1.0)
        self.num_compiled += 1
        self.progress.set(min(100, int(100 * self.num_compiled / self.num_sources)))
        self.update()

    def cancel_callback(self) -> bool:
        with self.lock:
            res = self.cancel_flag
        return res

    def poll_worker(self):
        self.update_idletasks()
        if self.worker and self.worker.is_alive():
            self.after(1000, self.poll_worker)
        else:
            self.cancel['stat'] = tkinter.DISABLED
            if self.cancel_flag:
                self.result.yview_moveto(1.0)
                with self.lock:  self.cancel_flag = False
            else:
                self.result.insert(tkinter.END, "Compilation finished.\n")
                out_dir = os.path.join(os.path.dirname(self.names[0]), 'out', self.target)
                if self.target == 'html':
                    html_name = os.path.splitext(os.path.basename(self.names[0]))[0] + '.html'
                    html_name = os.path.join(out_dir, html_name)
                    self.result.insert(tkinter.END, html_name + "\n")
                    webbrowser.open('file://' + os.path.abspath(html_name)
                                    if sys.platform == "darwin" else html_name)
                else:
                    webbrowser.open('file://' + os.path.abspath(out_dir)
                                    if sys.platform == "darwin" else out_dir)
            self.worker = None

    def on_pick_src(self):
        if not self.worker or self.on_cancel():
            self.progress.set(0)
            self.names = list(tkinter.filedialog.askopenfilenames(
                title="Chose files to parse/compile",
                filetypes=[('All', '*')]
            ))
            if self.names:
                self.num_sources = len(self.names)
                self.num_compiled = 0
                self.outdir = os.path.join(os.path.dirname(self.names[0]), 'out')
                if not os.path.exists(self.outdir):  os.mkdir(self.outdir)
                with self.lock:  self.cancel_flag = False
                self.worker = threading.Thread(
                    target = dhparser_projectParser.batch_process,
                    args = (self.names, self.outdir),
                    kwargs = dict([('log_func', self.log_callback),
                                   ('cancel_func', self.cancel_callback)]))
                self.worker.start()
                self.cancel['stat'] = tkinter.NORMAL
                self.after(1000, self.poll_worker)

    def on_cancel(self) -> bool:
        if self.worker:
            if tkinter.messagebox.askyesno(
                title="Cancel?",
                message="A parsing/compilation-process is still under way!\n"
                        "Cancel running process?"):
                if self.worker:
                    with self.lock:  self.cancel_flag = True
                    self.result.insert(tkinter.END, "Canceling reaming tasks...\n")
                    self.update()
                    self.update_idletasks()
                    self.worker.join(5.0)
                    if not self.worker.is_alive():
                        self.result.insert(tkinter.END, "Stopped.\n")
                        self.cancel_flag = False
                    self.result.yview_moveto(1.0)
                    return True
                else:
                    with self.lock:  self.cancel_flag = False
                    return False
        return True

    def on_close(self):
        if self.on_cancel():
            if self.worker and self.worker.is_alive():
                self.result.insert(tkinter.END, "Killing still running processes!\n")
                self.result.yview_moveto(1.0)
            self.destroy()
            self.quit()


if __name__ == '__main__':
    # # Uncomment the following 3 lines before bundling this script with pyinstaller
    # access_presets()
    # set_preset_value('batch_processing_parallelization', False)
    # finalize_presets()

    if not dhparser_projectParser.main(called_from_app=True):
        app = dhparser_projectApp()
        app.mainloop()


import wolframalpha
from tkinter import *
from tkinter import ttk
import matplotlib
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import urllib.request
import base64
client = wolframalpha.Client('X969A9-QP6K293UUR')
style.use("ggplot")

class CollatioData():

    def __init__(self):
        self.img = NONE

    def transmit(self, textbox, frame):

        pos = textbox.index("end-1c linestart")
        res = client.query(textbox.get(pos, END))
        if len(res.pods) > 0:
            for pod in res.pods:
                if pod.text:
                    textbox.tag_configure('tag-right', justify='right')
                    textbox.insert(END, '\n' + pod.text + '\n', 'tag-right')
                    textbox.tag_configure('tag-left', justify='left')
                elif pod.img:
                    url = pod.img
                    response = urllib.request.urlopen(url)
                    data = response.read()
                    response.close()
                    b64_data = base64.encodebytes(data)
                    self.img = PhotoImage(data=b64_data)
                    label = Label(frame, image=self.img)
                    label.image = self.img
                    label.pack()


class CollatioGui(Frame):

    def __init__(self, online):
        self.gui = Tk()
        Frame.__init__(self)
        self.internetstate = online

        self.canvas = NONE
        self.frame = NONE
        self.vsb = NONE
        self.data = NONE
        self.nb = NONE
        self.page1 = NONE
        self.page2 = NONE
        self.textbox = NONE
        self.menubar = NONE
        self.file = NONE
        self.edit = NONE
        self.functions = NONE
        self.a = NONE
        self.initializegui()

    def initializegui(self):
        self.gui.title("Collatio")
        self.canvas = NONE
        self.frame = NONE
        self.vsb = NONE
        self.data = CollatioData()
        self.nb = ttk.Notebook(self.gui)
        self.page1 = ttk.Frame(self.nb)
        self.page2 = ttk.Frame(self.nb)
        scrollbar2 = Scrollbar(self.page1)
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.textbox = Text(self.page1, wrap=WORD, yscrollcommand=scrollbar2.set)
        self.menubar = Menu(self.gui)

        self.file = Menu(self.menubar, tearoff=0)
        self.edit = Menu(self.menubar, tearoff=0)
        self.functions = Menu(self.menubar, tearoff=0)

        self.file.add_command(label="Open", command=self.hello)
        self.file.add_command(label="Settings", command=self.settings)
        self.file.add_command(label="Offline Mode", command=self.getoffline)

        self.edit.add_command(label="Copy", command=self.hello)
        self.edit.add_command(label="Paste", command=self.hello)

        self.functions = Menu(self.menubar, tearoff=0)
        self.functions.add_command(label="Graph", command=self.graph)
        self.functions.add_command(label="Matrix", command=self.matdimsettings)

        self.menubar.add_cascade(label="File", menu=self.file)
        self.menubar.add_cascade(label="Edit", menu=self.edit)
        self.menubar.add_cascade(label="Functions", menu=self.functions)
        self.nb.add(self.page1, text='Main')

        self.canvas = Canvas(self.page2, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(self.page2, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onframeconfigure)
        self.nb.add(self.page2, text='More Info')

        button = Button(self.page1, text="Ask!", command=lambda: self.data.transmit(self.textbox, self.frame))
        self.textbox.bind("<Key>", self.key)

        self.nb.grid(row=0)
        self.nb.grid(row=0, column=1)

        self.textbox.pack()
        button.pack()
        self.gui.config(menu=self.menubar)

        self.gui.mainloop()

    def getoffline(self):
        self.internetstate = False;


    def getonline(self):
        self.internetstate = True

    def hello(self):
        print("hello")

    def graph(self):
        f = Figure(figsize=(5,5),dpi=100)
        self.a = f.add_subplot(111)
        self.a.plot([1,2,3,4,5,],[1,2,3,4,5])

        graphframe = Frame()
        configure = Button(graphframe,text="Configure", command=self.configuregraph)
        configure.pack()
        graph = FigureCanvasTkAgg(f, master=graphframe)

        self.nb.add(graphframe, text='Graph')
        graph.show()
        graph.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(graph, graphframe)
        toolbar.update()
        graph._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        self.nb.select(graphframe)

    def configuregraph(self):
        configgraphpage = Frame()
        num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20)
        for n in num:
            label = Label(configgraphpage, text="Graph {} :".format(n))
            text = Text(configgraphpage)
            text.configure(height=1,width=40)
            text.grid(row=n, column=2)
            label.grid(row=n)
        self.nb.add(configgraphpage, text='Configure(Graph)')
        self.nb.select(configgraphpage)
    def settings(self):
        settings = Tk()
        settings.title("Settings")
        settings.mainloop()

    def matdimsettings(self):
        matdim = Tk()
        matdim.title("Dimensions")
        rowlabel = Label(matdim, text="Rows: ")
        collabel = Label(matdim, text="Columns: ")
        rowtext = Text(matdim, width=3, height=1)
        coltext = Text(matdim, width=3, height=1)
        done = Button(matdim, text="Done")
        done.configure(width=6,height=1)
        operationlabel = Label(matdim, text="Operation")

        var1 = StringVar()
        var1.set("Select")
        operation = OptionMenu(matdim, var1,'Add.', 'Sub.', 'X', 'Inv')
        operation.configure(width=6,height=1)
        rowlabel.grid(row=0)
        rowtext.grid(row=0, column=1)
        collabel.grid(row=1)
        coltext.grid(row=1, column=1)
        done.grid(row=1,column=2)
        operation.grid(row=0,column=3)
        operationlabel.grid(row=0,column=2)
        matdim.mainloop()

    def key(self,event):
        if str(event.char) == '\r':
            self.data.transmit(self.textbox, self.frame)
    def onframeconfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
    def onframeconfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class CollatioController():
    def main(self):
        gui = CollatioGui(True)


if __name__ == '__main__':
    CollatioController().main()
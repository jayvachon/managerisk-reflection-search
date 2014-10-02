import os
import json
# from Tkinter import *
# import tkMessageBox

import Tkinter as tk

class GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.activeVar = tk.StringVar()
        self.activeVar.set(1)

        self._add_search()
        
        self.canvas = tk.Canvas(self, background="white", borderwidth=0, highlightthickness=0)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y", expand=False)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self)
        self.canvas.create_window(0, 0, anchor="nw", window=self.inner_frame, tags=("frame",))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self._add_listbox(10)

    def _on_canvas_resize(self, event=None):
        width = self.canvas.winfo_width()
        self.canvas.itemconfigure("frame", width=width)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _add_search(self):
        self.search_canvas = tk.Canvas(self)
        self.search_canvas.pack(side="left", fill="both", expand=True)
        searchbar = tk.Entry(self.search_canvas)
        searchbar.grid(row=0, column=0, sticky='ew')

        search_button = tk.Button(self.search_canvas, text="Search")
        search_button.grid(row=0, column=1, sticky='ew')

    def _add_listbox(self, count):
        listbox = tk.Listbox(self.inner_frame)
        for i in range(count):
            listbox.insert("end", "test " + str(i))
        listbox.grid(row=0, column=0, sticky='ew')

if __name__ == "__main__":
    root = tk.Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


# Grab reflections from submissions.json and perform a search
def getReflections(data):
	submissions = data["submissions"]
	reflections = []
	submissionsCount = len(submissions)
	for i in range(0, submissionsCount):
		a = submissions[i]["reflection"]
		a = a.encode('utf-8', 'ignore')
		reflections.append(a)
	return reflections

def searchForTerm(reflections, term):
	reflectionsCount = len(reflections)
	found = []
	term = term.lower()
	for i in range(reflectionsCount):
		t = reflections[i].lower()
		if t.find(term) > -1:
			found.append(reflections[i])
	return found

def getJSONData():
	json_data = open('submissions.json')
	data = json.load(json_data)
	return data

"""
# GUI stuff
def buildSearchFrame():
    
    # Frame
    searchFrame = Frame(root)
    searchFrame.grid(row=0, column=0, sticky='ew')

    # Search bar
    searchBar = Entry(searchFrame)
    searchBar.grid(row=0, column=0, sticky='ew')

    # Search button
    buttonSearch = Button(searchFrame, text="Search")
    buttonSearch.grid(row=0, column=1)
    
    searchFrame.pack()

def buildResultsFrame():
    resultsFrame = Frame(root) 

    entriesLabel = Label(resultsFrame)
    entriesLabel["text"] = "Found x entries"
    entriesLabel.grid(row=1, column=0)

    # Scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side = RIGHT, fill = Y)
    # listbox = Listbox(resultsFrame, yscrollcommand=scrollbar.set)
    # listbox.grid(row=2, column=0)
    # listbox.pack(side = LEFT, fill = BOTH)
    resultsFrame.pack()

if __name__ == "__main__":
    
    root = Tk()
    root.title('Risk Management Reflection Search')
    root.geometry("500x500")

    buildSearchFrame()
    buildResultsFrame()

    root.mainloop()


"""

##############################

"""

# Tkinter stuff by S.Prasanna
def displayText(reflections):
    
    
    global found
    global entryWidget
    global root

    term = entryWidget.get().strip()
    arr = searchForTerm(reflections, term)

    if term == "":
        tkMessageBox.showerror("omg", "ugh come on you have to write something in the freakin box!")
    else:
    	# Display number of entries found
        # w = Label(root, text = "Found " + str(len(arr)) + " entries")
        # w.pack()
        foundCount.set("Found " + str(len(arr)) + " entries")

        # Scrollbar
        scrollbar = Scrollbar(root)
        scrollbar.pack(side = RIGHT, fill = Y)
        
        # List entries
        listbox = Listbox(root, yscrollcommand=scrollbar.set)
        listbox.bind("<Double-Button-1>", selectReflection)
        count = min(len(arr), 50)
        for i in range(count):
            listbox.insert(END, str(i) + ". " + getReflectionSummary(arr[i]) + "...")
        listbox.pack(side = LEFT, fill = BOTH)
        listbox.config(width=75)
        scrollbar.config(command=listbox.yview)

def getReflectionSummary(reflection):
	return reflection[:100]

def selectReflection(event):
	print event.widget.curselection()

if __name__ == "__main__":

    root = Tk()

    root.title("Risk Horizon Reflection Search")
    root["padx"] = 40
    root["pady"] = 20       
    root["width"] = 960

    data = getJSONData()
    reflections = getReflections(data)
    arr = searchForTerm(reflections, "discuss")

    # Create a text frame to hold the text Label and the Entry widget
    textFrame = Frame(root)
    
    #Create a Label in textFrame
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Search:"
    entryLabel.pack(side=LEFT)

    # Create an Entry Widget in textFrame
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)

    textFrame.pack()

    foundCount = StringVar()
    foundCount.set("test")
    foundLabel = Label(root, text = foundCount).pack()

    button = Button(root, text="Submit", command = lambda: displayText(reflections))
    button.pack()

    root.mainloop()


"""

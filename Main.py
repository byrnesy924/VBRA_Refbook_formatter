from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import time
import pandas as pd
import re

ws = Tk()
ws.title('PythonGuides')
ws.geometry('1200x400')


def open_file():
    file_path = askopenfilename()
    if file_path is not None:
        pass
    file_path_display.delete("1.0","end")
    file_path_display.insert(END, file_path[0:3] + ".../" +  re.sub(".*\/([^\/]+)\/", "", file_path))

    # Handle file types
    global df, file_type
    if file_path[-4:] == '.csv':
        file_type = "csv"
        df = pd.read_csv(file_path)
    elif file_path[-5:] == '.xlsx':
        file_type = "xlsx"
        df = pd.read_excel(file_path)
    else:
        messagebox.showerror('File Type Error', 'Error: file is not a csv or xlsx')
        return
    print(df.head(5))
    print(df.columns)
    csv_display.delete("1.0", "end")
    csv_display_output.delete("1.0","end")
    csv_display.insert(END, df.head(5))
    return df

def competition_str_processor(string):
    if string[0:1] == 'U' and re.match("U18 BOYS", string):
        return "Sunday" + " " + re.sub("(\ BOYS).+", "", string)
    elif string[0:1] == "U" and re.match("(U1)([68])\ GIRLS", string):
        return "Tuesday" + " " + re.sub("(\ GIRLS).+", " Girls", string)
    elif string[0:1] == 'U':
        return "Saturday" + " " + re.sub("(\ BOYS).+|(\ GIRLS).+", "", string)
    return string.replace("/", "").title()

def division_str_processor(string):
    if re.match("(Division\ ).+", string) and not re.match("", string):
        return ""
    return string.title()

def remove_zero(string):
    return string.replace("0", "").replace(" / ", "/")

def competition_str_mapper(string):
    if re.match("(U8)|(U10)|(U12)|(U14)|(U16)", string):
        return "Waverley Junior Domestic"
    return "Waverley Senior Domestic"



def process_file(df):
    """This is a button function. It takes the csv and applies the changes. It then outputs it to the other text"""
    if not isinstance(df, pd.DataFrame):
        messagebox.showerror('Input Error', 'No file selected!')
    # Do some stuff to the df TODO
    # Create court
    df['Court_updated'] = df['Venue'] + df['Court'].apply(str).apply(lambda x: ' ' + x)

    # map venue
    venue_dictionary = {'ORC':'Oakleigh Recreation Centre', 'WAV': 'Waverley Basketball Stadium',
                        'ASB':'Ashburton Primary School'}
    # TODO: Qn - are there any other venues?
    df['Venue_updated'] = df['Venue'].apply(lambda x: venue_dictionary[x])

    # TODO: Qn - what are the other pay classes?
    payclass_dictionary = {'Juniors': 'Juniors Standard', 'Seniors': 'Seniors Standard'}
    df['Pay Class_updated'] = df['Pay Class'].apply(lambda x: payclass_dictionary[x])

    # Update the Division column --> format the competition column, format the division column, add comp to div, map
    # first apply this function to the "Competition" Column to get it to work correctly
    # TODO: Qn - is Tuesday U16's meant to be Waverley Senior Domestic?

    # iterrows - remove U18 division
    for index, row in df.iterrows():
        if row["Competition"][0:3] == "U18" or re.match("SUNDAY U/23", row["Competition"]):
            df.loc[index, "Division"] = ""

    # Apply - format the competition column
    df["Competition"] = df["Competition"].apply(lambda x: competition_str_processor(x))

    # Apply - remove junior divisions
    df["Division"] = df["Division"].apply(lambda x: division_str_processor(x))

    df["Division"] = df["Competition"] + " " + df["Division"].apply(lambda x: remove_zero(x))
    print(df[["Competition", "Division"]].iloc[160:190,:])

    #TODO : fix this junior domestic crap
    df["Competition"] = df["Competition"].apply(lambda x: competition_str_mapper(x))
    print(df[["Competition", "Division"]].iloc[160:190,:])



    csv_display_output.delete("1.0", "end")
    csv_display_output.insert(END, df.tail())

def save_file(df):
    save_file_path = asksaveasfilename()
    print(save_file_path)
    if file_type == "csv":
        df.to_csv(str(save_file_path + ".csv"))
    else:
        df.to_excel(str(save_file_path + ".xlsx"))

addcsv = Label(
    ws,
    text='Upload CSV or Excel from WBA '
)
addcsv.grid(row=0, column=1, padx=10)

addcsvbtn = Button(
    ws,
    text='Choose File',
    command=lambda: open_file()
)
addcsvbtn.grid(row=0, column=2)

file_path_display = Text(ws, height=1, width=50)
file_path_display.grid(row=0, column=3)

input_example = Label(
    ws,
    text='Input '
)
input_example.grid(row=3, column=1, padx=40)

output_example = Label(
    ws,
    text='Output '
)
output_example.grid(row=3, column=3, padx=40)

csv_display = Text(ws, height=9, width=50)
csv_display.grid(row=4, column=1, padx=10)

csv_display_output = Text(ws, height=9, width=50)
csv_display_output.grid(row=4, column=3, padx=10)

addcsvbtn = Button(
    ws,
    text='Process File',
    command=lambda: process_file(df=df)
)
addcsvbtn.grid(row=6, column=1, padx=10, pady=10)

save_file_btn = Button(
    ws,
    text='Save File',
    command=lambda: save_file(df=df)
)
save_file_btn.grid(row=6, column=3, padx=10, pady=10)

ws.mainloop()

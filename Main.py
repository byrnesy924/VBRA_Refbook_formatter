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
from tabulate import tabulate

pd.set_option("display.max_columns", 8)

def open_file():
    file_path = askopenfilename()
    if file_path is not None:
        pass
    file_path_display.delete("1.0", "end")
    file_path_display.insert(END, file_path[0:3] + ".../" + re.sub(".*\/([^\/]+)\/", "", file_path))

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
    csv_display.delete("1.0", "end")
    csv_display_output.delete("1.0", "end")
    csv_display.insert(END, df[["Competition", "Division", "Round", "Pay Class", "Venue", "Court"]].head(100).to_string(index=False))
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
    if re.match("(Division)", string):
        return ""
    return string.title()


def remove_zero(string):
    return string.replace("0", "").replace(" / ", "/").replace("O'35", "O'35s")


def reformat_O35s(string):
    return string.replace("O'35", "O35's")


def competition_str_mapper(string):
    if re.match("Saturday", string) or re.match("Tuesday U", string):
        return "Waverley Junior Domestic"
    return "Waverley Senior Domestic"


def process_file(df):
    """This is a button function. It takes the csv and applies the changes. It then outputs it to the other text"""
    if not isinstance(df, pd.DataFrame):
        messagebox.showerror('Input Error', 'No file selected!')
    # Create court
    df['Court'] = df['Venue'] + df['Court'].apply(str).apply(lambda x: ' ' + x)

    # map venue
    venue_dictionary = {'ORC': 'Oakleigh Recreation Centre', 'WAV': 'Waverley Basketball Stadium',
                        'ASB': 'Ashburton Primary School'}
    df['Venue'] = df['Venue'].apply(lambda x: venue_dictionary[x])

    payclass_dictionary = {'Juniors': 'Juniors Standard', 'Seniors': 'Seniors Standard'}
    df['Pay Class'] = df['Pay Class'].apply(lambda x: payclass_dictionary[x])

    # Update the Division column --> format the competition column, format the division column, add comp to div, map
    # iterrows - remove U18 division from the division column - replace with empty string
    for index, row in df.iterrows():
        if row["Competition"][0:3] == "U18" or re.match("SUNDAY U/23", row["Competition"]):
            df.loc[index, "Division"] = ""

    # Apply - format the competition column
    df["Competition"] = df["Competition"].apply(lambda x: competition_str_processor(x))

    # Apply - remove junior divisions
    df["Division"] = df["Division"].apply(lambda x: division_str_processor(x))

    # Remove the slashes or zeros from the Division and add on the competition name
    df["Division"] = df["Competition"] + " " + df["Division"].apply(lambda x: remove_zero(x))
    df["Division"] = df["Division"].apply(lambda x: reformat_O35s(x))

    # Convert the Competition to just Junior or Senior Domestic
    df["Competition"] = df["Competition"].apply(lambda x: competition_str_mapper(x))

    csv_display_output.delete("1.0", "end")
    csv_display_output.insert(END, df[["Competition", "Division", "Round", "Pay Class", "Venue", "Court"]]
                              .head(100)
                              .to_string(index=False))


def save_file(df):
    save_file_path = asksaveasfilename()
    df.to_excel(str(save_file_path + ".xlsx"))
    # Assume refbook only takes xlsx --> functionality can be added later
    # if file_type == "csv":
    #     df.to_csv(str(save_file_path + ".csv"))
    # else:
    #     df.to_excel(str(save_file_path + ".xlsx"))
    return


if __name__ == "__main__":
    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('1600x450')

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

    csv_display = Text(ws, height=20, width=70)
    csv_display.grid(row=4, column=1, padx=10)

    csv_display_output = Text(ws, height=20, width=100)
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

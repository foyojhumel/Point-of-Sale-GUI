import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import csv
import numpy as np
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import squarify
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


def main():
    Gui()

class Gui:
    def __init__(self):
        # Initialize creating a window and title
        self.root = tk.Tk()
        self.root.title("Store POS")

        # Using notebook function to create tabs
        notebook = ttkb.Notebook(self.root)
        style = ttkb.Style("flatly")
        style.configure('TNotebook.Tab', font=('URW Gothic L', '11', 'bold'))

        # New frame for tab 1, tab2 and tab3
        tab1 = ttkb.Frame(notebook)
        self.tab2 = tk.Frame(notebook)
        self.tab3 = tk.Frame(notebook)

        notebook.add(tab1, text= "POS")
        notebook.add(self.tab2, text= "Inventory")
        notebook.add(self.tab3, text="Dashboard")
        notebook.pack(expand= True, fill= "both")  #expand = expand to fill any space not otherwise used
                                       #fill = fill space on x and y axis

        # Creating window size with a 9:16 ratio
        self.width = 1280
        self.height = 920
        self.root.geometry(f"{self.width}x{self.height}")

        # Functionalities and design of tab1 POS
        # Window Label
        self.label = ttkb.Label(tab1, text= "                               YoGurtIt",
                                font= ("Lucida Console", 24), bootstyle= ("primary", "inverse"))
        self.label.grid(row=0, rowspan= 1, columnspan=10, sticky= "nsew")

        # DEBUG - StringVar only accepts str data types
        # For display items on screen
        self.display_number = tk.StringVar()
        # Getting values (as a str) of sub-total prices
        self.sub_price = tk.StringVar()
        # Getting value for amount to be paid
        self.sub_payment = tk.StringVar()
        # For confirmation of cash payment
        self.cash = tk.StringVar()
        
        # For display of selected items by customer
        self.display_entry = ttk.Treeview(tab1, height=5)
        self.display_entry.grid(row=1, column=0, rowspan=3, columnspan=6, sticky="nsew")
        # For display of total price, amount paid and change
        self.display_total_price = ttk.Treeview(tab1, height=1, show="tree")
        self.display_total_price.grid(row=4, rowspan=1, columnspan=6, sticky="nsew")

        # Setting columns of display_entry Treeview
        self.display_entry['columns'] = ('quantity', 'item','price')
        self.display_entry.column("#0", width=0,  stretch="no")
        self.display_entry.column("quantity", anchor="center", width=60)
        self.display_entry.column("item", anchor="center", width=120)
        self.display_entry.column("price", anchor="center", width=60)

        self.display_entry.heading("#0", text="", anchor="center")
        self.display_entry.heading("quantity", text="Quantity", anchor="center")
        self.display_entry.heading("item", text="Item", anchor="center")
        self.display_entry.heading("price", text="Price", anchor="center")

        # Setting columns of display_total_price Treeview
        self.display_total_price['columns'] = ('null', 'name','price')
        self.display_total_price.column("#0", width=0,  stretch="no")
        self.display_total_price.column("null", anchor="center", width=80)
        self.display_total_price.column("name", anchor="e", width=80)
        self.display_total_price.column("price", anchor="center", width=80)
        # Pre setting total price, amount paid and change as label to the display_total_price treeview
        self.display_total_price.insert(parent="", index="end", iid=0, text="", value=("", "Total Price:"))
        self.display_total_price.insert(parent="", index="end", iid=1, text="", value=("", "Amount Paid:"))
        self.display_total_price.insert(parent="", index="end", iid=2, text="", value=("", "Change:"))

        # Manipulating height of entries in the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(20))
        style.configure("Treeview", font=(None, 16), rowheight=int(28))

        # Creating number, size and toppings buttons
        # toppings button is color coded (if applicable) for fruits, crunches and sauces
        self.buttons = [
            ("9", 1, 6), ("8", 1, 7), ("7", 1, 8), ("DEL", 1, 9),
            ("6", 2, 6), ("5", 2, 7), ("4", 2, 8), ("ENTER", 2, 9, 2, 1),
            ("3", 3, 6), ("2", 3, 7), ("1", 3, 8),
            ("0", 4, 6), ("CASH", 4, 7), ("E-CASH", 4, 8), ("SAVE", 4, 9),
            ("SMALL", 5, 0, 1, 4), ("MEDIUM", 5, 4, 1, 3), ("LARGE", 5, 7, 1, 3),
            ("BANANA", 6, 0), ("MANGO", 6, 1), ("APPLE", 6, 2), ("NUTS", 6, 3),
            ("GRANOLA", 6, 4), ("COOKIES", 6, 5), ("CHOCO CHIPS", 6, 6), ("CHOCO SYRUP", 6, 7),
            ("CARAMEL SYRUP", 6, 8), ("MAPLE SYRUP", 6, 9)
        ] 

        for button_info in self.buttons:
            button_text, row, col = button_info[:3]
            row_span = button_info[3] if len(button_info) == 5 else 1
            col_span = button_info[4] if len(button_info) == 5 else 1
            button_style = ttkb.Style() 
            if button_text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                boot_style = ("info")
                button_style.configure("info.TButton", font=("Source Sans Pro", 18))
            elif button_text in ["DEL", "CASH", "E-CASH"]:
                boot_style = ("dark")
                button_style.configure("dark.TButton", font=("Source Sans Pro", 18))
            elif button_text in ["ENTER", "SAVE"]:
                boot_style = ("success")
                button_style.configure("success.TButton", font=("Source Sans Pro", 18))
            elif button_text in size_price.keys():
                boot_style = ("danger")
                button_style.configure("danger.TButton", font=("Source Sans Pro", 21))
            else:
                boot_style = ("warning")
                button_style.configure("warning.TButton", font=("Source Sans Pro", 12))
            button = ttkb.Button(tab1, text=button_text, command=lambda text=button_text: self.button_handler(text),
                                 bootstyle=boot_style, style= f"{boot_style}.TButton")
            button.grid(row=row, column=col, rowspan=row_span, columnspan=col_span, sticky="nsew", padx= 1, pady= 1)
        
        #tab1_but = ttkb.Style()
        #tab1_but.configure("tab1.TButton", font= ("Source Sans Pro", 12))

        # Automatic resizing screen and buttons
        for i in range(7):
            tab1.grid_rowconfigure(i, weight= 1)
        for i in range(10):
            tab1.grid_columnconfigure(i, weight= 1)

        
        # Functionalities and design for tab2 Inventory
        # For each item - text, row, column, columnspan, font, bootstyle
        texts = [["Cup Size", 1, 1, 2, 16, ("primary", "inverse")], ["                 Current Quantity", 1, 4, 1, 16, ("success", "inverse")],
                 ["Small", 2, 2, 1, 16, ("info")], ["Medium", 3, 2, 1, 16, ("info")], ["Large", 4, 2, 1, 16, ("info")],
                 ["Fruits", 5, 1, 2, 16, ("primary", "inverse")], ["Banana", 6, 2, 1, 16, ("info")], ["Mango", 7, 2, 1, 16, ("info")],
                 ["Apple", 8, 2, 1, 16, ("info")], ["Crunches", 9, 1, 2, 16, ("primary", "inverse")], ["Nuts", 10, 2, 1, 16, ("info")],
                 ["Granola", 11, 2, 1, 16, ("info")], ["Cookies", 12, 2, 1, 16, ("info")], ["Choco Chips", 13, 2, 1, 16, ("info")],
                 ["Sauces", 14, 1, 2, 16, ("primary", "inverse")], ["Choco Syrup", 15, 2, 1, 16, ("info")], ["Caramel Syrup", 16, 2, 1, 16, ("info")],
                 ["Maple Syrup", 17, 2, 1, 16, ("info")]]
        
        for text in texts:
            self.tab2_t = ttkb.Label(self.tab2, text= text[0], font= ("Source Sans Pro", text[4]), bootstyle= text[5])
            self.tab2_t.grid(row=text[1], column= text[2], columnspan= text[3], sticky="nsew")

        # Entry field for inventory tab
        global entry_fields
        entry_fields = [["small", 2], ["medium", 3], ["large", 4],
                        ["banana", 6], ["mango", 7], ["apple", 8],
                        ["nuts", 10], ["granola", 11], ["cookies", 12], ["choco_chips", 13],
                        ["choco_syrup", 15], ["caramel_syrup", 16], ["maple_syrup", 17]]
        
        # Naming all the entry widgets that the for loop will create
        global entry_names
        entry_names = {}

        
        for entry in entry_fields:
            self.tab2_e = ttkb.Entry(self.tab2, font= ("Source Sans Pro", 16), justify= "center", bootstyle= "secondary")
            self.tab2_e.insert(0, "0")
            self.tab2_e.grid(row= entry[1], column= 3, rowspan= 1, columnspan= 1, sticky= "nsew")
            entry_names[entry[0]] = self.tab2_e

        # Save button of inputs
        #save_but_style = ttkb.Style()
        #save_but_style.configure("dark.Tbutton", font= (("Source Sans Pro", 8)))
        save_button = ttkb.Button(self.tab2, text= "SAVE INPUT", command= lambda text="SAVE INPUT": self.button_handler(text),
                                 style= "dark.TButton")
        save_button.grid(row= 18, column= 3, rowspan= 1, columnspan= 1, sticky= "nsew")

        #but_style = ttk.Style()
        #but_style.configure("tab2.TButton", font= ("Source Sans Pro", 16))

        self.entry_quan = tk.IntVar()
        self.quan_display(self.entry_quan, self.tab2)

        for i in range(20):
            self.tab2.grid_rowconfigure(i, weight= 1)
        for i in range(6):
            self.tab2.grid_columnconfigure(i, weight= 1)


        # Dashboard
        sales = df_checker("sales.csv")
        chart_toppings = df_checker("toppings.csv")

        # Setting parameters of figures
        plt.rcParams["figure.figsize"] = [1, 1]

        # Creating frame for the first three graphs
        upper_frame = tk.Frame(self.tab3)
        upper_frame.pack(side= "top", fill= "both", expand= True)

        # Histogram for figure 1   
        chart_generator(title= "Number of Sales by Hour", frame= upper_frame, ylabel= "Number of Sales",
                        xlabel= "Time (24-hour format)")
        ax.hist(sales["Time"], bins= list(range(24)), edgecolor= "black")
        ax.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.6)
        

        # Barplot for figure 2
        # Creating a new column that is values of Date column but of datetime datatype
        sales["date_column"] = pd.to_datetime(sales["Date"])
        # Creating again a new column that is the day name values of datetime datatype
        sales["day"] = sales["date_column"].dt.day_name()
        # Initilizes the categories and their sequence to be used for barplot
        bar_categories = {"Monday": "Mon.", "Tuesday": "Tue.", "Wednesday": "Wed.", "Thursday": "Thu.",
                          "Friday": "Fri.", "Saturday": "Sat.", "Sunday": "Sun."}
        # Changing the sequence of resulted index of calling value_counts
        weekday_counts = sales["day"].value_counts().reindex(bar_categories.keys())

        chart_generator(title= "Number of Sales per Days of the Week", frame= upper_frame, ylabel= "Number of Sales")
        ax.bar(bar_categories.values(), weekday_counts.values)
        # Here is the other way of calling bar plot --> weekday_counts.plot(kind= "bar", ax= ax2)
        # Sets x-axis to rotation of 45degrees
        ax.tick_params(axis= "x", rotation= 45)
        # Displays count labels for each bar
        for i in range(len(bar_categories)):
            plt.text(i, weekday_counts.values[i] + 0.5, weekday_counts.values[i], fontsize = 10,
                     color ='black', ha= "center")

        # Line plot for figure 3
        sales["month"] = sales["date_column"].dt.month_name()
        months = {"January": "Jan.", "February": "Feb.", "March": "Mar.", "April": "Apr.", "May": "May",
                  "June": "Jun.", "July": "Jul.", "August": "Aug.", "September": "Sep.", "October": "Oct.",
                  "November": "Nov.", "December": "Dec."}
        month_sales = sales["month"].value_counts().reindex(months.keys())

        chart_generator(title= "Number of Sales per Month", frame= upper_frame, ylabel= "Number of Sales")
        ax.plot(months.values(), month_sales.values, marker= "o")
        ax.tick_params(axis= "x", rotation= 45)
        # Displays values for each line point
        for x_value, y_value in zip(ax.lines[0].get_xdata(), ax.lines[0].get_ydata()):
            ax.annotate(f"{y_value:.0f}", xy= (x_value, y_value + 1), fontsize = 10, color ='black', ha= "center", va= "bottom")

        # Creating frame for the last two graphs
        lower_frame = tk.Frame(self.tab3)
        lower_frame.pack(side= "bottom", fill= "both", expand= True)

        # TreeMap for figure 4
        sizes = ["SMALL", "MEDIUM", "LARGE"]
        size_colors = ["orange", "blue", "gray"]
        size_sales = sales["Size"].value_counts(normalize= True).reindex(sizes)

        chart_generator(title= "Sales per Size", frame= lower_frame)
        squarify.plot(sizes= size_sales.values, label= sizes, value= [f'{(x * 100):.1f}%' for x in size_sales.values],
                      color= size_colors, alpha= 0.5, ec= "white", ax= ax, text_kwargs={'fontsize': 14})
        # Axes are not necessary for treemap so it is set to off
        ax.axis("off")

        # Horizontal bar plot for figure 5
        top_sales = chart_toppings["Topping"].value_counts(ascending= True)
        top_formatted = [top.replace(" ", "\n") for top in top_sales.index]

        chart_generator(title= "Number of Sales per Toppings", frame= lower_frame)
        ax.barh(top_formatted, top_sales.values)
        # Displays count value at the end of each horizontal bar
        for i, v in enumerate(top_sales.values):
            ax.text(v + 0.1, i, str(v), color='black', fontsize= 10, verticalalignment='center')


        self.root.mainloop()

    
    # DEBUG - separate sales count to items count
    global sales_count, item_count, item_list, size_price, top_cat, top_list, transformed_toppings
    sales_count = 0
    item_count = 0
    item_list = []
    size_price = {"SMALL": 79, "MEDIUM": 99, "LARGE": 149}
    top_cat = {"FRUITS":["BANANA", "MANGO", "APPLE"],
                         "CRUNCHIES":["NUTS", "GRANOLA", "COOKIES", "CHOCO CHIPS"],
                         "SAUCES":["CHOCO SYRUP", "CARAMEL SYRUP", "MAPLE SYRUP"]}
    top_list = [top for val in top_cat.values() for top in val]
    transformed_toppings = {"SMALL": "small", "MEDIUM": "medium", "LARGE": "large",
                            "BANANA": "banana", "MANGO": "mango", "APPLE": "apple",
                            "NUTS": "nuts", "GRANOLA": "granola", "COOKIES": "cookies",
                            "CHOCO CHIPS": "choco_chips", "CHOCO SYRUP": "choco_syrup",
                            "CARAMEL SYRUP": "caramel_syrup", "MAPLE SYRUP": "maple_syrup"}
    
    def quan_display(self, int_var, tab_number):
            for entry in entry_fields:
                int_var.set(df_checker("inventory.csv")[entry[0]].iloc[-1])
                self.tab2_quan = tk.Label(tab_number, text= int_var.get(),
                                        font= ("Source Sans Pro", 16), justify= "center")
                self.tab2_quan.grid(row= entry[1], column= 4, rowspan= 1, columnspan= 1, sticky= "nesw")

    # Handles how each button will behave.
    def button_handler(self, button):
        global sales_count, item_count, item_list, size_price, top_cat, top_list, transformed_toppings
        self.button = button
        self.num_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.input_quan = self.display_number.get()
        self.total_price = self.sub_price.get()
        self.total_payment = self.sub_payment.get()
        self.is_cash = self.cash.get()
        
        if self.button in self.num_buttons and self.is_cash == "":
            if self.button == "0" and self.input_quan == "":
                self.display_number.set("")
            elif self.button != "0" and self.input_quan == "":
                self.display_number.set(self.input_quan + self.button)
                self.display_entry.insert(parent="", index="end", iid=item_count, text="", value=(self.input_quan + self.button))
            elif self.button != "0" and self.input_quan != "":
                self.display_number.set(self.input_quan + self.button)
                self.display_entry.set(item_count, "quantity", (self.input_quan + self.button))
        if self.button in size_price.keys():
            initial_p = int(size_price[self.button]) * int(self.input_quan)
            self.display_entry.set(item_count, "item", self.button)
            self.display_entry.set(item_count, "price", initial_p)
            item_list.append([int(self.input_quan), self.button, initial_p])
            item_count += 1
            self.display_number.set("")
            # Checks if total price has value yet and create one if otherwise
            if self.total_price == "":
                self.display_total_price.set(0, "price", initial_p)
                self.sub_price.set(initial_p)
            else:
                self.display_total_price.set(0, "price", int(self.total_price) + initial_p)
                self.sub_price.set(int(self.total_price) + initial_p)
        # Using list comprehension to create a list collection of all values in the top_cat dictionary
        if self.button in top_list:
            #DEBUG - treated throwing error when size or topping is selected first without quantity
            try:
                item_list.append([int(self.input_quan), self.button, 0])
            except ValueError:
                messagebox.showerror("No Quantity Selected", "Please select quantity first before selecting size or toppings.")

            # Checks for the number of toppings per size purchased
            if toppings_checker(item_list):
                if quan_toppings_checker(item_list):
                    self.display_entry.set(item_count, "item", self.button)
                    self.display_entry.set(item_count, "price", "-")
                    item_count += 1
                    self.display_number.set("")
                else:
                    messagebox.showerror("Unavailable Number of Topping",
                                        "Selected topping quantity is unavailable, please select other topping or top up the inventory.")
                    item_list.pop()
                    self.display_entry.delete(item_count)
                    self.display_number.set("")
            else:
                messagebox.showerror("Exceeding Number of Toppings",
                                     "Total number of toppings exceeds applicable amount. Please enter additional size or proceed to payment.")
                # DEBUG - deletes the initial entry of quantity for exceeding additional topping
                item_list.pop()
                self.display_entry.delete(item_count)
                self.display_number.set("")
        if self.button == "DEL": 
            # Returns the row number of selected item in the treeview as a str
            row_id = self.display_entry.focus()
            if row_id != "":
                # Deletes the selected item in treeview
                self.display_entry.delete(row_id)
                # Also deletes the selected item in initial compilation of items for data_entry
                # DEBUG - handle error and gui hang up when deleting a record that has only quantity and no item yet
                # DEBUG - total_price not updating when you delete an item from treeview
                try:
                    self.display_total_price.set(0, "price", int(self.total_price) - item_list[int(row_id)][2])
                    self.sub_price.set(int(self.total_price) - item_list[int(row_id)][2])
                    del item_list[int(row_id)]
                # DEBUG - program hangs during delete of first row with quantity only due to conflict in display total price using ValueError
                except (IndexError, ValueError):
                    self.display_number.set("")
        # DEBUG - enter button throws error when e-cash is selected as payment
        if self.button == "E-CASH":
            self.sub_payment.set(self.total_price)
            self.display_total_price.set(1, "price", self.total_price)
        if self.button == "CASH":
            self.cash.set("CASH")
        if self.button in self.num_buttons and self.is_cash == "CASH":
            if self.button == "0" and self.total_payment == "":
                self.sub_payment.set("")
            else:
                self.sub_payment.set(self.total_payment + self.button)
                self.display_total_price.set(1, "price", self.total_payment + self.button)
        if self.button == "ENTER":
            # DEBUG - handles error during pushing enter button without value of amount paid
            try:
                change = int(self.total_payment) - int(self.total_price)
                if change < 0:
                    messagebox.showerror("Insufficient Amound Paid", "Not enough amount to be paid, please enter another amount.")
                    self.display_total_price.set(1, "price", "")
                    self.sub_payment.set("")
                elif self.total_payment != "":
                    self.display_total_price.set(2, "price", int(self.total_payment) - int(self.total_price))
                else:
                    self.display_total_price.set(2, "price", 0)
            except ValueError:
                messagebox.showerror("Amount Paid Problem", "Please input valid amount for payment.")
        if self.button == "SAVE":
            item_count = 0
            # Calls the function data saver to save input to a record
            size_data_saver()
            top_data_saver()
            sales_count += 1

            sales_update_inventory()

            # DEBUG- update also inventory quantities
            self.quan_display(self.entry_quan, self.tab2)

            # Initializes back to empty list the global item_list and top_list for next input
            item_list.clear()
            # Deletes all the display items, quantities and prices in the treeview
            self.display_entry.delete(*self.display_entry.get_children())
            # Sets collected initial total price to empty/whitespace
            self.sub_price.set("")
            # Sets collected sub payment to empty/whitespace
            self.sub_payment.set("")
            # Sets cash checker to empty str
            self.cash.set("")
            # KAIZEN - deletes entry in the total price after save button is selected
            # sets the total price, amount paid and change to whitespace since unable to delete the specific item of total price
            self.display_total_price.set(0, "price", "")
            self.display_total_price.set(1, "price", "")
            self.display_total_price.set(2, "price", "")
        if self.button == "SAVE INPUT":
            inventory_update()
            # Deletes quantity entry and sets entry fields back to 0
            for _, name in entry_names.items():
                name.delete(0, END)
                name.insert(0, "0")

            # DEBUG - Dynamically changes the current quantity after every inventory changes
            # DEBUG - error in calling function inside gui class
            self.quan_display(self.entry_quan, self.tab2)

        #print(item_list)

def toppings_checker(list_items):
    # Initializes numpy array for sizes small, medium and large
    init_size = np.array([0, 0, 0])
    # Initializes 2d numpy array for number of topping per size order
    #   Fruits, Crunches, Sauces
    top_num = np.array([[0, 1, 1],
                        [1, 2, 1],
                        [3, 2, 1]])
    # Initializes order of toppings for fruits, crunches and sauces
    top_order = np.array([0, 0, 0])
    # Initializes container for all the toppings allowable per size purchased in
    #   fruits, crunches and sauces order
    init_topsize = np.array([0, 0, 0])

    for item in list_items:
        if item[1] in size_price.keys():
            match item[1]:
                case "SMALL":
                    init_size[0] += item[0]
                case "MEDIUM":
                    init_size[1] += item[0]
                case "LARGE":
                    init_size[2] += item[0]
        elif item[1] in top_list:
            match item[1]:
                case "BANANA" | "MANGO" | "APPLE":
                    top_order[0] += item[0]
                case "NUTS" | "GRANOLA" | "COOKIES" | "CHOCO CHIPS":
                    top_order[1] += item[0]
                case "CHOCO SYRUP" | "CARAMEL SYRUP" | "MAPLE SYRUP":
                    top_order[2] += item[0]
    
    init_topsize += (init_size[0] * top_num[0, :]) + (init_size[1] * top_num[1, :]) + (init_size[2] * top_num[2, :])

    return init_topsize.sum() >= top_order.sum()

def quan_toppings_checker(list_items):
    if list_items[-1][1] in transformed_toppings.keys():
        return (df_checker("inventory.csv")[transformed_toppings[list_items[-1][1]]].iloc[-1] - list_items[-1][0]) >= 0

# Compiles all entries in the list to a dictionary to be iterated by writerow function
def size_list_to_dict(list_entry):
    global size_price
    size_data_for_entry = []

    for item in list_entry:
        if item[1] in size_price.keys():
            size_data_for_entry.append({"Order_Number": sales_count, "Date": date.today(), "Time": datetime.now().hour, 
                                        "Quantity": item[0], "Size": item[1], "Total_Price": item[2]})
    return size_data_for_entry
        
def top_list_to_dict(list_entry):
    global top_list
    top_data_for_entry = []

    for item in list_entry:
        if item[1] in top_list:
            top_data_for_entry.append({"Order_Number": sales_count, "Date": date.today(), "Time": datetime.now().hour, 
                                       "Quantity": item[0], "Topping": item[1]})
    return top_data_for_entry

def size_data_saver():
    # Accessing the items and price handled by buttons for each transactions (before pushing save button)
    global item_list

    with open("sales.csv", "a", newline= "") as file:
        fieldnames = ["Order_Number", "Date", "Time", "Quantity", "Size", "Total_Price"]
        writer = csv.DictWriter(file, fieldnames= fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for _ in size_list_to_dict(item_list):
            writer.writerow(_)

def top_data_saver():
    global item_list

    with open("toppings.csv", "a", newline= "") as file:
        fieldnames = ["Order_Number", "Date", "Time", "Quantity", "Topping"]
        writer = csv.DictWriter(file, fieldnames= fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for _ in top_list_to_dict(item_list):
            writer.writerow(_)

global inventory_field_names
inventory_field_names = ["date", "time", "small", "medium", "large", "banana", "mango", "apple", "nuts",
                          "granola", "cookies", "choco_chips", "choco_syrup", "caramel_syrup", "maple_syrup"]

def df_checker(file_name):
    try:
        inv_df = pd.read_csv(file_name)
    except FileNotFoundError:
        with open(file_name, "w", newline= "") as file:
            fieldnames = inventory_field_names
            writer = csv.DictWriter(file, fieldnames= fieldnames)
            writer.writeheader()
        inv_df = pd.read_csv(file_name)
    return inv_df

def inventory_update():
    global entry_names

    # Initializes dictionary for inventory input
    dict_inv = {"date": date.today(), "time": datetime.now().hour}

    # Appends all the inputs in inventory entry field for update to the file
    for entry, name in entry_names.items():
        try:
            dict_inv[entry] = df_checker("inventory.csv")[entry].iloc[-1] + int(name.get())
        except (ValueError, IndexError):
            dict_inv[entry] = int(name.get())
        
    # Appends the collected values to the inventory file
    with open("inventory.csv", "a", newline= "") as file:
        fieldnames = inventory_field_names
        writer = csv.DictWriter(file, fieldnames= fieldnames)
        writer.writerow(dict_inv)

def sales_update_inventory():
    global item_list, transformed_toppings

    # Initializes dictionary for inventory input
    dict_sales_update = {"date": date.today(), "time": datetime.now().hour}

    inv = ["small", "medium", "large", "banana", "mango", "apple", "nuts", "granola", "cookies",
           "choco_chips", "choco_syrup", "caramel_syrup", "maple_syrup"]

    # Appends all the inputs in inventory entry field for update to the file
    for category in inv:
        dict_sales_update[category] = df_checker("inventory.csv")[category].iloc[-1]
    
    for item in item_list:
        dict_sales_update[transformed_toppings[item[1]]] -= item[0]

    # Appends the collected values to the inventory file
    with open("inventory.csv", "a", newline= "") as file:
        fieldnames = inventory_field_names
        writer = csv.DictWriter(file, fieldnames= fieldnames)
        writer.writerow(dict_sales_update)


def chart_generator(title, frame, ylabel=None, xlabel=None):
    global ax
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    frame_position = tk.Frame(frame)
    frame_position.pack(side= "left", fill= "both", expand= True)
    canvas_position = FigureCanvasTkAgg(fig, frame_position)
    canvas_position.draw()
    canvas_position.get_tk_widget().pack(side= "left", fill= "both", expand= True)
        

if __name__ == "__main__":
    main()
# Store POS
#### [Here is the video demo](https://youtu.be/SScJPladFZg)
#### Description:
    Store POS is program that utilizes the graphical user interface functionality of Python programming language to create an interaction between the user and application.

    It assists small stores in everyday sales transaction and automatic sales data keeping as in inventory. It also shows sales data visualization that will help store owners analyze how well the business is doing.

    In this particular project, a yogurt store is selected to tackle complication of not just selecting quantities of yogurt cup sizes but also their amount of toppings per size. Here is the yogurt store offerings for number of toppings per purchased cup sizes as well as their prices:
        Small - two (2) toppings, 79
        Medium - four (4) toppings, 99
        Large - six (6) toppings, 149

    For every selection of cup size, succeeding selection of toppings must not exceed the offered number or else the business will fall into bankruptcy! But don't worry for our program handles all of it and flashes warning and messages to user.

***customer from here within points to people making orders in our shop***

***cashier will then point to people who uses our GUI***

#### **Functionality:**
Store POS graphical user interface (GUI) has three tabs: main, inventory and dashboard.

#### **Main tab (POS)**
The main tab, point-of-sale is written inside a class of object_oriented programming. It is concised into a grid function of tkinter library to place every buttons and treeview neatly on the main tab. With treeview, a method in tkinter library, transactions can be visualized as well as the functionalities like addition of prices and subtraction of the total price to the amount being paid. Commands of every buttons is also housed inside the class of GUI.

Buttons 0-9 is for selection of customer order quantities as well as payment input. 'DEL' button clears input in the treeview if the user wishes to discard it. 'CASH' button tells the program that the user is done selecting sizes and toppings and will treat inputs of button 0-9 as payments and not quantities anymore. With the electronic payment becoming widely accepted and implemented in today's world, 'E-CASH' button is also implemented. Customer may pay electronically and upon cashier confirmation of payment, he/she can select 'E-CASH' button and it will automatically copy the total price to the payment row and no need for manually inputting the paid amount in our GUI. 'ENTER' button functions as last part of transactions as it subtracts the total price to the amount paid to show how much change must be given to customer if there is any else it will show 0. Selecting 'ENTER' button without the input in amount paid will throw a warning message about no payment being done. 'SAVE' button collects and keep entry of all purchased yogurt in every transactions: quantity, number of cup size, number of toppings, to keep track of sales history to be used in sales visualization on dashboard tab and entry for inventory files to be shown in inventory tab.
It also marks the end of every transactions as it clears all the entry in the treeview.

Complexity of transactions as to not exceed the offered number of toppings per cup purchased is handled by functions, each for every checker like:
1. Checking for number of toppings per cup size purchased e.g. if one small yogurt cup is purchased, only two toppings can be added to the treeview transaction viewer, any additional toppings selected after will show message about the number limit of toppings.
2. Availability of cup sizes and toppings are being checked first from the inventory file. After every transactions, each one is updated and for the next transaction selecting a cup size or topping that is of zero quantity based on inventory file will show a warning message.

#### **Inventory tab**
Inventory tab shows all the current quantity of each cup sizes and toppings. Adding and subtracting quantities to the inventory is handled by tab. It dynamically displays all the current quantity after adding and subtracting from this tab and also after every transactions from the main tab.

#### **Dashboard tab**
Five graphics are shown in the dashboard tab to show how well the business is doing based on sales history created from the main tab.
- Histogram - shows the accumulated sales per hour of the day. It will tell the owner which hour of the day the business has the most and least sales. Scheduling of business operations can be adjusted based on this visualization to get advantage of the hour when most sales can be achieved.
- Bar graph - shows the accumulated sales per day of the week. It shows what days are the most and least profitable, giving feedback to the owner which day an employee day off can be permitted when the sale is historically low.
- Line graph - shows the accumulated sales per month. Comparison can be done per monthly sales to see if other gimmicks must be done to push the sales up.
- Tree map - shows the total sales per cup sizes. Owner can see what cup size is the most and least profitable. He/she then can decide if the number of toppings per cup size must be changed to attract customers to purchase the size with the least sale. Tree map is selected here as type of graphic because it has only three categories which is few for another bar graph, and also to make visual appeal which will not be achieved if another bar graph is being used.
- Horizontal bar graph - shows the total sales per toppings. It is the most important part of dashboard as it shows the owner what toppings do good and what is/are not. Inventory of most purchased toppings can be increased to avoid non-availability as it is the most wanted by customers and for least purchased toppings, the owner can change it to new topping/s.

#### **Debug**
During the course of writing and testing the program about differently possibility of how the user will operate the GUI, several functionalities are being implemented to handle things like program hang up and malfunction if certain button is being clicked before or after a certain button is clicked. Here are some of the debug being implemented:
1. Showing error message to handle throwing error when size or topping is selected first without quantity.
2. Adding functionality that deletes automatically the initial entry where topping selected and showed at treeview exceeds the offered number of toppings per cup size purchased after showing an error message.
3. Handles error and hang up of GUI when deleting a record that has only quantity and no item yet.
4. Handles error of total price row in main tab not updating when you delete an item from treeview.
5. Manages program hang up during deletion of first row with quantity only due to conflict in display total price using exception ValueError.
6. Displays error message during selecting of 'ENTER' button without inputting value of amount paid first or choosing 'E-CASH' in case of electronic payment.

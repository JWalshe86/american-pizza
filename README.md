# AMERICAN PIZZA - ORDER SYSTEM
## OVERVIEW
I created a fully functional order system for a fictional restaurant called American Pizza, whose field of activity is the preparation and serving of pizza inspired by american fast-food. The main purpose of this program is to facilitate the process of taking orders by introducing a system that automatically populate a google spreadsheet with data about each order for a better monitoring. Also it is very useful for the restaurant's clients because it estimates the waiting time for each order and it gives them the option to check their order status live.
American Pizza order system was created entirely with Python and cand be used through the terminal implemented with the Code Institute Python Template whose design was adapted to respect the restaurant theme.
<br><br>
The fully deployed project can be accesed at [this link](https://american-pizza-order-system.herokuapp.com/).<br>
<hr>

[![N|Solid](assets/images/full_image.JPG)](assets/images/full_image.JPG)
<hr>

## UX/UI
### STRATEGY
#### Goals<br>
* The program should be intuitive to navigate<br>
* The informations that appear on the screen should be relevant for each step of the order<br>
* Instructions should appear to sugerate the user what values to enter<br>
* The important informations should be highlighted to offer a better user experience<br>
* The program should access the right data sheet for every step <br>
* the program should update the Orders data sheet with the right values<br>
* The order content and price has to be displayed to the user before the order is finished<br>
* The order duration time has to be calculated and displayed to the user after the order is finished<br>
* The program should give the possibility of checking the status of the order

#### User Stories<br>
* As a user, I want to see informations about the pizza options that the restaurant offer<br>
* As a user, I want be able to create my own custom pizza<br>
* As a user, I want to be able to add more type of pizzas to my order<br>
* As a user, I want to see the content of my order when deciding to add more food.<br>
* As a user, I want to be able to choose the quantity for each pizza<br>
* As a user, I want to see informations about the total price and duration of the order<br>
* As a user, I want to be assigned a code for my order<br>
* As a user, I want to check my order status<br>

### SCOPE<br>
For the implementation of the ordering system I have planned the following features:<br>

* Data from spreadsheet about pizzas characteristics to be displayed to the user in tables<br>
* The Create Your Own pizza option that adds extra steps for the order<br>
* The user's options will be writen on the screen<br>
* The program displays warnings when the input of the user doesn't respect the format<br>
* The option of displaying the order content <br>
* The program calculates and displays the order total price<br>
* The program calculates and displays the order total duration<br>
* The program assign a number refference to the order<br>
* A table with the orders status can be displayed<br>

### STRUCTURE<br>
The ordering system can be used by the clients through a mock terminal that appears when the link is accessed.
The terminal was created using the Code Institute template which is not my work but his <code>CSS</code> code has been adjusted to conform it's design with the restaurant theme.
Apart from that, the program was made with <code>Python</code> as the only programming language used. The file which stores the entire code that appears in the terminal is named <code>run.py</code> and this is what Heroku will run when the program is used.<br>

### FLOWCHARTS<br>
The Flowchart for my program was created using <b>LucidChart</b> and it visually represents how the system works.<br>
[![N|Solid](assets/images/blank_diagram.jpeg)](assets/images/blank_diagram.jpeg)

### SURFACE/DESIGN<br>
The ordering system displays pages as steps of completing the order. Every page contains informations relevant to the user and a menu that will help him navigate through the program.<br>
#### Pizza Menu Page
* When the user first launches the program a welcome message is displayed and the pizza menu table.<br>
<img src="assets/images/menu.JPG" width="80%"><br>

#### Pizza Sizes Page
* In this step the user can see information about sizes and prices for the pizza.<br>
<img src="assets/images/sizes.JPG" width="80%"><br><br>

If the user choose the option of Create Your Own pizza, three more aditional steps are added to the process.<br>
#### Pizza Sauces Page
* The user can see sauces option as the first step in creating a custom pizza. <br>
<img src="assets/images/sauce.JPG" width="80%"><br>

#### Pizza Cheese Page
* A table with cheese options is displayed to the user as the second aditional step.<br>
<img src="assets/images/cheese.JPG" width="80%"><br>

#### Pizza Topings Page
* In this step the user can choose up to 5 topings for his custom pizza.<br>
<img src="assets/images/topings.jpg" width="80%"><br>

#### Pizza Quantity Page
* Choosing a number for the quantity of pizza the client wants is one of the last steps in completing the order.<br>
<img src="assets/images/quantity.JPG" width="80%"><br>

#### Order Overview Page
* Before finishing the order, the user can see his order content and it's final price and it is given the option of adding to the order.<br>
<img src="assets/images/overview.JPG" width="80%"><br>

#### Pizza Final Menu Page
* After processing the order, the client is informed about his number refference and the estimated time.<br>
<img src="assets/images/finish.JPG" width="80%"><br>

#### Pizza Orders Live Status Page
* As an aditional step every user can access a Live Status table that updates its values every time it is loaded.<br>
<img src="assets/images/status.JPG" width="80%"><br>
<hr>
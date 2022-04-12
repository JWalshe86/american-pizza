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
For the implementation of the ordering system I have planned the following features:

* Data from spreadsheet about pizzas characteristics to be displayed to the user in tables
* The Create Your Own pizza option that adds extra steps for the order
* The user's options will be writen on the screen
* The program displays warnings when the input of the user doesn't respect the format
* The option of displaying the order content 
* The program calculates and displays the order total price
* The program calculates and displays the order total duration
* The program assign a number refference to the order
* A table with the orders status can be displayed

### STRUCTURE<br>
The ordering system can be used by the clients through a mock terminal that appears when the link is accessed.
The terminal was created using the Code Institute template which is not my work but his <code>CSS</code> code has been adjusted to conform it's design with the restaurant theme.
Apart from that, the program was made with <code>Python</code> as the only programming language used. The file which stores the entire code that appears in the terminal is named <code>run.py</code> and this is what Heroku will run when the program is used.

 

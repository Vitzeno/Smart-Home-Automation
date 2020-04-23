
# Smart Home Automation

This project aims to develop a system that both monitors energy usage within the home and provides tools for control and actuation of various household appliances, accessed via a central mobile application. The project utilises OpenEnergyMonitor’s emonhub and emon sensors to collect energy usage and temperature / humidity readings from the user’s home and store this data. The mobile application will allow users to control devices but has a focus on end user programming, to allow the user to create custom rules for devices that respond to triggers in the home. An example might be to turn on an electric heater if the temperature in a room drops below a threshold defined by the user.

## Server/Hub

The hub is an always running multithreaded program running on the Raspberry Pi consisting of various key components. It uses Bluetooth (BT) particularly the Radio Frequency Communication (RFCOMM) protocol which provides a simple and reliable high-level data stream with built in flow control using a credit-based system, and a simple protocol was develop to allow for efficent communications between the server and the mobile application.

To allow for end user programming a simple context free grammar (CFG) was first defined which uses postfix notation for operators. The grammar supports both binary and unary operators and allows for infinite nesting of expression. The server must be able to evaluate user created rules and rules should be simple to communicate over the bluetooth medium. Because of this the parser, which manages the communications protocol and the rule evaluator have slightly different grammar definitions. Whilst the semantics are identical, the syntax for binary operators differ slightly as seen below:

### Grammar for parser

Rule => Expr Expr BinOp | Expr
Expr => Expr | Expr UnOp | Expr Expr BinOp | Expr Digit BinOp
Digit => [0-9]+
BinOp => GE | LE | EQ | AND | OR
UnOp => NOT

### Grammar for rule evaluator

Rule => Expr Expr BinOp | Expr
Expr => Expr | Expr UnOp | Expr Expr BinOp | Expr Digit BinOp
Digit => [0-9]+
BinOp => > | < | = | AND | OR
UnOp => NOT

## Mobile Application

-Make sure location permissions are granted for application to work
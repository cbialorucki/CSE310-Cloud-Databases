# Overview

This is a very simple, cloud-based account management system written in Python. It uses a CLI program to interact with a Google Firestore database. People can create accounts, and users can change information relating to their account such as their name, email address, password, or phone number. Users can also delete their account from the cloud database.

This project was designed to teach myself about how to use a cloud database, like Firebase. Many cloud databases are NoSQL databases, so I chose a cloud database that was NoSQL. Between this project and the [CSE-310-SQL-Relational-Database](https://github.com/Ticomware/CSE310-SQL-Relational-Database) project, I have developped an understanding and appreciation for both SQL and NoSQL databases.

[Software Demo Video](https://www.youtube.com/watch?v=lt5GPL2PJFA)

# Cloud Database

For this project, I am using a Firestore database, which is part of Google's Firebase service.

This database consists of a `users` collection, which has several documents with a random ID. Each document represents a user account. The document contains a few attributes.

  * `Email` The email address for the user.
  * `Name` The name stored for the user account.
  * `Password` The password for the user account, stored in plaintext.
  * `Phone` The phone number stored for the user account, without any formatting, as a string.

# Development Environment

IDE
* [Visual Studio Code](https://code.visualstudio.com/)

Programming Language and Libraries
* [Python](https://www.python.org/)
* [Firebase Admin](https://firebase.google.com/docs/database/admin/start)

# Useful Websites

* [Firebase Cloud Platform Tutorial](https://www.youtube.com/watch?v=N0j6Fe2vAK4)
* [Stack Overflow](https://stackoverflow.com/)

# Future Work

* __Store passwords more securely__: Storing passwords in plaintext like in this project is a bad idea. Passwords can be stolen with very little effort. Do not use this with passwords you use frequently or for any commercial purpose.

* __Adding OAuth2 support__: OAuth2 is a protocol used by other service providers to authenticate users. It is commonly used to log in users with another service, like the "Log in with Google" or "Log in with Facebook" icons. Adding support for this protocol could make this login system more useful.

* __A Graphical User Interface (GUI)__: Graphical user interfaces are more intuitive than command-line driven applications for most users. Adding a graphical user interface will make the program more comfortable to use.

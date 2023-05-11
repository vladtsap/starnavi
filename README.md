# Starnavi

This repository contains the code for a social media application developed as a test task for Starnavi. 
The application consists of two components: 
a Django web application for social media functionality and an automated bot for creating users, posts, and liking them.

#### [Task description is available here](misc/Task_Description.pdf)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Features

- User registration and authentication
- Post creation and getting
- Like, unlike, and like counts for posts
- Analytics about user or likes per day
- Automated bot for creating users, posts, and liking activity


## Installation

To install and run the application, follow these steps:

1. Clone the repository:

   ```bash
   $ git clone https://github.com/vladtsap/starnavi.git
   ```
   
2. Run the application using Docker Compose:

   ```bash
   $ docker-compose up --build
   ```

3. Run the automated bot:

   ```bash
   $ python automated_bot.py
   ```


## Usage

For the detailed description of the API endpoints, please refer to the [API documentation](https://www.postman.com/vladtsap/workspace/worldwide-workspace/collection/5723895-ac76a9b1-c416-407f-8af1-331a079f8955).

Also, you can import [Postman collection](misc/Starnavi_Test_Task.postman_collection.json) to your client.

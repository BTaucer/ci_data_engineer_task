## Intro

Purpose of this project was to create a web scrapper that will scrap information of football players from wikipedia pages. All the data has been collected and stored in postgreSQL database.

### Prerequisites

Before starting the program you should install python packages listed in requirements.txt. A good practice is to create virtual environment before installing anything else.

- to create a virtual environment (optional) run the following commands:

  ```python
  python -m venv env
  source /env/bin/activate
  ```

- after setting up virtual environment download python packages:
  ```python
  pip install -r requirements.txt
  ```

### Connect to database

For this project you should have postgreSQL. Create a database with a name of your choice. Run initial_script.sql to create the table players.

- To connect to the database with python you should change DATABASE_URL in db.py file. Format is

  ```sh
   postgresql://username:password@host:port/database
  ```

- Here is example of connection to the database called "c_and_i" running on localhost with user "postgres" and password "1234".
  ```sh
  postgresql://postgres:1234@localhost/c_and_i
  ```

### Run the program

After setting everything up you can run program with any given csv file which has list of urls in it (also column should be called "urls").

- Here is example how to run it with file called playersURLs.csv
  ```python
  python scrap.py playersURLs.csv
  ```

When program has finished you should have your database filled with data and program will also create file "scrapped_data.csv" with all the data it could find.

### Run SQL scripts

After you filled your database you should run all the other SQL scripts to enrich players data. (SQL scripts are in SQL folder)

1. First query will create two columns which will give us more information about peoples age category and ratio of goals and apearances in the current club
2. Second query will give us average age, goals and apearances for each club
3. Third query will give us a list of players in choosen club and count of players which are playing on the same positions, are younger and have more apearances in the current club. To choose a club change this part of query (change Liverpool to your cub of choice):
   ```sh
   WHERE players.current_club = 'Liverpool'
   ```

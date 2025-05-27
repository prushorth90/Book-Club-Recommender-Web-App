# Team Bald Unicorns Major Group project

## Team members
The members of the team are:
- Manivannan Prushorth  
- Charlie Bowen  
- Jun Yi Goh  
- Zaid Maraqa 
- Daro Saleh  
- Nilhil Suri 
- Alavro Moreno  

## Project structure
The project is called `bookClub`.  It currently consists of a single app `unibook`.

## Deployed version of the application
The deployed version of the application can be found at https://limitless-depths-09294.herokuapp.com/.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

To use spark recommender system, Java 8 needs to be installed and used:
  Installation of java 8: https://docs.datastax.com/en/jdk-install/doc/jdk-install/installOpenJdkDeb.html
  pyspark is included in requirements.txt, so running pip3 install -r requirements.txt will have pyspark downloaded.
  Switching between java versions in ubuntu if multiple versions are installed: https://aboullaite.me/switching-between-java-versions-on-ubuntu-linux/

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here.*
The orm_helper functions for clubs and users have been reused from King's College London's computer science's coursework, Chess Club Management System.
Some of the tests written have been reused as well with modifications and extensions of the tests to fit the bookaholics application.

DateField accepting only today and future's date: https://stackoverflow.com/questions/4941974/django-how-to-set-datefield-to-only-accept-today-future-dates/4942284
Disappearing location field with checkbox: https://stackoverflow.com/questions/53319441/when-checking-one-check-box-the-other-check-box-must-disappear

Recommender system and evaluation:
Source code - https://sundog-education.com/RecSys/
  The source code has been refactored to classes and functions to fit the bookaholics application.

Spark recommender sources
  Column in dataframe not being numeric - https://stackoverflow.com/questions/27772769/how-to-use-mllib-recommendation-if-the-user-ids-are-string-instead-of-contiguous
  Getting original column id - https://stackoverflow.com/questions/45787323/pyspark-reversing-stringindexer-in-nested-array

[![Build Status](https://app.travis-ci.com/NamoSmith/ku-polls.svg?branch=iteration2)](https://app.travis-ci.com/NamoSmith/ku-polls)
[![codecov](https://codecov.io/gh/NamoSmith/ku-polls/branch/iteration2/graph/badge.svg?token=F0LF2Y9UZ4)](https://codecov.io/gh/NamoSmith/ku-polls)

# KU Polls
A web application for conducting polls at [Kasetsart University](https://www.ku.ac.th/th).
## Project Documents

* [Home](../../wiki/Home)
* [Vision Statement](../../wiki/Vision%20Statement)   
* [Requirements](../../wiki/Requirements)

## Iterations

### Iteartion 1
* [Iteration 1 Plan](../../wiki/Iteration1%20Plan)
* [Iteration 1 TaskBoard](../../projects/1)
### Iteartion 2
* [Iteration 2 Plan](../../wiki/Iteration2%20Plan)
* [Iteration 2 TaskBoard](../../projects/3)
### Iteartion 3
* [Iteration 3 Plan](../../wiki/Iteration3%20Plan)
* [Iteration 3 TaskBoard](../../projects/4)


## How to run and get the initial data.

1. ```python manage.py migrate```  
2. ```python manage.py loaddata users polls``` 
3. ```python manage.py runserver```

## Running KU Polls  

Users provided by the initial data (users.json):

| Username   | Password        |
|------------|-----------------|
| test01     | hello123456    |
| test02     | hello123456    |

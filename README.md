# RESTful API - Golden Raspberry Awards
Development of RESTful API for reading and processing csv file data for Golden Raspberry Awards nominees and winners with [Flask v2.1.3](https://flask.palletsprojects.com/en/2.2.x/) and [flask-restx v0.5.1](https://flask-restx.readthedocs.io/en/latest/#). 

### Introduction
Before cloning this API repository, it is recommended to open a virtual development environment. Package conflicts with Flask and flask-restx may occur if this is not done. The necessary installation for the development of the project, if you want to install it manually, was:
<pre><code>pip install Flask==2.1.3, flask-restx==0.5.1, Werkzeug==2.0.3</code></pre>
If you have any problems with the installation, it is recommended to use the requirements.txt file:
<pre><code>pip install -r requirements.txt</code></pre>

### Important Topics
+ API Testing with Swagger
+ Endpoints and their input models
    + /csv (GET)
      + database request in csv
    + /csv (POST)
      + Newline integration in file and new id
      + Input error retention
    + /csv (DELETE)
      + Overwrite the database and calculate new id
    + /csv (PUT)
      + Updating and reusing data
      + Error retention in updates
    + /awards (GET)
      + Generalized clustering method
      + Raise exception system to save processing time
      + Range search followed by linear search

### API testing with Swagger
In the main '/' route it is possible to access the [swagger](https://github.com/swagger-api/swagger-ui) documentation, making it easier to test the api and its functionalities. In the payloads topic you can find out about the method used in API requests, but right on the swagger test page you can see the input models and server responses.

![Swagger](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/img/swagger.png?raw=true)

#### /csv (GET)
The method of viewing the csv data is quite simple. Only reading and storing in memory the csv file releasing a request to the user. When starting the server a preprocessing of the data in the file. An id column is added to facilitate data manipulation in the future. So when requesting the csv file, it will come with an id column. All API user actions are [listed here](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/data/data_change_request.py).

#### /csv (POST)
In this method the system used is different. Reading the file is necessary to collect the last id informed to correctly add the data to the database. The new id created is added to a list with the data entered by the user. 
Before sending this data to the actions in the database, the information is filtered by the payload models. After the payloads, a secondary check is made, so that there are no certain inputs such as the csv delimiter. You can check the payload models in the src\models\ And check the actions in the database in the directory [src\data\data_chage_request](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/data/data_change_request.py) in class `RequestCSV()` in `csv_post()`

#### /csv (DELETE)
This is the function that takes the most processing. The user will only have to enter a json file containing id. When it is informed and validated by all the steps, the system will do a linear search in the id column. All data is overwritten except the line containing the id entered by the user.
At that time a partial success. It is necessary to reshape the id column so that everything is in order. At this point, the script deletes the id column and reuses the same id creation process for the file that was used to open the server.

#### /csv (PUT)
This function is identical to POST. The only difference is that the user can define the parameters of the data lines so they don't need to update them if they don't want to. It is possible to update, for example, only the year of indication or the producers, without changing the rest. In this function we can see the functioning of the self-adapted system. [`find_element()`](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/data/data_change_request.py) is well used to define a newline without having to change the csv default.

#### /csv data processing
The functions used to process data at the user's request. [`Code here`](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/data/data_change_request.py)

| Function name  | Description                    | user inputs |
| -------------  | ------------------------------ | ----------- |
| `csv_post()`   | Add new data to the database   | [year*, title, studios, producers*, winner*] |
| `csv_2_list()` | Read from the database         | NaN |
| `csv_put()`    | Update existing data in the database | [id*, year, title, studios, producers, winner] |
| `csv_delete()`   | Delete data from the database | [id*]

### /awards (GET)
In this method, nothing is requested from the user, but there is an internal processing to return the processed data.
It is highly recommended to [take a look at the code](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/data/data_processing.py) to better understand the search method. There I left points for visualization of the processing to facilitate understanding.

The code is divided into:
| Data Processing         | Description                    | 
| ----------------------- | ------------------------------ | 
| `csv_reader()`          | Reading csv file in mode: open for reading (r) and text mode (t). The aim is to store the data in memory to speed up processing time and facilitate treatment.   | 
| `and_2_comma()`         | In the 'producers' column we see that there are two ways of dividing producers in the text. Separated by commas, 'and' and 'and, '. With this function we can have an effective separation of all producers in a list, facilitating the processing of information. |
| `find_element()`        | Finds the index of the searched string in a list. Used to save processing time, being faster than dictionary usage. |
| `producers_treatment()` | Treatment and verification of award winners. |

After this processing, the data must be grouped and analyzed. Below the system used.
| Function                | Description                    | 
| ----------------------- | ------------------------------ | 
| `CLUSTER()` | Returns a list of producers present in the films that won the award |
| `SECTION 1` | searches for a producer to be the research item in the secondary search |
| `SECTION 2` | intended to calculate the distance between the awards' data. |
| `SECTION 3` | intended to add an ID for each consecutive award range |
| `SECTION 4` | Has the objective of generating a list with the intervals necessary for the completion of the algorithm |
| `SECTION 5` | Intended to identify the maximum and minimum range of premiums and request data from the responsible producers |
| `FINALIZATION` | Iterates over the results to add to a json file |
| `list_2_json()` | Conversion of the result to json. |

If you use the same script for another database, look carefully at the [config.json](https://github.com/RP11-AI/API-RESTful-golden-raspberry-awards/blob/master/src/config/config.json) file.

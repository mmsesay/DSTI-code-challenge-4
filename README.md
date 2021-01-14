# DSTI Coding Challenge

If you’re reading this, then you’ve applied for a position at The Directorate of Science Technology & Innovation.

You have received this directory within the .zip archive.

**Instructions**

1. Create a repo out of this directory with this README.md in the root
2. Work on the task as specified in TASK.md
3. Follow the best practices when saving changes to the repo
4. Follow the best practices when creating your solution
5. Upload the solution to your personal Github account and add two collaborators
6. `zewolfe` username - George Gelaga-King, Software Developer
7. `Bayoh` username - Ibrahim Bayoh, Software Developer

---
**Installation**
1. **flask** : You need to create a virtual environment before install flask.
    The recommended way to create a virtual environment is to use the venv module. To install the python3-venv package that provides the venv module run the following command: ```sudo apt install python3-venv```
    1. Create a virtual environment directory: ```mkdir DSTI-code-challenge 4```
    2. Navigate to the virtual environment directory: ```cd DSTI-code-challenge 4```
    3. Once inside the directory, run the following command to create your new virtual environment: ```python3 -m venv venv```
    4. To start using this virtual environment, you need to activate it by running the activate script: ```source venv/bin/activate```
    5. Install all the packages ```pip install -r requirements.txt```
        1. Optional: Now that the virtual environment is activated, you can use the Python package manager pip to install Flask: ```(venv) pip install Flask```
    7. Verify the installation completed successfully with the following command which will print the Flask version: ```python -m flask --version```
    8. Now navigate back to the vagrant directory and clone the repo:
        ```git clone https://github.com/mmsesay/DSTI-code-challenge-4.git```
    9. cd to the **DSTI-Coding-Challenge 4** directory


## Executing the program
Make sure you are in the DSTI-Coding-Challenge directory and your virtual environment is activated:
1. Run the application on your terminal type the following in  a sequential format:
- ```export FLASK_APP=app.py``` and hit enter
- ```export FLASK_ENV=development``` optional: for development
- ```flask run``` and hit enter

3. Note: The map will be drawn and shown on a different webpage on your browser when you   visit http://localhost:5000 on browser.

## How to use the API Endpoints
This program is running on localhost port 5000. Therefore, use the API endpoints like so http://localhost:5000 


1. **/water_station/api/v1/read** : can return all the water stations
2. **/water_station/api/v1/create** : can accept a json payload and send the data to the server, then save in the db 
eg: 
```
{
    "id_number": 12,
    "latitude": 8.4851143,
    "longitude": -13.2201753,
    "water_station_type": "Pump",
    "capacity": 700
}
```

3. **/water_station/api/v1/update** : can accept a json payload and send the data to the server, then update the data
eg: 
```
{
    "id_number": 12,
    "latitude": 8.4851143,
    "longitude": -13.2201753,
    "water_station_type": "Pump",
    "capacity": 700
}
```
4. **/water_station/api/v1/delete** : can accept a json payload and the server will perform it operation
eg: 
```
{
	"id_number": 12
}
```

# app.py

import os
import csv
import shutil
import folium
import pandas as pd

from tempfile import NamedTemporaryFile
from typing import List, Tuple, Dict
from flask import Flask, jsonify, request, render_template

# instantiating 
app = Flask(__name__, template_folder="templates")

tempfile = NamedTemporaryFile(mode='w', delete=False)

water_stations_data = os.path.join('data', 'water_stations.csv')
fields = ['Id', 'Latitude', 'Longitude', 'Type', 'Capacity']

# readfile function
def readFile(file_path_n_filename: str) -> List[Dict[str, str]]:
    """ Is responsible to read the file and return the read data
    as a list of dictionary 
    
    Parameter:
    args: file_path_n_filename

    list[dict[str, str]]: the data read from the file
    """
    json_data = []  # will temporary hold the row to be returned

    # open the file for appending and closed when done
    with open(file_path_n_filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            json_data.append(row)

    return json_data

# writefile function
def writeFile(file_path_n_filename: str, entry: dict) -> Dict[str, str]:
    """Is responsible to write data into the csv
    args: file_path_n_filename

    Parameters: 
    file_path_n_filename (str): file path and the name of the file
    entry (dict): the new entry that the writer will write
  
    Returns: 
    dict: the entry that got written
    """
    fieldNames = ['Id', 'Latitude', 'Longitude', 'Type', 'Capacity']
    new_entry_list = []  # will temporary hold the row to be written

    # open the file for appending and closed when done
    with open(file_path_n_filename, 'a', newline='') as file:

        new_entry_list.append(entry)  # add the new entry to the new_entry_list

        # create the write object
        writer = csv.DictWriter(file, fieldNames)
        writer.writerows(new_entry_list)  # write the new entry

    return entry

# updateRecord function
def updateRecord(entry: dict) -> Dict[str, str]:
    """Is responsible to update a record

    Parameters: 
    entry (dict): the new entry that the writer will write
  
    Returns: 
    dict: the entry that got written
    """
    updatedRow = []

    with open(water_stations_data, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Id'] == str(entry['Id']):
                    print('updating row', row['Id'])
                    row['Latitude'], row['Longitude'], row['Type'], row['Capacity'] = entry['Latitude'], entry['Longitude'], entry['Type'], entry['Capacity']
            row = { 'Id': row['Id'],
                    'Latitude': row['Latitude'],
                    'Longitude': row['Longitude'],
                    'Type': row['Type'],
                    'Capacity': row['Capacity']}
            writer.writerow(row)  # write the updated row
            updatedRow.append(row)  # append the new update row

    shutil.move(tempfile.name, water_stations_data)
    return entry

@app.route("/")
def mapview():
    return render_template('salone-map.html')

# create api
@app.route('/water_station/api/v1/create', methods=['POST'])
def createWaterStation() -> Dict[str, str]:
    """
    Will handle the creation a new water station location
    """

    if request.method == 'POST':
        data = request.get_json()

        # get the incoming request data
        id_number           = data['id_number']
        latitude            = data['latitude']
        longitude           = data['longitude']
        water_station_type  = data['water_station_type']
        capacity            = data['capacity']

        # check for null values in the incoming request
        # if id_number or latitude or longitude or water_station_type or capacity is not None:
        new_entry = {
                'Id': id_number, 
                'Latitude': latitude, 
                'Longitude': longitude, 
                'Type': water_station_type, 
                'Capacity': capacity }

        # read the data
        waterStationsData = readFile(water_stations_data)

        # loop through the data
        for waterStation in waterStationsData:
            # convert the id_number and check if a match already exists
            if str(id_number) == waterStation['Id']:
                return jsonify({'duplicate error': 'A record with ID: {} already exits'.format(id_number)}), 409
            
        # write to the file
        response = writeFile(water_stations_data, new_entry)
        return jsonify(response), 201
    else:
        return jsonify({'error': 'Invalid request parse'}), 400

# read api
@app.route('/water_station/api/v1/read', methods=['GET'])
def readWaterStation() -> List[Dict[str, str]]:
    """
    Will handle reading all the water stations in the dataset
    """

    if request.method == 'GET':
        # read from the file function
        json_data = readFile(water_stations_data)
    return jsonify(json_data), 200

# update api
@app.route('/water_station/api/v1/update', methods=['PUT'])
def updateWaterStation():
    """
    Will handle updating a water station
    """

    if request.method == 'PUT':
        data = request.get_json()

        # get the incoming request data
        id_number           = data['id_number']
        latitude            = data['latitude']
        longitude           = data['longitude']
        water_station_type  = data['water_station_type']
        capacity            = data['capacity']

        # entry to update
        update_entry = {
                'Id': id_number, 
                'Latitude': latitude, 
                'Longitude': longitude, 
                'Type': water_station_type, 
                'Capacity': capacity 
            }

        # pass the entry to update and return the response 
        update_response = updateRecord(update_entry)
        return jsonify({'success': 'updating row {} was successful'.format(id_number)}), 204
    else:
        return jsonify({'error': 'Invalid request parse'}), 400


# delete api
@app.route('/water_station/api/v1/delete', methods=['DELETE'])
def deleteWaterStation():
    """
    Will handle deleting a water station
    """
    lines = list()  # will hold the list of water stations

    if request.method == 'DELETE':
        data = request.get_json()

        # get the incoming request data
        id_number   = data['id_number']

        # read the file
        with open(water_stations_data, 'r') as readFile:

            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)  # append the records to the temporary list
                
                # 
                for field in row:
                    if field == str(id_number):
                        lines.remove(row)  # remove the row
                    else:
                        return jsonify({'error':'ID {} not found'.format(id_number)})

        # write the changes to the file
        with open(water_stations_data, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
    return jsonify({"Success": "Deleted ID: {} successfully".format(id_number)})


@app.route("/map")
def newMap():
    start_coords = (8.460555, -11.779889)
    folium_map = folium.Map(
        location=start_coords, zoom_start=5    )

    json_data = readFile(water_stations_data)

    for point in json_data:

        folium.Marker(
                [point['Latitude'], point['Longitude']], 
                popup="""
                <strong>
                    Latitude: {},
                    Longitude: {},
                    Type: {},
                    Capacity: {},
                </strong>
                """.format(
                    point['Latitude'], point['Longitude'],
                    point['Type'], point['Capacity']
                ),
                tooltip="Click for more info").add_to(folium_map)

    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)
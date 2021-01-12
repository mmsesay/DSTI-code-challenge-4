# app.py

import csv
import json
import folium
import pandas as pd
import os

from typing import List, Tuple, Dict
from flask import Flask, jsonify, request, render_template

# read file
# districts = os.path.join('data', 'salone_geo.json')
# water_stations_data = os.path.join('data', 'water_stations.csv')
# districts_data = pd.read_csv(water_stations_data)
# data_path = os.path.join('data', 'water_stations.json')

# data = json.load(open(data_path, "r"))

# instantiating 
app = Flask(__name__, template_folder="templates")

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
def writeFile(file_path_n_filename: str, fields: list, entry: dict) -> Dict[str, str]:
    """Is responsible to read the file and return the read data
    as a list of dictionary 
    args: file_path_n_filename

    Parameters: 
    file_path_n_filename (str): file path and the name of the file
    fields (list): the fields of the csv file
    entry (dict): the new entry that the writer will write
  
    Returns: 
    dict: the entry that got written
    """
    new_entry_list = []  # will temporary hold the row to be written

    # open the file for appending and closed when done
    with open(file_path_n_filename, 'a', newline='') as file:

        new_entry_list.append(entry)  # add the new entry to the new_entry_list

        # create the write object
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerows(new_entry_list)  # write the new entry

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
        fieldNames = ['Id', 'Latitude', 'Longitude', 'Type', 'Capacity']
        new_entry = {
                'Id': id_number, 
                'Latitude': latitude, 
                'Longitude': longitude, 
                'Type': water_station_type, 
                'Capacity': capacity }

        # read the data
        waterStationsData = readFile('data/water_stations.csv')

        # loop through the data
        for waterStation in waterStationsData:
            # convert the id_number and check if a match already exists
            if str(id_number) == waterStation['Id']:
                return jsonify({'duplicate error': 'A record with ID: {} already exits'.format(id_number)}), 409
            
        # write to the file
        response = writeFile('data/water_stations.csv', fieldNames, new_entry)
        return jsonify(response), 201
        # return jsonify({'type error': 'All fields are required. A none-type is detected.'}), 400
    else:
        return jsonify({'error': 'Invalid request parse'}), 400

# read api
@app.route('/water_station/api/v1/read', methods=['GET'])
def readWaterStation() -> List[Dict[str, str]]:
    """
    Will handle reading all the water stations in the dataset
    """
    # read from the file function
    json_data = readFile('data/water_stations.csv')
    return jsonify(json_data), 200

# update api
@app.route('/water_station/api/v1/update', methods=['PUT'])
def updateWaterStation():
    """
    Will handle updating a water station
    """
    # json_object["d"] = 100
    pass

# delete api
@app.route('/water_station/api/v1/delete', methods=['DELETE'])
def deleteWaterStation():
    """
    Will handle deleting a water station
    """
    pass


@app.route("/map")
def newMap():
    start_coords = (8.460555, -11.779889)
    folium_map = folium.Map(
        location=start_coords, zoom_start=3

    )

    lat, lon = districts_data[['Latitude','Longitude']]
    print(lat, lon)

    # folium.Choropleth(
    #     geo_data=districts,
    #     name='choropleth',
    #     data=districts_data,
    #     columns=['Latitude','Longitude'],
    #     key_on='feature.id',
    #     fill_color='YlGn',
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name='Water Stations'
    # )

    folium.Marker(
            [8.4851143,-13.2201753], 
            popup='<strong>Location one</strong>',
            tooltip="point one").add_to(folium_map)

    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)
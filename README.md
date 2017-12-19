# OpenStreetMap in Manhattan Data Wrangling with MongoDB

## Procedure
1)	Obtain data (node(40.6978, -74.0224, 40.8704, -73.9160);<;);out meta; from [Overpass API](http://overpass-api.de/query_form.html); save as (‘manhattan.osm’)
2)	Run osm_to_json.py (‘manhattan.json’)
3)	Run keep_manhattan.py (‘manhattan_only.json’)
4)	Import data in MangoDB

## Code description
<osm_to_json.py>
input osm data
find elements in only 'node' and 'way' tags
process the data and transform it into json format
return json data

<keep_manhattan.py>
input data from osm_to_json.py
remove all data that is not in Manhattan using zipcode, latitude, longitude and city criteria
return cleaned data

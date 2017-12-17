# OpenStreetMap in Manhattan Data Wrangling with MongoDB

## Procedure
1)	Obtain data (node(40.6978, -74.0224, 40.8704, -73.9160);<;);out meta; from [Overpass API](http://overpass-api.de/query_form.html); save as (‘manhattan.osm’)
2)	Run osm_to_json.py (‘manhattan.json’)
3)	Run keep_manhattan.py (‘manhattan_only.json’)
4)	Import data in MangoDB


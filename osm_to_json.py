import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

# Give regular expression of problem characters
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# list the keys under 'created'
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    """
    input osm data
    find elements in only 'node' and 'way' tags
    process the data and transform it into json format
    return json data
    """

    node = {}
    if element.tag == "node" or element.tag == "way":
        ref = []

        # add nd ref
        for nd in element.iter('nd'):
            ref.append(nd.attrib['ref'])
        if ref != []:
            node['node_refs'] = ref

        # add id and type
        node['id'] = element.attrib['id']
        node['type'] = element.tag

        # add visible
        try:
            node['visible'] = element.attrib['visible']
        except:
            pass

        # add latitude and longitude
        try:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        except:
            pass

        # add content in created
        in_create = {}
        for i in ['changeset', 'user',  "version", "uid", "timestamp"]:
            in_create[i] = element.attrib[i]
        node['created'] = in_create

        # add content in address
        in_addr = {}
        for tag in element.iter('tag'):

            # remove problem characters
            if problemchars.search(tag.attrib['k']) > 0:
                pass

            elif tag.attrib['k'].startswith('addr:'):
                new_addr = tag.attrib['k'].replace('addr:', '')
                if ':' in new_addr:
                    pass
                else:
                    in_addr[new_addr] = tag.attrib['v']

            # add name and amenity in data
            elif tag.attrib['k'] in ['name', 'amenity']:
                node[tag.attrib['k']] = tag.attrib['v']

        if in_addr != {}:
            node['address'] = in_addr

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # process data and write data into json format
    file_out = "manhattan.json"
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    data = process_map('manhattan.osm', False)
    print data[0]

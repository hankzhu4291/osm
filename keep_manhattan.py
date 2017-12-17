import json
import codecs

def keep_MHT(data):
    """
    input data from osm_to_json.py
    remove all data that is not in Manhattan using zipcode, latitude, longitude and city criteria

    return cleaned data
    """

    # keep only data with zip code in Manhattan
    zipcode = [10026, 10027, 10030, 10037, 10039, 10001, 10011, 10018, 10019, 10020, 10036, 10029, 10035,
                10010, 10016, 10017, 10022,10012, 10013, 10014,10004, 10005, 10006, 10007, 10038, 10280,
                10002, 10003, 10009,10021, 10028, 10044,10065, 10075, 10128,10023, 10024, 10025,10031,
                10032, 10033, 10034, 10040]
    zipcode = [str(i) for i in zipcode]

    new_data = []
    for record in data:
        if 'address' in record.keys():
            if 'postcode' in record['address'].keys():
                if record['address']['postcode'] in zipcode:
                    new_data.append(record)

            else:
                new_data.append(record)
        else:
            new_data.append(record)

    # remove record in NJ
    below_nj = [40.719963, -74.042659]
    top_nj = [40.876282, -73.938882]
    slope_nj = (top_nj[0] - below_nj[0])/(top_nj[1] - below_nj[1])

    rm_nj_data = []
    for record in new_data:
        try:
            if (record['pos'][0] - below_nj[0])/(record['pos'][1] - below_nj[1]) > slope_nj:
                pass
            else:
                rm_nj_data.append(record)
        except:
                rm_nj_data.append(record)

    # remove data that is in Brooklyn or Long Island
    below_br = [40.715549, -73.969592]
    top_br = [40.796967, -73.911879]
    slope_br = (top_br[0] - below_br[0])/(top_br[1] - below_br[1])

    rm_br_data = []
    for record in rm_nj_data:
        try:
            if (record['pos'][0] - below_br[0])/(record['pos'][1] - below_br[1]) < slope_br:
                pass
            else:
                rm_br_data.append(record)
        except:
                rm_br_data.append(record)

    return rm_br_data


def process_data(data, file_out):
    new_data = keep_MHT(data)
    manhattan_only = []
    # for some street name with extra info, delete them
    for record in new_data:
        try:
            if ',' in record['address']['street']:
                record['address']['street'] = record['address']['street'].split(',')[0]
        except:
            pass

        # remove other city names and transform New York/ New York City into New York
        if 'address' in record.keys():
            if 'city' in record['address'].keys():
                record['address']['city'] = ' '.join(record['address']['city'].upper().split(' ')[:2])
                if record['address']['city'] == 'NEW YORK':
                    manhattan_only.append(record)
            else:
                manhattan_only.append(record)
        else:
            manhattan_only.append(record)

    # write data
    with codecs.open(file_out, "w") as fo:
        for elem in manhattan_only:
            fo.write(json.dumps(elem) + "\n")

    return manhattan_only

if __name__ == "__main__":
    data = []
    for line in open('manhattan.json', 'r'):
        data.append(json.loads(line))

    file_out = "manhattan_only.json"

    manhattan_only = process_data(data, file_out)
    print len(manhattan_only)

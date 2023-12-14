import random

from test_data import message_type


class HandleData(object):
    def get_param_data(self, message_id):
        # raw_data = message_type[message_id]
        # if message_id == "reportLocation":
        # key = random.choice(['x', 'y', 'orientation'])
        # raw_data[key] = raw_data[key] + random.randint(1, 10)

        raw_data = {
            "reportLocation": {
                "lng": 116,
                "lat": 40,
                "x": random.randint(0, 500),
                "y": random.randint(0, 500),
                "orientation": random.randint(0, 359),
                "rtkLng": 0,
                "rtkLat": 0,
                "mapId": "4827b3a14cf9419980357c36f5256e43"
            }
        }

        return raw_data

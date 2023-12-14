message_type = {
    "reportLocation": {
        "lng": 0,
        "lat": 0,
        "x": 100,
        "y": 100,
        "orientation": 200,
        "rtkLng": 0,
        "rtkLat": 0,
        "mapId": "4827b3a14cf9419980357c36f5256e43"
    },

    "reportStatus": {
        "language": "CH",
        "asrStatus": 1,
        "robotStatus": 1,
        "rcu": {
            "battery": {
                "percent": 97,
                "chargingStatus": 1,
                "temperature": 42
            }
        },
        "robot": {
            "battery": {
                "percent": 97,
                "chargingStatus": 0,
                "voltage": "49.62"
            }
        },
        "chassis": {
            "percent": 0,
            "chargingStatus": 0
        },
        "config": {
            "rcuCamera": {
                "videoStartBps": 300,
                "videoBps": 512,
                "audioStartBps": 64,
                "videoCodec": "VP8",
                "audioCodec": "OPUS",
                "videoFps": 512,
                "videoWidth": 640,
                "videoHeight": 480,
                "msMaxBps": 0,
                "msMinBps": 0,
                "rcuVideoEnable": True
            },
            "topCamera": {
                "videoFps": 0.5,
                "webCamStatus": False,
                "index": 0
            },
            "faceDetection": {
                "camera": "CHEST",
                "operationStatus": "Stopped"
            },
            "tts": {
                "type": "CloudMinds",
                "speakVolume": "60",
                "language": "CH",
                "location": "Cloud"
            },
            "asr": {
                "type": "CloudMinds",
                "language": "CH",
                "silence": False
            },
            "network": {
                "accessType": "WIFI",
                "quality": 4,
                "weakNetState": False
            },
            "operationMode": "online",
            "screenStatus": "off"
        },
        "indoorPosState": 0,
        "pepperActions": {
            "dances": [
            ],
            "actions": [
                {
                    "action": "cloudminds\/stop",
                    "text": "stop"
                },
                {
                    "action": "cloudminds\/inspect",
                    "text": "inspect"
                }
            ]
        }
    },

    "robotStatus": {
        "system": {
            "backLightStatus": False,
            "batteryLevel": 0,
            "chargingStatus": False,
            "collisionStatus": False,
            "emergencyStopStatus": False,
            "environment": {
                "CO": 0,
                "CO2": 0,
                "TVOC": 0,
                "atmosphere": 0,
                "humidity": 76,
                "pm2_5": 12,
                "smog": 0,
                "temperature": 28,
                "wade": 0
            },
            "frontLightStatus": False,
            "lowLiquidLevelStatus": False,
            "motorInfo": "",
            "redBlueStatus": False,
            "requestTalkStatus": False,
            "shutdownStatus": False,
            "softbrakeStatus": False
        }
    },

    "reportMapList": {
        "active": "4827b3a14cf9419980357c36f5256e43",
        "mapList": [
            {
                "mapVersion": "2",
                "mapType": "single",
                "description": "北京市(废弃)/东城区/达闼",
                "mapId": "4827b3a14cf9419980357c36f5256e43",
                "mapName": "房山一层全图_ginger-lite_1.0"
            }
        ]
    },

    "reportRmfRoute": {
        "action": "reportRmfRoute",
        "param": {
            "guid": "2A9E1EFF08DBB5DAB39394A021400033-61",
            "robotId": "GINLITXR-1LXXXXXXXXXGNL29S2242001377",
            "locations": [
                {
                    "index": 2,
                    "sec": 1694746721,
                    "nanoSec": 842183113,
                    "x": 186.00800000000001,
                    "y": 305,
                    "yaw": 38.875536064687346,
                    "type": 10,
                    "levelName": "L1"
                },
                {
                    "index": 4,
                    "sec": 1694746726,
                    "nanoSec": 834640979,
                    "x": 211,
                    "y": 274,
                    "type": 10,
                    "levelName": "L1"
                },
                {
                    "index": 6,
                    "sec": 1694746730,
                    "nanoSec": 372277021,
                    "x": 211,
                    "y": 238,
                    "levelName": "L1"
                }
            ],
            "taskId": "2A9E1EFF08DBB5DAB39394A021400033",
            "pathPlanner": "RMF",
            "map_id": "00047ca2653647aaa2612b43b809d9b4"
        }
    },

    "reportEvent": {
        "datetime": "2023-09-15 13:07:54",
        "detail": "boot",
        "id": 2100024,
        "level": 1,
        "name": "boot"
    }
}

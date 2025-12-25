from typing import Optional, Set

FORWARD_TOPIC_RULES = {
    1: {  # XFaction Chat
        "text": True,
        "photo": True,
        "video": True,
        "doc_ext": None,  # None = allow all
    },

    8201: {  # Mission Banners
        "text": False,
        "photo": False,
        "video": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
    },

    11079: {  # Ingress Updates
        "text": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
    },
}

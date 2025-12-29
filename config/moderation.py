TOPIC_RULES = {
    1: {  # XFaction Chat
        "text": True,
        "photo": True,
        "video": True,
        "forwarded_allowed": None,   # follow normal rules
        "doc_ext": None,   # None = allow all documents
    },

    10: {  # BRAGGING RIGHTS
        "text": False,
        "photo": True,
        "video": True,
        "forwarded_allowed": False,   # delete all forwarded messages
        "doc_ext": {".jpg", ".jpeg", ".png", ".mp4"},
    },

    8201: {  # Mission Banners
        "text": False,
        "photo": True,
        "video": False,
        "forwarded_allowed": None,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
    },
    11079: {  # Ingress Updates
        "text": False,
        "photo": False,
        "video": False,
        "forwarded_allowed": True,   # allowed all forwarded messages
        "doc_ext": False,
    },
}

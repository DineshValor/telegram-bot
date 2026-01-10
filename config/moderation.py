TOPIC_RULES = {
    11079: {  # Ingress Updates
        "text": False,
        "photo": False,
        "video": False,
        "gif": False,
        "doc_ext": False,
        "forwarded_allowed": True,
    },
    
    1: {  # XFaction Chat
        "text": True,
        "photo": True,
        "video": True,
        "gif": True,
        "doc_ext": None,   # None = allow all documents
        "forwarded_allowed": None,   # follow normal rules
    },

    10: {  # BRAGGING RIGHTS
        "text": False,
        "photo": True,
        "video": True,
        "gif": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".mp4"},
        "forwarded_allowed": True,   # allowed all forwarded messages
    },

    8201: {  # Mission Banners
        "text": False,
        "photo": True,
        "video": False,
        "gif": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
        "forwarded_allowed": True,  # allowed all forwarded messages
    },
}

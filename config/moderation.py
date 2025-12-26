TOPIC_RULES = {
    1: {  # XFaction Chat
        "text": True,
        "photo": True,
        "video": True,
        "doc_ext": None,  # None = allow all documents
    },
    
    10: { # BRAGGING RIGHTS
        "text": False,
        "photo": True,
        "video": True,
        "doc_ext": {".jpg", ".jpeg", ".png", ".mp4"},
    },
    8201: { # Mission Banners
        "text": False,
        "photo": True,
        "video": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
    },
}

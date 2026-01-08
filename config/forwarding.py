"""
Forwarding configuration:
- CHANNEL_TOPIC_MAP: where messages go
- FORWARD_TOPIC_RULES: what is allowed per topic
"""

# =========================
# Channel → Topic routing
# =========================

CHANNEL_TOPIC_MAP = {
    -5291719056: 1,  # Ingress India 🇮🇳 Test
    
    -1001305415858: 15,       # IngressFS Notifications

    -1001170454563: 11079,    # Ingress Official
    -1001008795454: 11079,    # Passcodes Ingress PRIME
    -1001126789733: 11079,    # Ingress Passcodes
    -1001093134636: 11079,    # Ingress Passcodes [RES]
    -1003307267310: 11079,    # Ingress India 🇮🇳 Passcodes

    -1001075281753: 8201,     # Mission Banners, Oh My!
    -1001078001228: 8201,     # #MissionProject
    -1001420065662: 8201,     # Ingress Mission Addicts

    -1002105354149: 1,        # Ingress World Wide Competition 2025
    -1001167466234: 1,        # NotNiantic Updates
    -1001077599821: 1,        # Ingress Updates [ENG]
    -1001402896020: 1,        # News_Hackventscalendar
    -1001851154018: 1,        # Ingress.Plus
}


# =========================
# Topic-based forwarding rules
# =========================

FORWARD_TOPIC_RULES = {
    11079: {  # Ingress Updates
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },
    
    1: {  # XFaction Chat
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    8201: {  # Mission Banners
        "text": False,
        "link": True,
        "photo": False,
        "video": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    10: {  # BRAGGING RIGHTS
        "text": False,
        "link": False,
        "photo": False,
        "video": False,
        "doc_ext": False,
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    3077: {  # Random Media (SFW)
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },
    
    14: {  # Anomaly & MD
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    15: {  # First Saturday
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    9762: {  # Nominations
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },

    7125: {  # Pokemon Go (Isolated)
        "text": True,
        "link": True,
        "photo": True,
        "video": True,
        "doc_ext": None,
        "dedup_new": True,
        "dedup_include_edits": True,
    },
}

# -*- coding: utf-8 -*-

SPEAKER_NAMES = [
    'FL', 'FR',  # 0–1
    'FC',        # 2
    'LFE',       # 3
    'SL', 'SR',  # 4–5 (Side surrounds)
    'BL', 'BR',  # 6–7 (Back surrounds)
    'WL', 'WR',  # 8–9 (Wide L/R)
    'TFL', 'TFR', 'TSL', 'TSR', 'TBL', 'TBR'  # 10–15
]

# Speaker layout indexes (without LFE channel for reference formats)
SPEAKER_LAYOUT_INDEXES = {
    "1.0": [(0,)],             # Mono (front left)
    "2.0": [(0, 1)],        # Front Left, Front Right
    "5.1": [(0, 1), (2,), (6, 7)],        # 2.0 plus Center, Back Left and Back Right
    "7.1": [(0, 1), (2,), (4, 5), (6, 7)], # 5.1 plus Side Left, Side Right, then Back Left Back Right
    "7.1.4": [(0, 1), (2,), (4, 5), (6, 7), (10, 11), (14, 15)],
    "9.1.6": [
        (0, 1),    # Front Left, Front Right
        (2,),      # Center
        (4, 5),    # Side Left, Side Right
        (6, 7),    # Back Left, Back Right
        (8, 9),    # Wide Left, Wide Right
        (10, 11),  # Top Front Left, Top Front Right
        (12, 13),  # Top Middle Left, Top Middle Right
        (14, 15)   # Top Back Left, Top Back Right
    ]
}
# Resolved layout mappings (label groups)
SPEAKER_LAYOUTS = {
    name: [[SPEAKER_NAMES[i] for i in group] for group in groups]
    for name, groups in SPEAKER_LAYOUT_INDEXES.items()
}
# Regex patterns and helpers
SPEAKER_PATTERN = f'({"|".join(SPEAKER_NAMES + ["X"])})'
SPEAKER_LIST_PATTERN = r'{speaker_pattern}+(,{speaker_pattern})*'.format(
    speaker_pattern=SPEAKER_PATTERN
)

SPEAKER_DELAYS = {_speaker: 0 for _speaker in SPEAKER_NAMES}

# Applies diffuse-field compensation to HRIRs
APPLY_DIFFUSE_FIELD_COMPENSATION = False

# Applies headphone EQ compensation
APPLY_HEADPHONE_EQ = True

# Applies room correction filtering (e.g., smoothing or flattening)
APPLY_ROOM_CORRECTION = False

# Preserve the room's full impulse response without normalization or truncation
PRESERVE_ROOM_RESPONSE = True

# Applies directional gains in order to correctly calibrate ITD
APPLY_DIRECTIONAL_GAINS = False

# Each channel, left and right
IR_ORDER = []
# SPL change relative to middle of the head - disable
IR_ROOM_SPL = {
    sp: {'left': 0.0, 'right': 0.0}
    for sp in SPEAKER_NAMES
}
COLORS = {
    'lightblue': '#7db4db',
    'blue': '#1f77b4',
    'pink': '#dd8081',
    'red': '#d62728',
    'lightpurple': '#ecdef9',
    'purple': '#680fb9',
    'green': '#2ca02c'
}

HESUVI_TRACK_ORDER = ['FL-left', 'FL-right', 'SL-left', 'SL-right', 'BL-left', 'BL-right', 'FC-left', 'FR-right',
                      'FR-left', 'SR-right', 'SR-left', 'BR-right', 'BR-left', 'FC-right', 'WL-left', 'WL-right', 'WR-left', 'WR-right', 'TFL-left', 'TFL-right',
                             'TFR-left', 'TFR-right', 'TSL-left', 'TSL-right', 'TSR-left', 'TSR-right',
                             'TBL-left', 'TBL-right', 'TBR-left', 'TBR-right']

HEXADECAGONAL_TRACK_ORDER = ['FL-left', 'FL-right', 'FR-left', 'FR-right', 'FC-left', 'FC-right', 'LFE-left',
                             'LFE-right', 'BL-left', 'BL-right', 'BR-left', 'BR-right', 'SL-left', 'SL-right',
                             'SR-left', 'SR-right', 'WL-left', 'WL-right', 'WR-left', 'WR-right', 'TFL-left', 'TFL-right',
                             'TFR-left', 'TFR-right', 'TSL-left', 'TSL-right', 'TSR-left', 'TSR-right',
                             'TBL-left', 'TBL-right', 'TBR-left', 'TBR-right']

# Map channel index to name using the default layout (first entry in SPEAKER_NAMES)
CHANNEL_LABELS = {i: name for i, name in enumerate(SPEAKER_NAMES)}
# Optional reverse lookup for GUI usage
CHANNEL_LABELS_REVERSE = {name: i for i, name in CHANNEL_LABELS.items()}
# Map layout name to flat list of speaker indices
FORMAT_PRESETS = {
    name: [idx for group in groups for idx in group]
    for name, groups in SPEAKER_LAYOUT_INDEXES.items()
}
# SMPTE layout index definitions per format
SMPTE_LAYOUT_INDEXES = {
    "1.0": [(0,)],
    "2.0": [(0, 1)],
    "5.1": [(0, 1), (2,), (3,), (6, 7)],
    "7.1": [(0, 1), (2,), (3,), (4, 5), (6, 7)],
    "7.1.4": [(0, 1), (2,), (3,), (4, 5), (6, 7), (10, 11), (14, 15)],
    "9.1.6": [(0, 1), (2,), (3,), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15)]
}
# Preset orders using SPEAKER_LAYOUT_INDEXES for SMPTE
# Flattened versions for GUI use
SMPTE_ORDER = {
    fmt: [i for group in SMPTE_LAYOUT_INDEXES[fmt] for i in group]
    for fmt in SMPTE_LAYOUT_INDEXES
}


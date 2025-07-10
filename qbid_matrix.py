# ============================================================================
# QuickBase ID Matrix
# ============================================================================

"""      
Determines which fields are concatenated with '|' to form QBID

!! NOTE: THIS IS JUNK FOR NOW, JUST EXPERIMENTING WITH DIFFERENT WAYS TO DERIVE QBID !!
"""
QBID_MATRIX = {
            'JFMP': {
                'forests': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'biodiversity': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],#
                'water': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'heritage': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'summary': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"]
            },
            'DAP': {
                'forests': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'biodiversity': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'water': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'heritage': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'summary': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"]
            },
            'NBFT': {
                'forests': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'biodiversity': ["UNIQUE_ID", "RECORD_ID", "MR_CODE", "COMM_NAME", "TYPE", "SCI_NAME", "X", "Y"], #
                'water': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'heritage': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
                'summary': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"]
            }
        }

# Alternative approach - specify concatenation fields for each
QBID2_MATRIX = {
    # FOREST
    'FMZ':                      ["UNIQUE_ID", "Value_ID"],
    'Monitoring Site':          ["UNIQUE_ID", "Value_ID", "Value"],
    'RECWEB SITE':              ["UNIQUE_ID", "Value_ID", "Value_Description"],
    'RECWEB ASSET':             ["UNIQUE_ID", "Value_ID", "Value_Description"],
    'RECWEB HISTORIC RELIC':    ["UNIQUE_ID", "Value_ID", "Value_Description"],
    'RECWEB SIGN':              ["UNIQUE_ID", "Value_ID", "Value_Description"],
    'RECWEB CARPARK':           ["UNIQUE_ID", "Value_ID", "Value_Description"],
    'Historic Heritage Site':   ["UNIQUE_ID", "Value_ID", "Value"],
    'TRP Coupe':                ["UNIQUE_ID", "Value_ID", "Value"],
    'JFMP':                     ["UNIQUE_ID", "Value_ID", "Value"],
    'Giant Tree':               ["UNIQUE_ID", "Value_ID", "Value_Type"],
    'Alpine Hut':               ["UNIQUE_ID", "Value_ID", "Value"],
    'Mine Site':                ["UNIQUE_ID", "Value_ID", "Value_Type"],
    'Mine Lease':               ["UNIQUE_ID", "Value_ID", "Value_Type"],
    'Apiary Site':              ["UNIQUE_ID", "Value_ID", "Value_Type"],
    'Ag Chem Control Area':     ["UNIQUE_ID", "Value_ID", "Value_Type"],
    'Phytophthora Risk':        ["UNIQUE_ID", "Value_ID", "Value"],
    'Historic Site':            [],
    'Grazing Licence':          [],
    'Powerline':                [],
    'Pipeline':                 [],
    'Railway':                  [],


        'EVC': ["UNIQUE_ID", "MR_CODE"],
        'Bio Monitoring': ["UNIQUE_ID", "RECORD_ID", "MR_CODE"],
        
        'Flora': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
        'Fauna': ["UNIQUE_ID", "COMM_NAME", "SCI_NAME", "MR_CODE", "X", "Y"],
        'LBP Colony': ["UNIQUE_ID", "MR_CODE", "COMM_NAME"],
        'other': ["UNIQUE_ID", "MR_CODE", "COMM_NAME", "TYPE"],
        'Value_Description_present': ["UNIQUE_ID", "Value", "Value_Description", "X", "Y"],
        
        'Mining Site': ["UNIQUE_ID", "Value_ID", "Value_Type"],
        'Apiary Site': ["UNIQUE_ID", "Value_ID", "Value_Type"],
        
        
        
        'other_no_description': ["UNIQUE_ID", "Value", "X", "Y"],
        'other_with_description': ["UNIQUE_ID", "Value", "Value_Description", "X", "Y"]
    }
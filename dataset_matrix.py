# ============================================================================
# Dataset Processing Matrix
# ============================================================================

"""      
DATASET DEFINITIOINS:
    'name': {
            'path':                 string (required) - datapath to values layer
            'high_risk_only':       bool (Optional) - if True, do not process for LRLI activities; default is False
            'modes':                list (Optional) - If list populated, layer will only be processed for listed modes
            'buffer':               string or dict (Optional) - See note above; default value is '1m'
            'where_clause':         string (Optional) - SQL type selection for values; default is None
            'fields':               list (required) - field names to include in summary
            'value_type':           string (required) - description of value type for all values in layer
            'value_field':          string or list (Optional) - field name of main value field; must exist in fields (above)     
            'description_field':    string (Optional) - field name of description field; must exist in fields (above)
            'id_field':             string (Optional) - unique identifier for value instance; must exist in fields (above)
        },

NOTE:   'buffer' can be:
            - a string, e.g. 'buffer: '1m' which will be applied to all modes
            - a dict, e.g. 'buffer': {'DAP': '1m', 'JFMP': '50m', 'NBFT': '1m'} which will apply the buffer depending on selected mode
            - a nested dict, e.g.: 'buffer': {'DAP': '500m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '500m'} which will separately apply each listed buffer type for the selected mode
            - omitted, in which case overlapping (1m buffer) values will be captured
        'value_field' can be:
            - a string, e.g. 'COMM_NAME' resulting in CSV 'Value' = COMM_NAME, e.g. 'Broad Shield-fern'
            - a list, e.g. ['COMM_NAME', 'SCI_NAME'] which concats fields, e.g. 'Broad Shield-fern, Polystichum formosum'
"""

DATASET_MATRIX = {
    # FORESTS THEME
    'forests': {
        'fmz': {
            'path': "{csdl}\\FORESTS.GDB\\FMZ100",
            'high_risk_only': True,
            'where_clause': "FMZDIS IN('SPZ', 'SMZ')",
            'fields': ["FMZDIS", "DESC1", "FMZ_NO", "DETAILNO"],
            'value_type': 'FMZ',
            'value_field': 'FMZDIS',
            'description_field': 'DESC1',
            'id_field': 'FMZ_NO' # Mod from DETAILNO
        },
        'monitoring_forest': {
            'path': "{regional}\\RegionalData.gdb\\BLD_LAND_MANAGEMENT_SITES",
            'where_clause': "(SITE_CATEGORY IN('FOREST','FIRE')) AND TIMEFRAME <> 'NOT ACTIVE'",
            'fields': ["SITE_ID", "SITE_NAME", "LMS_ID"],
            'value_type': 'Monitoring Site',
            'value_field': 'SITE_ID',
            'description_field': 'SITE_NAME',
            'id_field': 'LMS_ID'
        },
        'recweb_sites': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_SITE",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "FAC_TYPE", "SERIAL_NO"],
            'value_type': 'RECWEB SITE',
            'value_field': 'NAME',
            'description_field': 'FAC_TYPE',
            'id_field': 'SERIAL_NO'
        },
        'recweb_assets': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_ASSET",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "ASSET_CLS", "SERIAL_NO"],
            'value_type': 'RECWEB ASSET',
            'value_field': 'NAME',
            'description_field': 'ASSET_CLS',
            'id_field': 'SERIAL_NO'
        },
        'recweb_historic_relic': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_HISTORIC_RELIC",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "ASSET_CLS", "SERIAL_NO"],
            'value_type': 'RECWEB HISTORIC RELIC',
            'value_field': 'NAME',
            'description_field': 'ASSET_CLS',
            'id_field': 'SERIAL_NO'
        },
        'recweb_sign': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_SIGN",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "ASSET_CLS", "SERIAL_NO"],
            'value_type': 'RECWEB SIGN',
            'value_field': 'NAME',
            'description_field': 'ASSET_CLS',
            'id_field': 'SERIAL_NO'
        },
        'recweb_carpark': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_CARPARK",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "ASSET_CLS", "SERIAL_NO"],
            'value_type': 'RECWEB CARPARK',
            'value_field': 'NAME',
            'description_field': 'ASSET_CLS',
            'id_field': 'SERIAL_NO'
        },
        'historic_sites': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\HIST100_POINT",
            'buffer': '300m',
            'where_clause': None,
            'fields': ["NAME"],
            'value_type': 'Historic Heritage Site',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        },
        'trp_coupes': {
            'path': "{csdl}\\FORESTRY.GDB\\TRP",
            'where_clause': None,
            'fields': ["COUPE"],
            'value_type': 'TRP Coupe',
            'value_field': 'COUPE',
            'description_field': None,
            'id_field': None
        },
        'burn_plan': {
            'path': "{csdl}\\FIRE.GDB\\BURNPLAN25",
            'where_clause': "REGION = 'Gippsland'",
            'fields': ["TREAT_NO", "TREAT_NAME", "TREAT_TYPE"],
            'value_type': 'JFMP',
            'value_field': 'TREAT_TYPE',
            'description_field': 'TREAT_NAME',
            'id_field': 'TREAT_NO'
        },
        'giant_trees': {
            'path': "{csdl}\\FORESTS.GDB\\EG_GIANT_TREES",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["SOURCE"],
            'value_type': 'Giant Tree',
            'value_field': 'SOURCE',
            'description_field': None,
            'id_field': None
        },
        'alpine_huts': {
            'path': "{csdl}\\FORESTS.GDB\\EG_ALPINE_HUT_SURVEY",
            'high_risk_only': True,
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "EASTING", "NORTHING"],
            'value_type': 'Alpine Hut',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        },
        'mine_site': {
            'path': "{csdl}\\MINERALS.GDB\\MINSITE",
            'buffer': '100m',
            'where_clause': None,
            'fields': ["SITEID", "MINE_TYPE", "MINE_NAME"],
            'value_type': 'Mining Site',
            'value_field': 'MINE_TYPE',
            'description_field': 'MINNMAE',
            'id_field': "SITEID"
        },
        'mine_lease': {
            'path': "{csdl}\\MINERALS.GDB\\MIN",
            'where_clause': None,
            'fields': ["TAG", "STATUSADSC", "TNO"],
            'value_type': 'Mining Lease',
            'value_field': 'TAG',
            'description_field': 'STATUSADSC',
            'id_field': "TNO"
        },
        'apiary_site': {
            'path': "{csdl}\\CROWNLAND.GDB\\APIARY_BUFF",
            'where_clause': None,
            'fields': ["TENURE_ID"],
            'value_type': 'Apiary Site',
            'value_field': 'TENURE_ID',
            'description_field': None,
            'id_field': None
        },
        'chemical_control': {
            'path': "{csdl}\\regional_business.gdb\\BLD_CHEMICAL_CONTROL_AREAS",
            'where_clause': None,
            'fields': ["ACCA_NAME"],
            'value_type': 'Ag Chem Control Area',
            'value_field': 'ACCA_NAME', 
            'description_field': None,
            'id_field': None
        },
        'phytophthora_risk': {
            'path': "{csdl}\\regional_business.gdb\\HIGH_PC_RISK_0610_POLY",
            'where_clause': "CLASS = 'High'",
            'fields': ["CLASS"],
            'value_type': 'Phytophthora Risk',
            'value_field': 'CLASS', 
            'description_field': None,
            'id_field': None
        },
        'heritage_inventory': {
            'path': "{csdl}\\PLANNING.GDB\\HERITAGE_INVENTORY",
            'buffer': '50m',
            'where_clause': None,
            'fields': ["VHI_NUM", "SITE_NAME", "HERMES_NUM"],
            'value_type': 'Historic Site',
            'value_field': 'VHI_NUM', 
            'description_field': 'SITE_NAME',
            'id_field': 'HERMES_NUM'
        },
        'heritage_register': {
            'path': "{csdl}\\PLANNING.GDB\\HERITAGE_REGISTER",
            'buffer': '50m',
            'where_clause': None,
            'fields': ["VHR_NUM", "SITE_NAME", "HERMES_NUM"],
            'value_type': 'Historic Site',
            'value_field': 'VHR_NUM', 
            'description_field': 'SITE_NAME',
            'id_field': 'HERMES_NUM'
        },
        'grazing_license': {
            'path': "{csdl}\\VMCLTENURE.GDB\\V_CL_TENURE_POLY",
            'high_risk_only': True,
            'where_clause': "CLTEN_TENURE_CODE >= '100' and CLTEN_TENURE_CODE < '200'",
            'fields': ["CLTEN_TENURE_ID", "TENURE", "HERMES_NUM"],
            'value_type': 'Grazing Licence',
            'value_field': 'TENURE', 
            'description_field': 'CLTEN_TENURE_ID',
            'id_field': None
        },
        'powerline': {
            'path': "{csdl}\\VMFEAT.gdb\\POWER_LINE",
            'buffer': '50m',
            'where_clause': None,
            'fields': ["FEATURE_SUBTYPE", "VOLTAGE"],
            'value_type': 'Powerline',
            'value_field': 'FEATURE_SUBTYPE', 
            'description_field': 'VOLTAGE',
            'id_field': None
        },
        'pipeline': {
            'path': "{csdl}\\VMFEAT.gdb\\FOI_LINE",
            'buffer': '50m',
            'where_clause': "FEATURE_TYPE = 'pipeline'",
            'fields': ["FEATURE_SUBTYPE", "NAME_LABEL"],
            'value_type': 'Pipeline',
            'value_field': 'NAME_LABEL', 
            'description_field': 'FEATURE_SUBTYPE',
            'id_field': None
        },
        'railway': {
            'path': "{csdl}\\VMTRANS.gdb\\TR_RAIL",
            'buffer': '50m',
            'where_clause': None, # CHECK - original script has query commented out?
            'fields': ["NAME", "FEATURE_TYPE_CODE"],
            'value_type': 'Railway',
            'value_field': 'NAME', 
            'description_field': 'FEATURE_TYPE_CODE',
            'id_field': None
        },
    },
    
    # BIODIVERSITY THEME
    'biodiversity': {
        # VBA Flora
        'vba_flora25': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FLORA25",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND (EPBC_DESC in ('Endangered','Vulnerable','Critically Endangered') OR OLD_VICADV in ('e','v','P','x') OR FFG in('cr','en','vu','th','cd','en-x','L'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Flora',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_flora_threatened': {
            'path': "{csdl_restricted}\\VBA_FLORA_THREATENED",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Flora_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_flora_restricted': {
            'path': "{csdl_restricted}\\VBA_FLORA_RESTRICTED",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Flora_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        # VBA Fauna - note: 3 datasets, special treatment of owls, bats, sea eagle and goshawk for each
        'vba_fauna_owl': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Masked Owl','Powerful Owl','Sooty Owl','Square-tailed Kite','Barking Owl')) AND " +
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna - Owl',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_wbse': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': {'DAP': '500m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '500m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'White-bellied Sea-Eagle') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna - WBSE',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_ghawk': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'Grey Goshawk') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna - G',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_bat': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': {'DAP': '100m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '100m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Grey-headed Flying-fox','Eastern Horseshoe Bat','Common Bent-wing Bat','Eastern Bent-winged Bat')) and " + 
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna25': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND (EPBC_DESC in ('Endangered','Vulnerable','Critically Endangered') OR OLD_VICADV in ('cr','en','vu','wx') OR FFG in ('cr','en','vu','th','cd','en-x','L') OR COMM_NAME = 'Koala')",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },

        'vba_fauna_threatened_owl': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Masked Owl','Powerful Owl','Sooty Owl','Square-tailed Kite','Barking Owl')) AND " +
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_threatened_wbse': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': {'DAP': '500m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '500m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'White-bellied Sea-Eagle') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_threatened_ghawk': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'Grey Goshawk') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_threatened_bat': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': {'DAP': '100m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '100m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Grey-headed Flying-fox','Eastern Horseshoe Bat','Common Bent-wing Bat','Eastern Bent-winged Bat')) and " + 
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_threatened': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Threatened',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        
        'vba_fauna_restricted_owl': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Masked Owl','Powerful Owl','Sooty Owl','Square-tailed Kite','Barking Owl')) AND " +
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_restricted_wbse': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': {'DAP': '500m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '500m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'White-bellied Sea-Eagle') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_restricted_ghawk': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': {'DAP': '250m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '250m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME = 'Grey Goshawk') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_restricted_bat': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': {'DAP': '100m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '100m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Grey-headed Flying-fox','Eastern Horseshoe Bat','Common Bent-wing Bat','Eastern Bent-winged Bat')) and " + 
                "(EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_restricted': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME not in ('Masked Owl','Powerful Owl','Sooty Owl','Square-tailed Kite','Barking Owl'," + 
                "'Grey-headed Flying-fox','Eastern Horseshoe Bat','Common Bent-wing Bat','Eastern Bent-winged Bat'," +
                "'White-bellied Sea-Eagle','Grey Goshawk'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID", "COLLECTOR", "FFG_DESC", "EPBC_DESC", "MAX_ACC_KM", "RECORD_ID", "STARTDATE"],
            'value_type': 'Fauna_Restricted',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },

        'evc': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\NV2005_EVCBCS",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': None,
            'fields': ["X_EVCNAME", "VEG_CODE"],
            'value_type': 'EVC',
            'value_field': 'X_EVCNAME',
            'description_field': 'VEG_CODE',
            'id_field': None
        },
        'lbp_colonies': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\LBPAG_BUFF_CHRFA",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'high_risk_only': True,
            'where_clause': None,
            'fields': ["LBP_DESC"],
            'value_type': 'LBP Colony',
            'value_field': 'LBP_DESC',
            'description_field': None,
            'id_field': None
        },
        'monitoring_bio': {
            'path': "{regional}\\RegionalData.gdb\\BLD_LAND_MANAGEMENT_SITES",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "(SITE_CATEGORY IN('FAUNA', 'FLORA') OR RISK_CODE = 'LittoralRF') AND TIMEFRAME <> 'NOT ACTIVE'",
            'fields': ["SITE_NAME", "RISK_CODE", "LMS_ID"],
            'value_type': 'Bio Monitoring',
            'value_field': 'SITE_NAME',
            'description_field': 'RISK_CODE',
            'id_field': 'LMS_ID'
        },
        'species_recovery_overlay_gbc': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_GBC = 'Yes'",
            'fields': ["PU_ID", "SRO_GBC"],
            'value_type': 'SRO - GBC',
            'value_field': 'SRO_GBC',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'species_recovery_overlay_dpy': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_DPy = 'Yes'",
            'fields': ["PU_ID", "SRO_DPy"],
            'value_type': 'SRO - DPy',
            'value_field': 'SRO_DPy',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'species_recovery_overlay_sgg': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_SGG = 'Yes'",
            'fields': ["PU_ID", "SRO_SGG"],
            'value_type': 'SRO - SGG',
            'value_field': 'SRO_SGG',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'species_recovery_overlay_mo': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_MO = 'Yes'",
            'fields': ["PU_ID", "SRO_MO"],
            'value_type': 'SRO - MO',
            'value_field': 'SRO_MO',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'species_recovery_overlay_so': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_SO = 'Yes'",
            'fields': ["PU_ID", "SRO_SO"],
            'value_type': 'SRO - SO',
            'value_field': 'SRO_SO',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'species_recovery_overlay_stq': {
            'path': "{regional}\\RegionalData.gdb\\BLD_SpeciesRecoveryOverlay_20210611",
            'buffer': '100m',
            'modes': ['JFMP', 'NBFT'],
            'where_clause': "SRO_STQ = 'Yes'",
            'fields': ["PU_ID", "SRO_STQ"],
            'value_type': 'SRO - STQ',
            'value_field': 'SRO_STQ',
            'description_field': None,
            'id_field': 'PU_ID'
        },
        'rainforest': {
            'path': "{csdl}\\FORESTS.GDB\\RAINFOR",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "CHECKED = 1", # Edited from "RF = 1" because field RF doesn't exist
            'fields': ["EVC_RF"],
            'value_type': 'Rainforest',
            'value_field': 'EVC_RF',
            'description_field': None,
            'id_field': None
        },
        'rainforest_clip': {
            'path': "{csdl}\\FORESTS.GDB\\RAINFOREST_CLIP",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "RF = 1", 
            'fields': ["EVC_RF"],
            'value_type': 'Rainforest - Clip',
            'value_field': 'EVC_RF',
            'description_field': None,
            'id_field': None
        },
        'rainforest_100': {
            'path': "{csdl}\\FORESTS.GDB\\RAINFOR100_CH",
            'buffer': {'DAP': '50m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '50m'},
            'where_clause': "RF = 1", 
            'fields': ["SRC"],
            'value_type': 'Rainforest_100',
            'value_field': 'SRC',
            'description_field': None,
            'id_field': None
        },
        'aquatic': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\ARI_AQUA_CATCH",
            'buffer': {'DAP': '1m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '1m'},
            'where_clause': None,
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID"],
            'value_type': 'Aquatic',
            'value_field': ['COMM_NAME', 'SCI_NAME'],
            'description_field': 'COMM_NAME',
            'id_field': 'TAXON_ID'
        }
    },
    
    # HERITAGE THEME
    'heritage': {
        'achris_sites_prelim': {
            'path': "{csdl_culture}\\prelim_ch_change_detection\\data",
            'buffer': {'DAP': '550m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '550m'},
            'where_clause': None,
            'fields': ["COMPONENT_NO", "PLACE_NAME", "COMPONENT_TYPE", "DATE_MODIFIED"],
            'value_type': 'Heritage Site - Preliminary',
            'value_field': 'COMPONENT_NO',
            'description_field': 'PLACE_NAME',
            'id_field': 'COMPONENT_NO'
        },
        'achris_sites': {
            'path': "{csdl_culture}\\ACHP_FIRESENS",
            'buffer': {'DAP': '550m', 'JFMP': {'500m', '1000m_ring'}, 'NBFT': '550m'},
            'where_clause': None,
            'fields': ["COMPONENT_NO", "PLACE_NAME", "COMPONENT_TYPE", "DATE_MODIFIED", "FIRE_SENSITIVITY"],
            'value_type': 'Heritage Site',
            'value_field': 'COMPONENT_NO',
            'description_field': 'PLACE_NAME',
            'id_field': 'COMPONENT_NO'
        },
        'rap_areas': {
            'path': "{csdl}\\CULTURE.gdb\\RAP",
            'where_clause': None,
            'fields': ["NAME"],
            'value_type': 'RAP Area',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        },
        'cultural_sensitivity': {
            'path': "{csdl}\\CULTURE.gdb\\SENSITIVITY_PUBLIC",
            'where_clause': None,
            'fields': ["SENSITIVITY"],
            'value_type': 'Cultural Sensitivity',
            'value_field': 'SENSITIVITY',
            'description_field': None,
            'id_field': None
        },
        'joint_managed_parks': {
            'path': "{regional}\\RegionalData.gdb\\GLaWACJointManagedParks_Dissolved",
            'where_clause': None,
            'fields': ["JointManagedPark"],
            'value_type': 'Joint Managed Park',
            'value_field': 'JointManagedPark',
            'description_field': 'None',
            'id_field': None
        },
        'plm25': {
            'path': "{csdl}\\CROWNLAND.GDB\\PLM25",
            'where_clause': None,
            'fields': ["MMTGEN", "MNG_SPEC", "ACT"],
            'value_type': 'Land Tenure',
            'value_field': 'MMTGEN',
            'description_field': 'MNG_SPEC',
            'id_field': None
        },
    },
    
    # SUMMARY THEME
    'summary': {
        'plm25': {
            'path': "{csdl}\\CROWNLAND.GDB\\PLM25",
            'where_clause': None,
            'fields': ["MMTGEN", "MNG_SPEC", "ACT"],
            'value_type': 'Land Tenure',
            'value_field': 'MMTGEN',
            'description_field': 'MNG_SPEC',
            'id_field': None
        },
        'planning_zones': {
            'path': "{csdl}\\VMPLAN.GDB\\PLAN_ZONE",
            'where_clause': None,
            'fields': ["ZONE_CODE", "LGA"],
            'value_type': 'Planning Zone',
            'value_field': 'ZONE_CODE',
            'description_field': 'LGA',
            'id_field': None
        },
        'forest_type': {
            'path': "{csdl}\\FORESTS.GDB\\FORTYPE500",
            'where_clause': None,
            'fields': ["X_DESC"],
            'value_type': 'Forest Type',
            'value_field': 'X_DESC',
            'description_field': None,
            'id_field': None
        },
        'native_title': {
            'path': "{regional}\\RegionalData.gdb\\GUNAIKURNAI_DETERMINATION",
            'where_clause': None,
            'fields': ["NT_Name", "Tribunal_No", "NT_STATUS"],
            'value_type': 'Native Title',
            'value_field': 'NT_Name',
            'description_field': 'NT_STATUS',
            'id_field': 'Tribunal_No'
        }
    },
    
    # WATER THEME
    'water': {
        'watercourse': {
            'path': "{csdl}\\VMHYDRO.gdb\\HY_WATERCOURSE",
            'where_clause': "FEATURE_TYPE_CODE <> '' OR FEATURE_TYPE_CODE IS NOT NULL",
            'fields': ["NAME", "FEATURE_TYPE_CODE"],
            'value_type': 'Watercourse',
            'value_field': 'NAME',
            'description_field': 'FEATURE_TYPE_CODE',
            'id_field': None
        },
        'cma_boundaries': {
            'path': "{csdl}\\CATCHMENTS.gdb\\CMA100",
            'where_clause': None,
            'fields': ["CMANAME"],
            'value_type': 'CMA Boundary',
            'value_field': 'CMANAME',
            'description_field': None,
            'id_field': None
        }
    }
}
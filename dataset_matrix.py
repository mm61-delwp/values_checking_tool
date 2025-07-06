# ============================================================================
# Dataset Processing Matrix
# ============================================================================

"""
NOTE: 'buffer' can be a string, e.g. 'buffer: '1m' which will be applied to all modes
      or a dict, e.g. 'buffer': {'DAP': '1m', 'JFMP': '50m', 'NBFT': '1m', 'LRLI': '1m'}
      Should default to 1m if it can't find a match.
NOTE: 'modes' is OPTIONAL. If included, the layer will be processed for any mode in the list
      e.g. 'modes': ['DAP', 'JFMP'] will not be processed in NBFT or LRLI mode
"""

DATASET_MATRIX = {
    # FORESTS THEME
    'forests': {
        'fmz': {
            'path': "{csdl}\\FORESTS.GDB\\FMZ100",
            'buffer': {'DAP': '1m', 'JFMP': '50m', 'NBFT': '1m', 'LRLI': '1m'},
            'modes': ['DAP', 'JFMP', 'NBFT', 'LRLI'],
            'where_clause': "FMZDIS IN('SPZ', 'SMZ')",
            'fields': ["FMZDIS", "DESC1", "DETAILNO"],
            'value_type': 'FMZ',
            'value_field': 'FMZDIS',
            'description_field': 'DESC1',
            'id_field': 'DETAILNO'
        },
        'monitoring_forest': {
            'path': "{regional}\\RegionalData.gdb\\BLD_LAND_MANAGEMENT_SITES",
            'buffer': '1m',
            'where_clause': "(SITE_CATEGORY IN('FOREST','FIRE')) AND TIMEFRAME <> 'NOT ACTIVE'",
            'fields': ["SITE_ID", "SITE_NAME", "LMS_ID"],
            'value_type': 'Monitoring Site',
            'value_field': 'SITE_ID',
            'description_field': 'SITE_NAME',
            'id_field': 'LMS_ID'
        },
        'recweb_sites': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_SITE",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["NAME", "FAC_TYPE", "SERIAL_NO"],
            'value_type': 'REC SITES',
            'value_field': 'NAME',
            'description_field': 'FAC_TYPE',
            'id_field': 'SERIAL_NO'
        },
        'recweb_assets': {
            'path': "{csdl}\\FORESTS.GDB\\RECWEB_ASSET",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["NAME", "ASSET_CLS", "SERIAL_NO"],
            'value_type': 'ASSET',
            'value_field': 'NAME',
            'description_field': 'ASSET_CLS',
            'id_field': 'SERIAL_NO'
        },
        'historic_sites': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\HIST100_POINT",
            'buffer': '250m',
            'where_clause': None,
            'fields': ["NAME"],
            'value_type': 'Historic Heritage Site',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        },
        'trp_coupes': {
            'path': "{csdl}\\FORESTRY.GDB\\TRP",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["COUPE"],
            'value_type': 'TRP Coupe',
            'value_field': 'COUPE',
            'description_field': None,
            'id_field': None
        },
        'burn_plan': {
            'path': "{csdl}\\FIRE.GDB\\BURNPLAN25",
            'buffer': '1m',
            'where_clause': "REGION = 'Gippsland'",
            'fields': ["TREAT_NO", "TREAT_NAME"],
            'value_type': 'Joint Fuel Management Plan',
            'value_field': 'TREAT_NO',
            'description_field': 'TREAT_NAME',
            'id_field': None
        },
        'giant_trees': {
            'path': "{csdl}\\FORESTS.GDB\\EG_GIANT_TREES",
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
            'buffer': '10m',
            'where_clause': None,
            'fields': ["NAME", "EASTING", "NORTHING"],
            'value_type': 'Alpine Hut',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        }
    },
    
    # BIODIVERSITY THEME
    'biodiversity': {
        'vba_flora25': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FLORA25",
            'buffer': '50m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND (EPBC_DESC in ('Endangered','Vulnerable','Critically Endangered') OR OLD_VICADV in ('e','v','P','x') OR FFG in('cr','en','vu','th','cd','en-x','L'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Flora',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna25': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\VBA_FAUNA25",
            'buffer': '50m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND (EPBC_DESC in ('Endangered','Vulnerable','Critically Endangered') OR OLD_VICADV in ('cr','en','vu','wx') OR FFG in ('cr','en','vu','th','cd','en-x','L') OR COMM_NAME = 'Koala')",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Fauna',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_flora_threatened': {
            'path': "{csdl_restricted}\\VBA_FLORA_THREATENED",
            'buffer': '50m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Flora',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_threatened': {
            'path': "{csdl_restricted}\\VBA_FAUNA_THREATENED",
            'buffer': '50m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Fauna',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_flora_restricted': {
            'path': "{csdl_restricted}\\VBA_FLORA_RESTRICTED",
            'buffer': '500m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5)",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Flora',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'vba_fauna_restricted': {
            'path': "{csdl_restricted}\\VBA_FAUNA_RESTRICTED",
            'buffer': '500m',
            'where_clause': "(STARTDATE > date '1980-01-01 00:00:00') AND (MAX_ACC_KM <= 0.5) AND " +
                "(COMM_NAME in ('Masked Owl','Powerful Owl','Sooty Owl','Square-tailed Kite','Barking Owl')) AND (EXTRA_INFO in ('Roost site','Breeding')) OR " +
                "(COMM_NAME = 'White-bellied Sea-Eagle') and (EXTRA_INFO in ('Roost site','Breeding')) OR " +
                "(COMM_NAME in ('Grey-headed Flying-fox','Eastern Horseshoe Bat','Common Bent-wing Bat','Eastern Bent-winged Bat')) and (EXTRA_INFO in ('Roost site','Breeding')) OR " +
                "(COMM_NAME = 'Grey Goshawk') and (EXTRA_INFO in ('Roost site','Breeding'))",
            'fields': ["SCI_NAME", "COMM_NAME", "TAXON_ID", "EXTRA_INFO", "RECORD_ID"],
            'value_type': 'Fauna',
            'value_field': 'SCI_NAME',
            'description_field': 'COMM_NAME',
            'id_field': 'RECORD_ID'
        },
        'evc': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\NV2005_EVCBCS",
            'buffer': '50m',
            'where_clause': None,
            'fields': ["X_EVCNAME", "VEG_CODE"],
            'value_type': 'EVC',
            'value_field': 'X_EVCNAME',
            'description_field': 'VEG_CODE',
            'id_field': None
        },
        'lbp_colonies': {
            'path': "{csdl}\\FLORAFAUNA1.GDB\\LBPAG_BUFF_CHRFA",
            'buffer': '50m',
            'where_clause': None,
            'fields': ["LBP_DESC"],
            'value_type': 'LBP Colony',
            'value_field': 'LBP_DESC',
            'description_field': None,
            'id_field': None
        },
        'monitoring_bio': {
            'path': "{regional}\\RegionalData.gdb\\BLD_LAND_MANAGEMENT_SITES",
            'buffer': '50m',
            'where_clause': "(SITE_CATEGORY IN('FAUNA', 'FLORA') OR RISK_CODE = 'LittoralRF') AND TIMEFRAME <> 'NOT ACTIVE'",
            'fields': ["SITE_NAME", "RISK_CODE", "LMS_ID"],
            'value_type': 'Bio Monitoring',
            'value_field': 'SITE_NAME',
            'description_field': 'RISK_CODE',
            'id_field': 'LMS_ID'
        },
        'rainforest': {
            'path': "{csdl}\\FORESTS.GDB\\RAINFOR",
            'buffer': '50m',
            'where_clause': "CHECKED = 1", # Edited from "RF = 1" because field RF doesn't exist
            'fields': ["EVC_RF"],
            'value_type': 'Rainforest',
            'value_field': 'EVC_RF',
            'description_field': None,
            'id_field': None
        }
    },
    
    # HERITAGE THEME
    'heritage': {
        'achris_sites': {
            'path': "{csdl_culture}\\ACHP_FIRESENS",
            'buffer': '550m',
            'where_clause': None,
            'fields': ["COMPONENT_NO", "PLACE_NAME", "COMPONENT_TYPE", "DATE_MODIFIED", "FIRE_SENSITIVITY"],
            'value_type': 'Heritage Site',
            'value_field': 'COMPONENT_NO',
            'description_field': 'PLACE_NAME',
            'id_field': 'COMPONENT_NO'
        },
        'rap_areas': {
            'path': "{csdl}\\CULTURE.gdb\\RAP",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["NAME"],
            'value_type': 'RAP Area',
            'value_field': 'NAME',
            'description_field': None,
            'id_field': None
        },
        'cultural_sensitivity': {
            'path': "{csdl}\\CULTURE.gdb\\SENSITIVITY_PUBLIC",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["SENSITIVITY"],
            'value_type': 'Cultural Sensitivity',
            'value_field': 'SENSITIVITY',
            'description_field': None,
            'id_field': None
        }
    },
    
    # SUMMARY THEME
    'summary': {
        'plm25': {
            'path': "{csdl}\\CROWNLAND.GDB\\PLM25",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["MMTGEN", "MNG_SPEC", "ACT"],
            'value_type': 'Land Tenure',
            'value_field': 'MMTGEN',
            'description_field': 'MNG_SPEC',
            'id_field': None
        },
        'planning_zones': {
            'path': "{csdl}\\VMPLAN.GDB\\PLAN_ZONE",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["ZONE_CODE", "LGA"],
            'value_type': 'Planning Zone',
            'value_field': 'ZONE_CODE',
            'description_field': 'LGA',
            'id_field': None
        },
        'forest_type': {
            'path': "{csdl}\\FORESTS.GDB\\FORTYPE500",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["X_DESC"],
            'value_type': 'Forest Type',
            'value_field': 'X_DESC',
            'description_field': None,
            'id_field': None
        },
        'native_title': {
            'path': "{regional}\\RegionalData.gdb\\GUNAIKURNAI_DETERMINATION",
            'buffer': '1m',
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
            'buffer': '1m',
            'where_clause': None,
            'value_type': 'Watercourse',
            'value_field': 'NAME',
            'description_field': 'FEATURE_TYPE_CODE',
            'id_field': None
        },
        'cma_boundaries': {
            'path': "{csdl}\\CATCHMENTS.gdb\\CMA100",
            'buffer': '1m',
            'where_clause': None,
            'fields': ["CMANAME"],
            'value_type': 'CMA Boundary',
            'value_field': 'CMANAME',
            'description_field': None,
            'id_field': None
        }
    }
}
# Mitigation lookup tables
FOREST_MITIGATIONS = {
    'Monitoring Site': "Prior to works, inform the contact listed on research site",
    'PEST_PLANT': "Ensure hygiene practices to reduce weed spread risk. Refer to Pest Plants Management Guideline",
    'Agricultural Chemical Control Area': "ACCA permit required for herbicide use. Contact Agriculture Victoria",
    'Phytophthora Risk': "Refer to Gippsland FMP risk mitigation strategies and Phytophthora SOP",
    'Joint Fuel Management Plan': "Engage with district planned burn officer to confirm no conflicts",
    'Mining Site': "Adopt OH&S procedures, notify licensee if active site",
    'Apiary Site': "Ensure no negative impacts on apiary operations, contact licensee via Land Folio",
    'Historic Heritage Site': "May require Heritage Victoria permit/consent. Refer to Historic Places Management Guideline",
    'TRP Coupe': "Engage with relevant project planning team",
    'FMZ': "Refer to Action Statement and SMZ plan. See Planning Standards for timber harvesting 2014",
    'Giant Tree': "Engage with Regional NEP team, especially for native veg removal",
    'Alpine Hut': "Engage with District Forest Planning Officer/Alpine Huts association/Parks Victoria",
    'REC SITES': "Recweb asset present. Engage with District Forest Planning Officer/Regional Recreation Planning Team",
    'ASSET': "Recweb asset present. Engage with District Forest Planning Officer/Regional Recreation Planning Team",
    'Powerline': "Contact asset manager if within 6.4m. Ausnet spotter required if asset affected",
    'Pipeline': "Contact asset manager. No steel tracked crossing. Use dial before you dig service",
    'Railway': "Contact asset manager. VicTrack permit may be required if on their land"
}

HERITAGE_MITIGATIONS = {
    # (risk_level, sites_exist, sensitivity)
    ('LRLI', 'No',  'No' ): "No known sites. Apply contingency plan if CH discovered. Remain in existing footprint",
    ('LRLI', 'No',  'Yes'): "No known sites but culturally sensitive area. Use machinery caution. Apply contingency plan",
    ('DAP',  'No',  'No' ): "No known sites or sensitivity. Remain in disturbed footprint. Contingency plan on site",
    ('DAP',  'No',  'Yes'): "Culturally sensitive area. Remain in disturbed footprint. Contingency plan on site",
    ('DAP',  'Yes', 'No' ): "Sites detected. Heritage specialist assessment required. Permit if harm unavoidable",
    ('DAP',  'Yes', 'Yes'): "Sites and sensitivity detected. Heritage specialist assessment required. Permit if harm unavoidable"
}

NATIVE_TITLE_MATRIX = {
    'NT_EXTINGUISHED': "Native Title Extinguished - No Procedural Rights Observed",
    'LOW_IMPACT': "Low Impact/Exempt Activity - Assessment Not Required",
    'CONSULT': "Seek Further Advice - Consult NT Assessor", 
    'GLAWAC_FAA': "Future Act Rights Apply - Gunaikurnai Notices (Determination Area)",
    'OTHER_FAA': "Future Act Rights Apply - FNLRS Notices (Non-Determined)"
}

# Example including biodiversity risk register. How to maintain?
MITIGATIONS = {
    'JFMP': {
        'biodiversity': {
            'EVC': {
                # Key = Value_Description (VEG_CODE)
                'WPro0858': 'Autumn burning preferred for this EVC to maintain floristic diversity and avoiding impacts to annual species (obligate seeders).',
                'EGL_0018': 'Avoid direct ignition during burning. This EVC contains riparian vegetation.',
                'GipP0018': 'Avoid direct ignition during burning. This EVC contains riparian vegetation.'
                },
            'Flora': {
                # KEY = Value_Description (TAXON_ID)
                '500002': 'Exclude sites with records of this species from works associated with burning and roading. Ensure works do not alter current drainage patterns near records of this species.',
                '500009': 'Exclude sites with records of this species from works associated with burning and roading. Ensure works do not alter current drainage patterns near records of this species.',
                '500010': 'Exclude sites with records of this species from works associated with burning and roading. Establish buffer of 30m radius around record of this species to protect known populations from disturbance (earthworks, machinery and vehicles), in particular where plants occur on roadsides and are at risk of damage from vehicles. Ensure works do not alter current drainage patterns near records of this species.',
            }
        },
    },
    'DAP': {
        'biodiversity': {},
        'forests': {}
    }
}

# Example option to remove hard-coded stuff from main script using multi-level lookup
# MITIGATIONS = {
#     ('JFMP', 'forests', 'biodiversity', 'EVC', Actual_EVC_goes_here): "Mitigation here",
#     ('JFMP', 'forests', 'Flora', 'TAXON', Specific_taxon_goes_here): "Mitigation here"
# }
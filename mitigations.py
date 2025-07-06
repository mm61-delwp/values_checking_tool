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
    ('LRLI', 'No', 'No'): "No known sites. Apply contingency plan if CH discovered. Remain in existing footprint",
    ('LRLI', 'No', 'Yes'): "No known sites but culturally sensitive area. Use machinery caution. Apply contingency plan",
    ('DAP', 'No', 'No'): "No known sites or sensitivity. Remain in disturbed footprint. Contingency plan on site",
    ('DAP', 'No', 'Yes'): "Culturally sensitive area. Remain in disturbed footprint. Contingency plan on site",
    ('DAP', 'Yes', 'No'): "Sites detected. Heritage specialist assessment required. Permit if harm unavoidable",
    ('DAP', 'Yes', 'Yes'): "Sites and sensitivity detected. Heritage specialist assessment required. Permit if harm unavoidable"
}

NATIVE_TITLE_MATRIX = {
    'NT_EXTINGUISHED': "Native Title Extinguished - No Procedural Rights Observed",
    'LOW_IMPACT': "Low Impact/Exempt Activity - Assessment Not Required",
    'CONSULT': "Seek Further Advice - Consult NT Assessor", 
    'GLAWAC_FAA': "Future Act Rights Apply - Gunaikurnai Notices (Determination Area)",
    'OTHER_FAA': "Future Act Rights Apply - FNLRS Notices (Non-Determined)"
}
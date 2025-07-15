# ============================================================================
# Values Checking Tool - Version 0.0.0.2 
# Updated July 7th 2025
# Department of Energy, Environment and Climate Action
# Gippsland rulz
# ============================================================================

import arcpy
import pandas as pd
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

from dataset_matrix import DATASET_MATRIX
from qbid_matrix import QBID_MATRIX, QBID2_MATRIX
from mitigations import FOREST_MITIGATIONS, HERITAGE_MITIGATIONS, NATIVE_TITLE_MATRIX


# ============================================================================
# Configuration Classes
# ============================================================================

@dataclass
class Settings:
    """Main configuration"""
    input_data: str
    workspace: Path
    mode: str = "DAP"
    themes: List[str] = None
    district: str = None
    
    def __post_init__(self):
        if self.themes is None:
            self.themes = ["forests", "biodiversity"]
        self.workspace = Path(self.workspace)
        self.workspace.mkdir(exist_ok=True)

@dataclass
class DatasetConfig:
    """Configuration for a single dataset"""
    # Note: this is important for parsing dataset matrix and assigning default/optional values
    path: str
    fields: List[str]
    value_type: str
    buffer: Union[str, Dict[str, Union[str, set[str]]]] = '1m'
    where_clause: Optional[str] = None
    value_field: Optional[str] = None
    description_field: Optional[str] = None
    id_field: Optional[str] = None
    high_risk_only: bool = False
    modes: Optional[List[str]] = None


# ============================================================================
# Main Processing Engine
# ============================================================================

class ValuesChecker:
    """Main processing engine for values checking"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = self._setup_logging()
        self.start_date = datetime.now().strftime("%Y%m%d") #("%d%m%Y")
        self.temp_datasets = []
        self._setup_arcpy_environment()
    
    def process(self) -> Dict:
        """
        Main processing workflow - this is the primary entry point
        
        WOT IT DOES
        1. Setup workspace and prepare input data including buffered versions of features to check
        2. Process each theme to find intersecting values
        3. Apply mitigations to results
        4. Generate output files
        6. Cleanup temporary data
        """
        try:
            self.logger.info(f"Starting values checking - Mode: {self.settings.mode}")
            
            # Phase 1: Data Preparation
            self.logger.info("Phase 1: Preparing data...")
            self._setup_workspace()
            working_data = self._prepare_input_data()
            buffered_layers = self._create_all_buffers(working_data)
            
            # Phase 2: Values Detection
            self.logger.info("Phase 2: Detecting values...")
            all_results = {}
            for theme in self.settings.themes:
                self.logger.info(f"Processing {theme} theme...")
                theme_results = self._process_single_theme(theme, buffered_layers)
                all_results[theme] = theme_results
                self.logger.info(f"Found {len(theme_results)} values for {theme} theme")
                print("-" * 60)
            
            # Phase 3: Apply Mitigations
            self.logger.info("Phase 3: Applying mitigations...")
            mitigated_results = self._apply_all_mitigations(all_results)
            
            # Phase 4: Generate Outputs
            self.logger.info("Phase 4: Generating outputs...")
            outputs = self._generate_all_outputs(mitigated_results, working_data)
            
            self.logger.info("Processing completed successfully")
            return {'success': True, 'outputs': outputs, 'results': mitigated_results}
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
            
        finally:
            # Phase 5: Clean up temporary files
            self._cleanup_temp_data()
    
    # ========================================================================
    # Phase 1: Data Preparation Methods
    # ========================================================================
    
    def _setup_workspace(self):
        """Setup output geodatabase"""
        output_gdb = self.settings.workspace / "Values_Checking_Output.gdb"
        if output_gdb.exists():
            arcpy.env.workspace = str(output_gdb)

            # Clear existing data
            self.logger.warning("Dataset deletion disabled for debugging - fix this later")
            for fc in arcpy.ListFeatureClasses(): 
                a = 1 # arcpy.management.Delete(fc) # !! NOTE: Temporarily disabled for faster debugging
            for tbl in arcpy.ListTables(): 
                arcpy.management.Delete(tbl)
        else:
            arcpy.management.CreateFileGDB(str(self.settings.workspace), "Values_Checking_Output.gdb")
        
        arcpy.env.workspace = str(output_gdb)
        self.logger.info(f"Workspace set up at {output_gdb}")
    
    def _prepare_input_data(self) -> str:
        """Create working copy of input data with geometry fields"""
        working_copy = "works_shapefile"

        # create a copy of the input feature class, excluding features without valid ID_FIELD
        arcpy.conversion.FeatureClassToFeatureClass(
            self.settings.input_data, arcpy.env.workspace, working_copy,
            f'{ID_FIELD} <> \'\''
        )
        
        # Add and calculate geometry fields
        self._add_geometry_fields(working_copy)
        self.temp_datasets.append(working_copy)
        count_feat = arcpy.GetCount_management(working_copy)
        self.logger.info(f"{self.settings.input_data} cleaned and copied ({count_feat} features)")
        
        return working_copy
    
    def _create_all_buffers(self, input_data: str) -> Dict[str, str]:
        """Create all required buffer distances for analysis"""
        buffers = {}
        buffer_names = []
        
        # Process buffers in dependency order
        for buffer_name, config in BUFFERS.items():
            buffer_layer = f"buffer_{buffer_name}"
            buffer_path = os.path.join(arcpy.env.workspace, buffer_layer)
            
            if not arcpy.Exists(buffer_path):
                # Determine input features - are we buffering the original features or buffering an existing buffer?
                input_features = config['input_features']
                if input_features == "input_layer":
                    arcpy.analysis.Buffer(
                    in_features=input_data,
                    out_feature_class=buffer_layer,
                    buffer_distance_or_field=config['buffer_distance'],
                    line_side="FULL",
                    line_end_type="ROUND",
                    dissolve_option="NONE",
                    dissolve_field=None,
                    method="PLANAR"
                )
                else:
                    # Use previously created buffer
                    input_path = os.path.join(arcpy.env.workspace, config['input_features'])
                    arcpy.analysis.Buffer(
                    in_features=input_path,
                    out_feature_class=buffer_layer,
                    buffer_distance_or_field=config['buffer_distance'],
                    line_side="OUTSIDE_ONLY",
                    line_end_type="ROUND",
                    dissolve_option="NONE",
                    dissolve_field=None,
                    method="PLANAR"
                )
            
            buffers[buffer_name] = buffer_layer
            self.temp_datasets.append(buffer_layer)
            self.logger.debug(f"Created {buffer_name} buffer with type {config['buffer_type']}")
            buffer_names.append(buffer_name)
        
        self.logger.info(f"Buffers created: {', '.join(buffer_names)}")
        return buffers
    
    # ========================================================================
    # Phase 2: Values Detection Methods
    # ========================================================================
    
    def _process_single_theme(self, theme: str, buffered_layers: Dict[str, str]) -> List[Dict]:
        """Process all datasets for a single theme"""
              
        # Get dataset configurations for this theme
        if theme not in DATASET_MATRIX:
            self.logger.warning(f"No datasets configured for theme: {theme}")
            return []
        
        theme_datasets = DATASET_MATRIX[theme]
        
        # Process each dataset in the theme
        all_theme_results = []
        
        for dataset_name, config in theme_datasets.items():
            try:
                # Unpack configuration fields, applying defaults & type
                config = DatasetConfig(**config)

                if self._is_dataset_enabled_for_mode(config):
                    for buffer in self._get_buffer_list(config):
                        dataset_results = self._process_single_dataset(dataset_name, config, buffer, buffered_layers, theme)
                        all_theme_results.extend(dataset_results)
                        self.logger.info(f"Processed {dataset_name} with {buffer[7:]} buffer: {len(dataset_results)} values found")
                else:
                    self.logger.info(f"Skipped {dataset_name} as it is disabled in {MODE} mode")
            except Exception as e:
                self.logger.warning(f"Failed to process {dataset_name}: {e}")

        return all_theme_results
    
    def _process_single_dataset(self, dataset_name: str, config: DatasetConfig, 
                           buffer_name: str, buffered_layers: Dict[str, str], theme: str) -> List[Dict]:
        """Process a single dataset using its configuration"""
        
        # Step 1: Resolve dataset path and check existence
        values_layer_path = config.path.format(**DATA_PATHS)

        if not arcpy.Exists(values_layer_path):
            self.logger.warning(f"Dataset not found: {values_layer_path}")
            return []
        
        # Step 2: Apply selection criteria to values layer if specified
        values_layer = values_layer_path
        if config.where_clause:
            values_layer = arcpy.management.SelectLayerByAttribute(values_layer_path, "NEW_SELECTION", config.where_clause)

        # Step 3: Apply LRLI filter to works layer if specified
        if config.high_risk_only:
            works_layer = arcpy.management.SelectLayerByAttribute(buffer_name, "NEW_SELECTION", f"{RISK_LEVEL_FIELD} <> 'LRLI'")
        else:
            works_layer = buffer_name

        # Step 4: quick check of how many features remain after selection/filtering
        values_count = int(arcpy.GetCount_management(values_layer)[0])
        works_count = int(arcpy.GetCount_management(works_layer)[0])
        
        # Step 5: Perform spatial intersection
        if values_count > 0 and works_count > 0:
            intersect_output = f"intersect_{dataset_name}_{buffer_name}"
            intersect_result = arcpy.analysis.Intersect([works_layer, values_layer], intersect_output, "ALL")
            self.temp_datasets.append(intersect_output)
        else:
            self.logger.warning(f"No features after selection criteria: {dataset_name}, {config.where_clause}")
            return []

        # Step 6: Extract and return results
        if intersect_result:
            return self._extract_results_from_intersection(dataset_name, intersect_result, config, theme, buffer_name)
        else:
            self.logger.warning(f"No intersections between: {buffer_name}, {dataset_name}")
            return []
    
    def _extract_results_from_intersection(self, dataset_name: str, intersect_result: str, config: DatasetConfig, theme: str, buffer_layer: str) -> List[Dict]:
        """Extract structured results from intersection output"""
        
        # Prepare and validate fields
        available_fields = [f.name for f in arcpy.ListFields(intersect_result)]   # List all intersecting fields
        valid_fields = [ID_FIELD, NAME_FIELD, DESCRIPTION_FIELD, DISTRICT_FIELD, RISK_LEVEL_FIELD]   # list standard fields
        valid_fields.extend([f for f in config.fields if f in available_fields])  # add values configuration fields that exist in intersection
        
        if len(valid_fields) < 3:  # Need at least DAP_REF_NO, DAP_NAME, DISTRICT
            self.logger.warning(f"Insufficient fields available for {intersect_result}")
            return []
        
        # Dissolve features to deal with e.g. multiple intersections with same SMZ
        dissolve_result = f"dissolve_{dataset_name}"
        arcpy.analysis.PairwiseDissolve(intersect_result, dissolve_result, dissolve_field=valid_fields, multi_part="MULTI_PART")
        self._add_geometry_fields(dissolve_result)
        valid_fields.extend(['X', 'Y'])  # add coordinate fields to list of fields
        self.temp_datasets.append(dissolve_result)

        # Extract data using cursor
        results = []
        with arcpy.da.SearchCursor(dissolve_result, valid_fields) as cursor:
            for row in cursor:
                if not row[0]:  # Skip if no ID_FIELD
                    continue
                
                # Build result in desired format
                result = self._build_result_row(row, valid_fields, config, theme, buffer_layer)
                
                # add to output
                results.append(result)

        return results
    
    def _build_result_row(self, row: tuple, valid_fields: List[str], config: DatasetConfig, theme: str, buffer_layer: str) -> Dict:
        """Build the base result structure common to all themes"""
        result = {
            # Standard fields for all values datasets - from works feature class
            'UNIQUE_ID':   row[valid_fields.index(f'{ID_FIELD}')],
            'DISTRICT':    row[valid_fields.index(f'{DISTRICT_FIELD}')],
            'NAME':        row[valid_fields.index(f'{NAME_FIELD}')],
            'DESCRIPTION': row[valid_fields.index(f'{DESCRIPTION_FIELD}')],
            'RISK_LVL':    row[valid_fields.index(f'{RISK_LEVEL_FIELD}')],

            # Details of values - from overlapping values feature class
            'Theme': theme,
            'Value_Type': config.value_type,
            'Buffer': buffer_layer[7:], # Shorten buffer string, removing "buffer_" prefix,
            'Value': None,
            'Value_Description': None,
            'Value_ID': None,
            'X': int(row[valid_fields.index('X')] or 0),
            'Y': int(row[valid_fields.index('Y')] or 0),
            'QBID': None,
            'QBID_Alt': None,
            'DATE_CHECKED': self.start_date
            # Any remaining fields specified by 'fields' in values dataset configuration will be appended here
        }
        
        # Update value field data from value field or fields
        if isinstance(config.value_field, str): 
            # single value field; return single value to 'Value' field
            result['Value'] = row[valid_fields.index(config.value_field)]
        elif isinstance(config.value_field, list): 
            # multiple value fields; concatenate into 'Value' field with ', ' separator
            vf_values = []
            for vf in config.value_field:
                vf_values.append(row[valid_fields.index(vf)])
            vf_string = ", ".join(str(item) for item in vf_values)
            result['Value'] = vf_string

        # Update Value_ID field data from specified field, if specified
        if config.id_field:
            row[valid_fields.index({config.id_field})],
        
        # Update Value_Description field data from specified field, if specified
        if config.description_field:
            row[valid_fields.index(config.description_field)],
        
        # Add any aditional fields specified in dataset configuration
        for fieldname in config.fields:
            if fieldname not in result: 
                if fieldname not in filter(None, [config.value_field, config.id_field, config.description_field]):
                    result[fieldname] = row[valid_fields.index(fieldname)] or 'Field not found'

        # calculate quickbase id code
        result['QBID_Test'] = self._build_quickbase_id(result, theme)

        # alternative QBID
        qbid_fields = ["UNIQUE_ID", "Value_Type", "Value", "Value_ID", "X", "Y"]
        qbid_string = "|".join(str(result[item]) for item in qbid_fields if result[item] not in [None, "", 0])
        result['QBID_Alt'] = qbid_string
        
        return result
    
    
    # ========================================================================
    # Phase 3: Mitigation Application Methods
    # ========================================================================
    
    def _apply_all_mitigations(self, all_results: Dict) -> Dict:
        """Apply appropriate mitigations to all theme results"""
        mitigated_results = {}
        
        for theme, theme_results in all_results.items():
            self.logger.info(f"Applying mitigations for {theme} theme...")
            mitigated_results[theme] = []
            
            for result in theme_results:
                # mitigation = self._determine_mitigation(theme, result)
                if theme == "forests":
                    # return self._get_forest_mitigation(result)
                    """Get forest-specific mitigation"""
                    value_type = result.get('Value_Type', '')
                    mitigation = FOREST_MITIGATIONS.get(value_type, "Standard work practices apply")
                elif theme == "heritage":
                    # return self._get_heritage_mitigation(result)
                    risk_level = result.get('RISK_LVL', 'DAP')
                    sites_exist = 'Yes' if result.get('ACHRIS_ID') else 'No'
                    sensitivity = result.get('CH_SENS', 'No')
                    
                    matrix_key = (risk_level, sites_exist, sensitivity)
                    mitigation = HERITAGE_MITIGATIONS.get(matrix_key, "Heritage assessment required")
                elif theme == "summary":
                    # return self._get_native_title_mitigation(result)
                    nt_status = result.get('NT_STATUS', '')
                    risk_level = result.get('RISK_LVL', 'DAP')
                    
                    if 'EXTINGUISHED' in nt_status:
                        mitigation = NATIVE_TITLE_MATRIX['NT_EXTINGUISHED']
                    elif risk_level == 'LRLI':
                        mitigation = NATIVE_TITLE_MATRIX['LOW_IMPACT']
                    else:
                        mitigation = NATIVE_TITLE_MATRIX['CONSULT']
                elif theme == "biodiversity":
                    mitigation = "Refer to NEP team. Standard biodiversity protection measures apply"
                elif theme == "water":
                    mitigation = "Ensure works comply with waterway protection requirements"
                else:
                    mitigation = "Standard work practices apply"
                
                result['mitigation'] = mitigation
                mitigated_results[theme].append(result)
        
        return mitigated_results

    
    # ========================================================================
    # Phase 4: Output Generation Methods
    # ========================================================================
    
    def _generate_all_outputs(self, mitigated_results: Dict, working_data: str) -> List[str]:
        """Generate all output files"""
        outputs = []
        
        # Generate CSV reports for each theme that has results
        for theme, theme_results in mitigated_results.items():
            if theme_results:
                csv_file = self._create_theme_csv_report(theme, theme_results)
                outputs.append(csv_file)
        
        # Generate works detail report
        works_csv = self._create_works_detail_report(working_data)
        outputs.append(works_csv)

        # Generate QuickBase reports
        
        # Generate output shapefile
        shapefile = self._create_output_shapefile(working_data)
        outputs.append(shapefile)
        
        return outputs
    
    def _create_theme_csv_report(self, theme: str, results: List[Dict]) -> str:
        """Create CSV report for a specific theme"""
        df = pd.DataFrame(results)
        
        filename = f"{self.start_date}_{self.settings.mode}_{theme}_values.csv"
        filepath = self.settings.workspace / filename
        
        df.to_csv(filepath, index=False)
        self.logger.info(f"Created {theme} report: {filepath}")
        
        return str(filepath)
    
    def _create_works_detail_report(self, working_data: str) -> str:
        """Create detailed CSV report of all works"""
        works_data = []
        fields = [ID_FIELD, NAME_FIELD, DESCRIPTION_FIELD, RISK_LEVEL_FIELD, DISTRICT_FIELD, "AREA_HA", "X", "Y"]
        
        with arcpy.da.SearchCursor(working_data, fields) as cursor:
            for row in cursor:
                works_data.append(dict(zip(fields, row)))
        
        df = pd.DataFrame(works_data)
        
        filename = f"{self.start_date}_{self.settings.mode}_works_detail.csv"
        filepath = self.settings.workspace / filename
        
        df.to_csv(filepath, index=False)
        self.logger.info(f"Created works detail report: {filepath}")
        
        return str(filepath)
    
    def _create_output_shapefile(self, working_data: str) -> str:
        """Create output shapefile of processed works"""
        filename = f"{self.start_date}_{self.settings.mode}_works"
        filepath = self.settings.workspace / f"{filename}.shp"
        
        arcpy.conversion.FeatureClassToFeatureClass(
            working_data, str(self.settings.workspace), filename
        )
        
        self.logger.info(f"Created output shapefile: {filepath}")
        return str(filepath)
    
    # ========================================================================
    # Utility and Helper Methods
    # ========================================================================
    
    def _build_quickbase_id(self, rowdata:dict, theme:str) -> str:
        try:        
            qbid_fields = QBID_MATRIX[MODE][theme]
            qbid_string = "|".join(str(rowdata[item]) for item in qbid_fields if rowdata[item] not in [None, "", 0])
            
            return qbid_string
        
        except Exception as e:
            a=1
            # self.logger.warning(f"Failed to generate QBID: {e}")
        
        try:
            qbid_fields = ["UNIQUE_ID", "Value_Type", "Value", "Value_ID"]
            qbid_string = "|".join(str(rowdata[item]) for item in qbid_fields if rowdata[item] not in [None, "", 0])

            return qbid_string
        
        except Exception as e:
            # self.logger.warning(f"Failed to generate QBID: {e}")
            
            return rowdata['UNIQUE_ID']

    def _setup_arcpy_environment(self):
        """Configure ArcPy environment settings"""
        arcpy.env.overwriteOutput = True
        arcpy.env.scriptWorkspace = str(self.settings.workspace)
        arcpy.env.parallelProcessingFactor = "85%"
        arcpy.SetLogHistory(False)
        
        # Set spatial reference to VICGRID2020
        sr = arcpy.SpatialReference(7899)
        arcpy.env.outputCoordinateSystem = sr
    
    def _add_geometry_fields(self, feature_class: str):
        """Add and calculate geometry fields for the feature class based on geometry type"""
        try:
            # Add coordinate fields to all feature classes
            arcpy.management.AddField(feature_class, "X", "DOUBLE")
            arcpy.management.AddField(feature_class, "Y", "DOUBLE")
            
            # Get the geometry type of the feature class
            desc = arcpy.Describe(feature_class)
            geometry_type = desc.shapeType.upper()
            
            # Add and populate appropriate fields based on geometry type
            if geometry_type in ["POINT", "MULTIPOINT"]:

                # Calculate point coordinates
                with arcpy.da.UpdateCursor(feature_class, ["X", "SHAPE@X", "Y", "SHAPE@Y"]) as cursor:
                    for row in cursor:
                        row[0] = int(row[1]) if row[1] else 0  # Easting
                        row[2] = int(row[3]) if row[3] else 0  # Northing
                        cursor.updateRow(row)
                        
            elif geometry_type == "POLYGON":
                arcpy.management.AddField(feature_class, "AREA_HA", "DOUBLE")
                
                # Calculate polygon centroid and area
                with arcpy.da.UpdateCursor(feature_class, ["X", "Y", "AREA_HA", "SHAPE@"]) as cursor:
                    for row in cursor:
                        if row[3]:  # Check if geometry exists
                            centroid = row[3].centroid
                            # row[0] = int(centroid.X) if centroid.X else 0  # Easting
                            # row[1] = int(centroid.Y) if centroid.Y else 0  # Northing
                            row[2] = row[3].getArea('GEODESIC', 'HECTARES')  # Area in hectares
                        else:
                            row[0] = row[1] = row[2] = 0
                        cursor.updateRow(row)
                        
            elif geometry_type == "POLYLINE":
                arcpy.management.AddField(feature_class, "LENGTH_KM", "DOUBLE")

                # Calculate line midpoint and length
                with arcpy.da.UpdateCursor(feature_class, ["X", "Y", "LENGTH_KM", "SHAPE@"]) as cursor:
                    for row in cursor:
                        if row[3]:  # Check if geometry exists
                            # Get midpoint of the line
                            midpoint = row[3].positionAlongLine(0.5, True).firstPoint
                            row[0] = int(midpoint.X) if midpoint.X else 0  # Easting
                            row[1] = int(midpoint.Y) if midpoint.Y else 0  # Northing
                            row[2] = row[3].getLength('GEODESIC', 'KILOMETERS')  # Length 
                        else:
                            row[0] = row[1] = row[2] = 0
                        cursor.updateRow(row)
            else:
                self.logger.warning(f"Unsupported geometry type: {geometry_type}")
                return
                
            # self.logger.info(f"Added geometry fields for {geometry_type} feature class: {feature_class}")
            
        except Exception as e:
            self.logger.warning(f"Could not add geometry fields: {e}")

    def _get_field_index(self, field_list: List[str], field_name: str) -> Optional[int]:
        """Get the index of a field in the field list"""
        try:
            return field_list.index(field_name)
        except ValueError:
            return None
    
    def _is_dataset_enabled_for_mode(self, config: Dict) -> bool:
        """Check if a dataset is enabled for the current mode"""

        # If no enabled_modes specified, assume enabled for all modes
        if not config.modes:
            return True
        
        # Check if current mode is in the enabled modes list
        return self.settings.mode in config.modes

    def _get_buffer_list(self, config:Dict) -> list:
        """Determine buffer distance or distances for given mode and dataset"""
        
        # If buffer is a string, return as-is regardless of mode
        if isinstance(config.buffer, str):
            return [f'buffer_{config.buffer}']
        
        # If buffer is a dict, get mode-specific value or values
        if isinstance(config.buffer, dict):
            return ['buffer_' + value for value in config.buffer[self.settings.mode]]
        
    def _is_point_dataset(self, dataset_path: str) -> bool:
        """Check if a dataset has point geometry"""
        try:
            desc = arcpy.Describe(dataset_path)
            return desc.shapeType == 'Point'
        except:
            return False
        
    def _is_polygon_dataset(self, dataset_path: str) -> bool:
        """Check if a dataset has polygon geometry"""
        try:
            desc = arcpy.Describe(dataset_path)
            return desc.shapeType == 'Polygon'
        except:
            return False
    
    def _is_line_dataset(self, dataset_path: str) -> bool:
        """Check if a dataset has polygon geometry"""
        try:
            desc = arcpy.Describe(dataset_path)
            return desc.shapeType == 'Polyline'
        except:
            return False
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger(__name__)
    
    def _cleanup_temp_data(self):
        """Clean up all temporary datasets"""
        self.logger.info("Cleaning up temporary datasets...")
        print("Dataset deletion disabled for debugging - fix this later")
        for dataset in self.temp_datasets:
            try:
                if arcpy.Exists(dataset):
                    # arcpy.management.Delete(dataset)          # !! NOTE: Temporarily disabled for faster debugging (don't build buffers every time)
                    a = 1
            except Exception as e:
                self.logger.warning(f"Could not delete {dataset}: {e}")


# ============================================================================
# Configuration Section - Modify these settings as needed
# ============================================================================

# USER CONFIGURATION
INPUT_DATA = r"C:\data\gippsdap\Tambo_2324_DAP_sample.shp"
ID_FIELD = "DAP_REF_NO"
NAME_FIELD = "DAP_NAME"
DESCRIPTION_FIELD = "DESCRIPTIO"
DISTRICT_FIELD = "DISTRICT"
RISK_LEVEL_FIELD = "RISK_LVL"
WORKSPACE = r"C:\data\temp"
MODE = "JFMP"                                       # Options: "DAP", "JFMP", "NBFT"
THEMES = ["forests", "biodiversity", "water", "heritage", "summary"]     # Options: "summary", "forests", "biodiversity", "water", "heritage"
DISTRICT = None                                     # Optional: specify district name or leave as None
VERBOSE_LOGGING = True                              # Set to True for detailed logging

# Paths to risk register data - maintained by NEP(?)
RISK_REGISTERS = {
    'dap': WORKSPACE + r"\RiskRegister.gdb\NBFTDAP_RiskRegister",  # use this for DAP or NBFT, full risk register with all EVCs
    'lrli': WORKSPACE + r"\RiskRegister.gdb\LRLI_RiskRegister",    # filtered out values that won't be threatened under LRLI (additional EVCs removed)
    'jfmp': WORKSPACE + r"\RiskRegister.gdb\JFMP_RiskRegister"     # for FOP/JFMP only - combined advice for both EC and AGG BRL
}

# Data source paths
DATA_PATHS = {
    'csdl': "C:\\Data\\CSDL",
    'csdl_restricted': "C:\\Data\\CSDL FloraFauna2", 
    'csdl_culture': "C:\\Data\\CSDL Culture",
    'regional': "C:\\Data\\CSDL"
}

# Buffer distances
BUFFERS = {
    '1m':    {'input_features': "input_layer", 'buffer_distance': "1 meter", 'buffer_type': "FULL"},
    '10m':   {'input_features': "input_layer", 'buffer_distance': "10 meters", 'buffer_type': "FULL"},
    '50m':   {'input_features': "input_layer", 'buffer_distance': "50 meters", 'buffer_type': "FULL"},
    '100m':  {'input_features': "input_layer", 'buffer_distance': "100 meters", 'buffer_type': "FULL"},
    '250m':  {'input_features': "input_layer", 'buffer_distance': "250 meters", 'buffer_type': "FULL"},
    '300m':  {'input_features': "input_layer", 'buffer_distance': "300 meters", 'buffer_type': "FULL"},
    '500m':  {'input_features': "input_layer", 'buffer_distance': "500 meters", 'buffer_type': "FULL"},
    '550m':  {'input_features': "input_layer", 'buffer_distance': "550 meters", 'buffer_type': "FULL"},
    '1000m_ring': {'input_features': "buffer_500m", 'buffer_distance': "500 meters", 'buffer_type': "OUTSIDE_ONLY"},
}

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """
    Main entry point for the Values Checking Tool
    
    1. Creates settings from the configuration above
    2. Initializes the ValuesChecker with those settings
    3. Runs the processing workflow
    4. Reports results to the user
    """
    
    # Create settings from configuration
    settings = Settings(
        input_data=INPUT_DATA,
        workspace=Path(WORKSPACE),
        mode=MODE,
        themes=THEMES,
        district=DISTRICT
    )
    
    # Configure logging level
    if VERBOSE_LOGGING:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Display startup information
    print(f"Starting Values Checking Tool")
    print(f"Input: {INPUT_DATA}")
    print(f"Workspace: {WORKSPACE}")
    print(f"Mode: {MODE}")
    print(f"Themes: {', '.join(THEMES)}")
    if DISTRICT:
        print(f"District: {DISTRICT}")
    print("=" * 60)
    
    # Run the processing workflow
    checker = ValuesChecker(settings)
    result = checker.process()
    
    # Display results
    print("=" * 60)
    if result['success']:
        print(f"Processing completed successfully!")
        print(f"Outputs created: {len(result['outputs'])}")
        for output in result['outputs']:
            print(f"  {Path(output).name}")
        print(f"All outputs saved to: {WORKSPACE}")
    else:
        print(f"Processing failed!")
        print(f"Error: {result['error']}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
        
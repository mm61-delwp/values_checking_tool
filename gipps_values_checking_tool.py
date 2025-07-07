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
from typing import Dict, List, Optional
from dataclasses import dataclass

from dataset_matrix import DATASET_MATRIX
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


@dataclass # !! NOTE: should be updated (or maybe deleted?)
class DatasetConfig:
    """Configuration for a single dataset"""
    path: str
    buffer: str 
    where_clause: Optional[str]
    fields: List[str]
    value_type: str
    value_field: str
    description_field: Optional[str] = None
    id_field: Optional[str] = None


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
            self.logger.warning("File class deletion disabled for debugging - fix this later")
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
        self.logger.info(f"{self.settings.input_data} cleaned and copied")
        
        return working_copy
    
    # def _create_all_buffers(self, input_data: str) -> Dict[str, str]:
    #     """Create all required buffer distances for analysis"""
    #     buffers = {}
    #     buffer_names = []
        
    #     for buffer_name, distance in BUFFERS.items():
    #         buffer_layer = f"buffer_{buffer_name}"
    #         buffer_path = os.path.join(arcpy.env.workspace, buffer_layer)
    #         if not arcpy.Exists(buffer_path):
    #             arcpy.analysis.Buffer(input_data, buffer_layer, distance, "FULL", "ROUND", "NONE")
    #         buffers[buffer_name] = buffer_layer
    #         self.temp_datasets.append(buffer_layer)
    #         self.logger.debug(f"Created {buffer_name} buffer")
    #         buffer_names.append(buffer_name)
        
    #     self.logger.info(f"Buffers created at {', '.join(buffer_names)}")
    #     return buffers
    
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
        
        # Skip certain themes for LRLI mode
        if self.settings.mode == 'LRLI' and theme in ['biodiversity', 'heritage', 'summary']:
            self.logger.info(f"Skipping {theme} theme for LRLI mode")
            return []
        
        # Get dataset configurations for this theme
        if theme not in DATASET_MATRIX:
            self.logger.warning(f"No datasets configured for theme: {theme}")
            return []
        
        theme_datasets = DATASET_MATRIX[theme]
        
        # Process each dataset in the theme
        all_theme_results = []
        # for dataset_name, config in theme_datasets.items():
        #     try:
        #         if self._is_dataset_enabled_for_mode(config):
        #             dataset_results = self._process_single_dataset(dataset_name, config, buffered_layers, theme)
        #             all_theme_results.extend(dataset_results)
        #             self.logger.info(f"Processed {dataset_name}: {len(dataset_results)} values found")
        #         else:
        #             self.logger.info(f"Skipped {dataset_name} as it is disabled in {mode} mode")
        #     except Exception as e:
        #         self.logger.warning(f"Failed to process {dataset_name}: {e}")
        
        for dataset_name, config in theme_datasets.items():
            try:
                if self._is_dataset_enabled_for_mode(config):
                    for buffer in self._get_buffer_distance(config):
                        dataset_results = self._process_single_dataset(dataset_name, config, buffer, buffered_layers, theme)
                        all_theme_results.extend(dataset_results)
                        self.logger.info(f"Processed {dataset_name} with {buffer} buffer: {len(dataset_results)} values found")
                else:
                    self.logger.info(f"Skipped {dataset_name} as it is disabled in {mode} mode")
            except Exception as e:
                self.logger.warning(f"Failed to process {dataset_name}: {e}")

        return all_theme_results
    
    def _process_single_dataset(self, dataset_name: str, config: DatasetConfig, 
                               buffer_distance: str, buffered_layers: Dict[str, str], theme: str) -> List[Dict]:
        """Process a single dataset using its configuration"""
        
        # Step 1: Resolve dataset path and check existence
        dataset_path = config['path'].format(**DATA_PATHS)

        if not arcpy.Exists(dataset_path):
            self.logger.warning(f"Dataset not found: {dataset_path}")
            return []
        
        # Step 2: Apply selection criteria if specified
        selection_criteria = config['where_clause']
        if selection_criteria != None:
            source_dataset = self._apply_selection_criteria(dataset_name, dataset_path, selection_criteria)
        else:
            source_dataset = dataset_path
        
        # Step 3: Perform spatial intersection
        #intersect_result = self._perform_spatial_intersection(dataset_name, source_dataset, buffered_layers[config['buffer']])
        # buffer_distance = self._get_buffer_distance(config)
        intersect_result = self._perform_spatial_intersection(dataset_name, source_dataset, buffer_distance)

        # Step 4: Extract and return results
        if intersect_result:
            return self._extract_results_from_intersection(dataset_name, intersect_result, config, theme, buffer_distance)
        else:
            return []
    
    def _apply_selection_criteria(self, dataset_name: str, dataset_path: str, where_clause: Optional[str]) -> str:
        """Apply selection criteria to dataset if specified"""
        if where_clause: 
            selected_dataset = f"selected_{dataset_name}"
            arcpy.conversion.FeatureClassToFeatureClass(
                dataset_path, arcpy.env.workspace, selected_dataset, where_clause
            )
            self.temp_datasets.append(selected_dataset)
            return selected_dataset
        else:
            return dataset_path
    
    def _perform_spatial_intersection(self, dataset_name: str, source_dataset: str, buffer_layer: str) -> Optional[str]:
        """Perform spatial intersection between datasets"""
        intersect_result = f"intersect_{dataset_name}_{buffer_layer}"
        
        try:
            # Try intersect first (preserves all attributes)
            arcpy.analysis.Intersect([buffer_layer, source_dataset], intersect_result, "ALL")
            self.temp_datasets.append(intersect_result)
            return intersect_result
            
        except Exception as e:
            self.logger.warning(f"Intersect failed for {dataset_name}, trying clip: {e}")
            
            # Fallback to clip
            try:
                arcpy.analysis.Clip(source_dataset, buffer_layer, intersect_result)
                self.temp_datasets.append(intersect_result)
                return intersect_result
            except Exception as e2:
                self.logger.error(f"Both intersect and clip failed for {dataset_name}: {e2}")
                return None
    
    def _extract_results_from_intersection(self, dataset_name: str, intersect_result: str, config: DatasetConfig, theme: str, buffer_layer: str) -> List[Dict]:
        """Extract structured results from intersection output"""
        
        # List of intersection fields for validation
        available_fields = [f.name for f in arcpy.ListFields(intersect_result)]
        
        # List of fields we want to keep
        valid_fields = [ID_FIELD, NAME_FIELD, DISTRICT_FIELD]                           # add standard fields
        valid_fields.extend([f for f in config['fields'] if f in available_fields])     # add values configuration fields that exist in intersection
        
        if len(valid_fields) < 3:  # Need at least DAP_REF_NO, DAP_NAME, DISTRICT
            self.logger.warning(f"Insufficient fields available for {intersect_result}")
            return []
        
        # Dissolve features to deal with e.g. multiple intersections with same SMZ
        dissolve_result = f"dissolve_{dataset_name}"
        arcpy.analysis.PairwiseDissolve(intersect_result, dissolve_result, dissolve_field=valid_fields, multi_part="MULTI_PART")
        self.temp_datasets.append(dissolve_result)

        # Extract data using cursor
        results = []
        with arcpy.da.SearchCursor(dissolve_result, valid_fields) as cursor:
            for row in cursor:
                if not row[0]:  # Skip if no ID_FIELD
                    continue
                
                # Build base result structure
                result = self._build_base_result(row, valid_fields, config, theme, buffer_layer)
                
                # Add theme-specific fields - additional detail for biodiversity & heritage themes
                self._add_theme_specific_fields(result, row, valid_fields, theme)
                
                # add to output
                results.append(result)

        return results
    
    def _build_base_result(self, row: tuple, valid_fields: List[str], config: DatasetConfig, theme: str, buffer_layer: str) -> Dict:
        """Build the base result structure common to all themes"""
        result = {
            'ID': row[0],
            'NAME': row[1] if len(row) > 1 else '',
            'DISTRICT': row[2] if len(row) > 2 else '',
            'Theme': theme,
            'Value_Type': config['value_type'],
            'Buffer': buffer_layer
        }
        
        # Add value field
        value_field_idx = self._get_field_index(valid_fields, config['value_field'])
        if value_field_idx is not None and value_field_idx < len(row) and row[value_field_idx]:
            result['Value'] = row[value_field_idx]
        
        # Add description field if specified
        if config['description_field']:
            desc_field_idx = self._get_field_index(valid_fields, config['description_field'])
            if desc_field_idx is not None and desc_field_idx < len(row) and row[desc_field_idx]:
                result['Value_Description'] = row[desc_field_idx]
        
        # Add ID field if specified
        if config['id_field']:
            id_field_idx = self._get_field_index(valid_fields, config['id_field'])
            if id_field_idx is not None and id_field_idx < len(row) and row[id_field_idx]:
                result['Value_ID'] = row[id_field_idx]
        
        return result
    
    def _add_theme_specific_fields(self, result: Dict, row: tuple, valid_fields: List[str], theme: str):
        """Add theme-specific fields to the result"""
        if theme == 'biodiversity':
            bio_fields = ['SCI_NAME', 'COMM_NAME', 'TAXON_ID', 'EXTRA_INFO', 'RECORD_ID']
            for bio_field in bio_fields:
                field_idx = self._get_field_index(valid_fields, bio_field)
                if field_idx is not None and field_idx < len(row):
                    result[bio_field] = row[field_idx]
        
        elif theme == 'heritage':
            heritage_fields = ['COMPONENT_NO', 'PLACE_NAME', 'COMPONENT_TYPE', 'DATE_MODIFIED', 'FIRE_SENSITIVITY']
            for heritage_field in heritage_fields:
                field_idx = self._get_field_index(valid_fields, heritage_field)
                if field_idx is not None and field_idx < len(row):
                    if heritage_field == 'COMPONENT_NO':
                        result['ACHRIS_ID'] = row[field_idx]
                    else:
                        result[heritage_field] = row[field_idx]
    
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
        fields = ["DAP_REF_NO", "DAP_NAME", "DESCRIPTION", "RISK_LVL", "DISTRICT", "AREA_HA", "Easting", "Northing"]
        
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
    
    def _setup_arcpy_environment(self):
        """Configure ArcPy environment settings"""
        arcpy.env.overwriteOutput = True
        arcpy.env.scriptWorkspace = str(self.settings.workspace)
        arcpy.env.parallelProcessingFactor = "75%"
        arcpy.SetLogHistory(False)
        
        # Set spatial reference to VICGRID2020
        sr = arcpy.SpatialReference(7899)
        arcpy.env.outputCoordinateSystem = sr
    
    def _add_geometry_fields(self, feature_class: str):
        """Add and calculate geometry fields for the feature class"""
        try:
            # Add fields
            arcpy.management.AddField(feature_class, "Easting", "DOUBLE")
            arcpy.management.AddField(feature_class, "Northing", "DOUBLE")
            arcpy.management.AddField(feature_class, "AREA_HA", "DOUBLE")
            
            # Calculate geometry
            with arcpy.da.UpdateCursor(feature_class, ["Easting", "SHAPE@X", "Northing", "SHAPE@Y", "AREA_HA", "SHAPE@"]) as cursor:
                for row in cursor:
                    row[0] = int(row[1]) if row[1] else 0  # Easting
                    row[2] = int(row[3]) if row[3] else 0  # Northing
                    row[4] = row[5].getArea('GEODESIC', 'HECTARES') if row[5] else 0  # Area in hectares
                    cursor.updateRow(row)
                    
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
        enabled_modes = config.get('modes', [])
        
        # If no enabled_modes specified, assume enabled for all modes
        if not enabled_modes:
            return True
        
        # Check if current mode is in the enabled modes list
        return self.settings.mode in enabled_modes

    def _get_buffer_distance(self, config:Dict) -> list:
        """Determine buffer distance for given mode and dataset or multiple distances if supplied"""
        buffer_config = config['buffer']
        
        # If buffer is a string, return as-is regardless of mmode
        if isinstance(buffer_config, str):
            return [f'buffer_{buffer_config}']
        
        # If buffer is a dict, get mode-specific value or values
        if isinstance(buffer_config, dict):
            return ['buffer_' + value for value in buffer_config.get(self.settings.mode, '1m')]
        
        # Fallback
        return ['buffer_1m']

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
        for dataset in self.temp_datasets:
            try:
                if arcpy.Exists(dataset):
                    # arcpy.management.Delete(dataset)          # !! NOTE: Temporarily disabled for faster debugging (don't build buffers every time)
                    print("Dataset deletion disabled for debugging - fix this later")
            except Exception as e:
                self.logger.warning(f"Could not delete {dataset}: {e}")


# ============================================================================
# Configuration Section - Modify these settings as needed
# ============================================================================

# USER CONFIGURATION
INPUT_DATA = r"C:\data\gippsdap\Tambo_2324_DAP.shp"
ID_FIELD = "DAP_REF_NO"
NAME_FIELD = "DAP_NAME"
DISTRICT_FIELD = "DISTRICT"
WORKSPACE = r"C:\data\temp"
MODE = "JFMP"                                       # Options: "DAP", "JFMP", "NBFT", "LRLI"
THEMES = ["forests", "biodiversity", "summary"]     # Options: "summary", "forests", "biodiversity", "water", "heritage"
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
    # '1000m': {'input_features': "input_layer", 'buffer_distance': "1000 meters", 'buffer_type': "FULL"},
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
        
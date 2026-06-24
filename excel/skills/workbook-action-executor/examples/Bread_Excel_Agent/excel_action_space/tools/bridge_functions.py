"""
Bridge functions to connect pandas and openpyxl workflows
Handles state transfer between the two executors
"""

import pandas as pd
import openpyxl
import tempfile
import os
from typing import Dict, Any

class PandasOpenpyxlBridge:
    """
    Bridges pandas and openpyxl executors for seamless workflows
    """

    def __init__(self, pandas_executor, openpyxl_executor):
        self.pandas_exec = pandas_executor
        self.openpyxl_exec = openpyxl_executor
        self.temp_files = []  # Track temp files for cleanup

    def pandas_to_openpyxl(self, dataframe_id: str = None, preserve_formatting: bool = False) -> Dict[str, Any]:
        """
        Transfer DataFrame from pandas to openpyxl for formatting

        Common workflow:
        1. pandas analyzes/transforms data
        2. This bridge saves to temp file
        3. openpyxl loads for formatting
        """
        try:
            # Get DataFrame from pandas executor
            df = self.pandas_exec._get_dataframe(dataframe_id)

            # Use a persistent workspace file to avoid repeated permission prompts
            temp_filename = 'excel_bridge_workspace.xlsx'
            temp_path = os.path.abspath(temp_filename)
            # Don't add to temp_files since we're reusing it

            # Save DataFrame to temp file
            df.to_excel(temp_path, index=False)

            # Load into openpyxl
            self.openpyxl_exec.workbook = openpyxl.load_workbook(temp_path)
            self.openpyxl_exec.active_sheet = self.openpyxl_exec.workbook.active

            return {
                'status': 'success',
                'message': f'Transferred DataFrame to openpyxl workbook',
                'temp_file': temp_path,
                'shape': df.shape
            }

        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def openpyxl_to_pandas(self, sheet_name: str = None) -> Dict[str, Any]:
        """
        Transfer openpyxl workbook to pandas DataFrame

        Common workflow:
        1. openpyxl formats/modifies Excel
        2. SAVE FIRST (required by this method)
        3. This bridge uses Excel to calculate formulas
        4. pandas loads for analysis with calculated values
        """
        try:
            # Check if workbook is open
            if self.openpyxl_exec.workbook is None:
                return {
                    'status': 'error',
                    'error': 'No openpyxl workbook loaded. Use openpyxl_load_workbook first, then retry bridge_openpyxl_to_pandas.'
                }

            # ✅ NEW CHECK 1: Detect unsaved changes
            if getattr(self.openpyxl_exec, 'modified', False):
                return {
                    'status': 'error',
                    'error': (
                        'CRITICAL: Workbook has UNSAVED changes. '
                        'You MUST call openpyxl_workbook_save before using bridge_openpyxl_to_pandas. '
                        'Why: This bridge uses Excel to calculate formulas, which breaks the file handle. '
                        'If you don\'t save first, your changes will be LOST. '
                        f'Current file: {getattr(self.openpyxl_exec, "current_filename", "unsaved")}. '
                        'Workflow: 1) openpyxl_workbook_save, 2) bridge_openpyxl_to_pandas, 3) continue.'
                    )
                }

            # ✅ NEW CHECK 2: Verify filename exists
            if not hasattr(self.openpyxl_exec, 'current_filename') or not self.openpyxl_exec.current_filename:
                return {
                    'status': 'error',
                    'error': (
                        'Cannot use bridge - workbook filename is unknown. '
                        'This usually means the workbook was created with openpyxl_workbook (new file) '
                        'but never saved. Call openpyxl_workbook_save first to establish a filename.'
                    )
                }

            # Use a persistent workspace file to avoid repeated permission prompts
            temp_filename = 'excel_bridge_workspace.xlsx'
            temp_path = os.path.abspath(temp_filename)

            # ✅ SIMPLIFIED: Copy the already-saved file (we validated it's saved above)
            import shutil
            shutil.copy(self.openpyxl_exec.current_filename, temp_path)

            # Use xlwings to open Excel and calculate formulas
            try:
                import xlwings as xw

                # Open with Excel in silent mode to reduce permission prompts
                app = xw.App(visible=False, add_book=False)
                app.display_alerts = False  # Suppress Excel alerts
                app.screen_updating = False  # Prevent screen updates

                try:
                    wb_excel = xw.Book(temp_path)

                    # Force Excel to calculate all formulas
                    wb_excel.app.calculate()

                    # Save the file with calculated values cached
                    wb_excel.save()
                    wb_excel.close()
                finally:
                    # Ensure Excel app is closed
                    app.quit()

            except Exception as e:
                # If xlwings fails (no Excel installed), continue without calculation
                # Formulas will remain but pandas might read NaN
                pass

            # Read into pandas - will now have calculated values if xlwings succeeded
            if sheet_name:
                df = pd.read_excel(temp_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(temp_path)

            # Store in pandas executor
            df_id = self.pandas_exec._store_dataframe(df)

            # CRITICAL: After xlwings opens the file, openpyxl's file handle is broken
            # We need to reload the workbook to fix the handle
            if self.openpyxl_exec.current_filename:
                try:
                    # Reload the workbook to get a fresh file handle
                    self.openpyxl_exec.workbook = openpyxl.load_workbook(
                        self.openpyxl_exec.current_filename,
                        read_only=False,
                        data_only=False
                    )
                    self.openpyxl_exec.active_sheet = self.openpyxl_exec.workbook.active
                    # ✅ Reset modified flag since we reloaded from saved file
                    self.openpyxl_exec.modified = False
                except Exception as reload_error:
                    # If reload fails, warn but don't fail the bridge operation
                    return {
                        'status': 'success',
                        'message': f'Transferred workbook to pandas DataFrame {df_id}. WARNING: Could not reload openpyxl workbook - file handle may be broken. Close and reload before saving.',
                        'dataframe_id': df_id,
                        'shape': df.shape,
                        'warning': f'Workbook reload failed: {str(reload_error)}'
                    }

            return {
                'status': 'success',
                'message': f'Transferred workbook to pandas DataFrame {df_id}. Workbook reloaded from disk with fresh handle.',
                'dataframe_id': df_id,
                'shape': df.shape
            }

        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def sync_file(self, filepath: str, direction: str = 'pandas_to_openpyxl') -> Dict[str, Any]:
        """
        Synchronize changes through a file

        Args:
            filepath: Path to Excel file
            direction: 'pandas_to_openpyxl' or 'openpyxl_to_pandas'
        """
        try:
            if direction == 'pandas_to_openpyxl':
                # Ensure pandas changes are saved
                df = self.pandas_exec._get_dataframe()
                df.to_excel(filepath, index=False)

                # Reload in openpyxl
                self.openpyxl_exec.workbook = openpyxl.load_workbook(filepath)
                self.openpyxl_exec.active_sheet = self.openpyxl_exec.workbook.active

                return {
                    'status': 'success',
                    'message': f'Synced pandas changes to openpyxl via {filepath}'
                }

            elif direction == 'openpyxl_to_pandas':
                # Save openpyxl changes
                if self.openpyxl_exec.workbook:
                    self.openpyxl_exec.workbook.save(filepath)

                # Reload in pandas
                df = pd.read_excel(filepath)
                df_id = self.pandas_exec._store_dataframe(df)

                return {
                    'status': 'success',
                    'message': f'Synced openpyxl changes to pandas DataFrame {df_id}'
                }

            else:
                raise ValueError(f"Invalid direction: {direction}")

        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def cleanup(self):
        """Clean up workspace file if needed"""
        # Clean up the persistent workspace file if it exists
        workspace_file = os.path.abspath('excel_bridge_workspace.xlsx')
        if os.path.exists(workspace_file):
            try:
                os.remove(workspace_file)
            except:
                pass

        # Clean up any old temp files that might still exist
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except:
                pass
        self.temp_files = []


# Bridge tools for LiteLLM
BRIDGE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bridge_pandas_to_openpyxl",
            "description": "[BRIDGE] Transfer DataFrame from pandas to openpyxl for formatting. USE AFTER: pandas analysis/transformation. USE BEFORE: openpyxl formatting operations. Automatically handles file transfer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dataframe_id": {
                        "type": ["string", "null"],
                        "description": "DataFrame ID to transfer (uses last if not specified)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bridge_openpyxl_to_pandas",
            "description": "[BRIDGE] Transfer formatted workbook from openpyxl to pandas for analysis. USE AFTER: openpyxl formatting. USE BEFORE: pandas analysis. Creates new DataFrame from workbook.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sheet_name": {
                        "type": ["string", "null"],
                        "description": "Sheet to read (uses active if not specified)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bridge_sync_file",
            "description": "[BRIDGE] Synchronize changes between pandas and openpyxl through a file. USE WHEN: both libraries need to work on the same file sequentially.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to Excel file for synchronization"
                    },
                    "direction": {
                        "type": "string",
                        "description": "Direction: 'pandas_to_openpyxl' or 'openpyxl_to_pandas'",
                        "enum": ["pandas_to_openpyxl", "openpyxl_to_pandas"]
                    }
                },
                "required": ["filepath", "direction"]
            }
        }
    }
]
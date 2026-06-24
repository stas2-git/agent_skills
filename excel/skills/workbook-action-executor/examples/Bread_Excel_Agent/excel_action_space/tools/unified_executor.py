"""
Unified Excel Executor for LLM Integration
Combines openpyxl, pandas, and bridge functionality for comprehensive Excel automation
"""

import json
from typing import Any, Dict, Optional

from .openpyxl_executor import OpenpyxlToolExecutor
from .pandas_executor import PandasToolExecutor
from .pdf_executor import PdfToolExecutor
from .bridge_functions import PandasOpenpyxlBridge


class UnifiedExcelExecutor:
    """
    Unified executor that manages both openpyxl and pandas operations
    with seamless bridging between them
    """

    def __init__(self):
        """Initialize all executors and bridge"""
        self.openpyxl_exec = OpenpyxlToolExecutor()
        self.pandas_exec = PandasToolExecutor()
        self.pdf_exec = PdfToolExecutor()
        self.bridge = PandasOpenpyxlBridge(self.pandas_exec, self.openpyxl_exec)

    def execute_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute any tool based on its prefix

        Args:
            tool_name: Name of the tool (with prefix like openpyxl_, pandas_, bridge_, system_)
            params: Parameters for the tool

        Returns:
            Dict with status and result/error
        """
        if params is None:
            params = {}

        try:
            # Route to appropriate executor based on prefix
            if tool_name.startswith('openpyxl_'):
                return self.openpyxl_exec.execute_tool(tool_name, params)

            elif tool_name.startswith('pandas_'):
                return self.pandas_exec.execute_tool(tool_name, params)

            elif tool_name.startswith('pdf_'):
                return self._execute_pdf_tool(tool_name, params)

            elif tool_name.startswith('bridge_'):
                return self._execute_bridge_tool(tool_name, params)

            elif tool_name.startswith('system_'):
                return self._execute_system_tool(tool_name, params)

            else:
                # Try without prefix for backward compatibility
                # First try openpyxl
                try:
                    return self.openpyxl_exec.execute_tool(tool_name, params)
                except:
                    # Then try pandas
                    try:
                        return self.pandas_exec.execute_tool(tool_name, params)
                    except:
                        return {
                            'status': 'error',
                            'error': f"Unknown tool: {tool_name}. Tools should have prefix: openpyxl_, pandas_, bridge_, or system_"
                        }

        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def _execute_pdf_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute PDF tools with special handling for to_dataframe"""
        
        # Special handling for pdf_to_dataframe - needs pandas executor reference
        if tool_name == 'pdf_to_dataframe':
            # Inject pandas_executor into params so PDF executor can store DataFrames
            params['pandas_executor'] = self.pandas_exec
            return self.pdf_exec.execute_tool(tool_name, params)
        
        # All other PDF tools
        return self.pdf_exec.execute_tool(tool_name, params)

    def _execute_bridge_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute bridge tools for pandas-openpyxl interop"""

        if tool_name == 'bridge_pandas_to_openpyxl':
            return self.bridge.pandas_to_openpyxl(params.get('dataframe_id'))

        elif tool_name == 'bridge_openpyxl_to_pandas':
            return self.bridge.openpyxl_to_pandas(params.get('sheet_name'))

        elif tool_name == 'bridge_sync_file':
            filepath = params.get('filepath')
            direction = params.get('direction', 'pandas_to_openpyxl')
            if not filepath:
                return {'status': 'error', 'error': 'filepath parameter is required'}
            return self.bridge.sync_file(filepath, direction)

        else:
            return {'status': 'error', 'error': f"Unknown bridge tool: {tool_name}"}

    def _execute_system_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system management tools"""

        if tool_name == 'system_get_state':
            return self._get_full_state()

        elif tool_name == 'system_reset':
            if not params.get('confirm', False):
                return {
                    'status': 'error',
                    'error': 'Reset requires confirm=true parameter to prevent accidental data loss'
                }
            return self._reset_all()

        elif tool_name == 'system_close_files':
            return self._close_all_files()

        else:
            return {'status': 'error', 'error': f"Unknown system tool: {tool_name}"}

    def _get_full_state(self) -> Dict[str, Any]:
        """Get complete state information from all executors"""
        try:
            openpyxl_state = self.openpyxl_exec.get_state()
            pandas_state = self.pandas_exec.get_state()
            pdf_state = self.pdf_exec.get_state()

            return {
                'status': 'success',
                'result': {
                    'openpyxl': {
                        'workbook_open': self.openpyxl_exec.workbook is not None,
                        'workbook_loaded_from': getattr(self.openpyxl_exec, 'current_filename', None),
                        'has_unsaved_changes': getattr(self.openpyxl_exec, 'modified', False),
                        'active_sheet': openpyxl_state.get('active_sheet'),
                        'sheets': openpyxl_state.get('sheets', []),
                        'created_objects': openpyxl_state.get('created_objects', {})
                    },
                    'pandas': {
                        'dataframes': pandas_state.get('dataframes', []),
                        'excel_writers': pandas_state.get('excel_writers', []),
                        'last_df_id': pandas_state.get('last_df_id'),
                        'total_dataframes': pandas_state.get('total_dataframes', 0)
                    },
                    'pdf': {
                        'loaded_pdfs': pdf_state.get('loaded_pdfs', []),
                        'last_pdf_id': pdf_state.get('last_pdf_id'),
                        'total_pdfs': pdf_state.get('total_pdfs', 0)
                    },
                    'bridge': {
                        'temp_files': len(self.bridge.temp_files)
                    }
                }
            }
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to get state: {str(e)}"}

    def _reset_all(self) -> Dict[str, Any]:
        """Reset all executors and clear state"""
        try:
            # Clear pandas state
            self.pandas_exec.clear_state()

            # Clear PDF state
            self.pdf_exec.clear_state()

            # Reset openpyxl - create new instance
            self.openpyxl_exec = OpenpyxlToolExecutor()

            # Clean up bridge temp files
            self.bridge.cleanup()

            # Create new bridge instance
            self.bridge = PandasOpenpyxlBridge(self.pandas_exec, self.openpyxl_exec)

            return {
                'status': 'success',
                'result': 'All state reset successfully. Ready for new task.'
            }
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to reset: {str(e)}"}

    def _close_all_files(self) -> Dict[str, Any]:
        """Close all open file handles to prevent conflicts"""
        try:
            closed_items = []

            # Close pandas ExcelWriters
            if hasattr(self.pandas_exec, 'excel_writers'):
                for writer_id, writer in self.pandas_exec.excel_writers.items():
                    try:
                        writer.close()
                        closed_items.append(f"ExcelWriter: {writer_id}")
                    except:
                        pass
                self.pandas_exec.excel_writers.clear()

            # Close PDFs
            if hasattr(self.pdf_exec, 'loaded_pdfs'):
                pdf_count = len(self.pdf_exec.loaded_pdfs)
                for pdf_id, pdf in list(self.pdf_exec.loaded_pdfs.items()):
                    try:
                        pdf.close()
                    except:
                        pass
                self.pdf_exec.loaded_pdfs.clear()
                self.pdf_exec.pdf_metadata.clear()
                if pdf_count > 0:
                    closed_items.append(f"{pdf_count} PDF(s)")

            # Save and close openpyxl workbook if open
            if hasattr(self.openpyxl_exec, 'workbook') and self.openpyxl_exec.workbook:
                try:
                    # Don't save automatically - just close
                    self.openpyxl_exec.workbook.close()
                    closed_items.append("Openpyxl workbook")
                except:
                    pass

            # Clean up bridge temp files
            if hasattr(self.bridge, 'temp_files'):
                temp_count = len(self.bridge.temp_files)
                self.bridge.cleanup()
                if temp_count > 0:
                    closed_items.append(f"{temp_count} temporary files")

            return {
                'status': 'success',
                'result': f"Closed: {', '.join(closed_items) if closed_items else 'No files were open'}"
            }
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to close files: {str(e)}"}

    def get_state(self) -> Dict[str, Any]:
        """Get current state (for backward compatibility)"""
        result = self._get_full_state()
        if result['status'] == 'success':
            return result['result']
        return {}


# Convenience function for testing
def create_unified_executor():
    """Create and return a new unified executor instance"""
    return UnifiedExcelExecutor()
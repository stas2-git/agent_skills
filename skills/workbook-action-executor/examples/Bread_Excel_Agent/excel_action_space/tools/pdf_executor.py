"""
PDF Tool Executor for LLM Integration
Enables reading PDFs, extracting text and tables, and bridging to pandas/Excel
"""

import os
from typing import Any, Dict, Optional, List


class PdfToolExecutor:
    """
    Executor for PDF reading and extraction operations
    Integrates with pandas for seamless PDF → DataFrame → Excel workflows
    """

    def __init__(self):
        """Initialize PDF executor with state tracking"""
        self.loaded_pdfs = {}  # {pdf_id: pdf_object}
        self.pdf_metadata = {}  # {pdf_id: metadata_dict}
        self.pdf_counter = 0
        self.last_pdf_id = None
        
        # Import libraries lazily to avoid startup overhead
        self._pypdf = None
        self._pdfplumber = None

    def _import_pypdf(self):
        """Lazy import pypdf"""
        if self._pypdf is None:
            try:
                import pypdf
                self._pypdf = pypdf
            except ImportError:
                raise ImportError(
                    "pypdf is required for PDF operations. "
                    "Install with: pip install pypdf"
                )
        return self._pypdf

    def _import_pdfplumber(self):
        """Lazy import pdfplumber"""
        if self._pdfplumber is None:
            try:
                import pdfplumber
                self._pdfplumber = pdfplumber
            except ImportError:
                raise ImportError(
                    "pdfplumber is required for table extraction. "
                    "Install with: pip install pdfplumber"
                )
        return self._pdfplumber

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a PDF tool by name
        
        Args:
            tool_name: Name of the tool (with or without pdf_ prefix)
            params: Tool parameters
            
        Returns:
            Dict with status and result/error
        """
        # Remove prefix if present
        method_name = tool_name.replace('pdf_', '') if tool_name.startswith('pdf_') else tool_name
        method_name = f'_{method_name}'
        
        if hasattr(self, method_name):
            try:
                method = getattr(self, method_name)
                return method(**params)
            except TypeError as e:
                return {'status': 'error', 'error': f"Invalid parameters for {tool_name}: {str(e)}"}
            except Exception as e:
                return {'status': 'error', 'error': f"Tool execution failed: {str(e)}"}
        else:
            return {'status': 'error', 'error': f"Unknown PDF tool: {tool_name}"}

    def _load(self, filepath: str) -> Dict[str, Any]:
        """
        Load PDF into memory for reading
        
        Args:
            filepath: Path to PDF file
            
        Returns:
            Dict with pdf_id and metadata
        """
        try:
            # Validate file exists
            if not os.path.exists(filepath):
                return {'status': 'error', 'error': f"File not found: {filepath}"}
            
            if not filepath.lower().endswith('.pdf'):
                return {'status': 'error', 'error': f"File is not a PDF: {filepath}"}
            
            # Load with pdfplumber (better for table extraction)
            pdfplumber = self._import_pdfplumber()
            pdf = pdfplumber.open(filepath)
            
            # Generate unique ID
            self.pdf_counter += 1
            pdf_id = f"pdf_{self.pdf_counter}"
            
            # Store PDF object
            self.loaded_pdfs[pdf_id] = pdf
            self.last_pdf_id = pdf_id
            
            # Extract metadata
            page_count = len(pdf.pages)
            
            # Get text preview from first page
            first_page_preview = ""
            if page_count > 0:
                first_page_text = pdf.pages[0].extract_text() or ""
                first_page_preview = first_page_text[:200] + "..." if len(first_page_text) > 200 else first_page_text
            
            metadata = {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'page_count': page_count,
                'first_page_preview': first_page_preview
            }
            
            self.pdf_metadata[pdf_id] = metadata
            
            return {
                'status': 'success',
                'result': {
                    'pdf_id': pdf_id,
                    'page_count': page_count,
                    'filename': metadata['filename'],
                    'message': f"Successfully loaded PDF with {page_count} pages. Use pdf_id='{pdf_id}' for extraction operations.",
                    'first_page_preview': first_page_preview
                }
            }
            
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to load PDF: {str(e)}"}

    def _extract_text(
        self, 
        pdf_id: str, 
        page_number: Optional[int] = None,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Extract text from PDF pages
        
        Args:
            pdf_id: ID of loaded PDF
            page_number: Specific page to extract (1-based, overrides start/end)
            start_page: Starting page for range (1-based, inclusive)
            end_page: Ending page for range (1-based, inclusive)
            
        Returns:
            Dict with extracted text
        """
        try:
            # Validate PDF is loaded
            if pdf_id not in self.loaded_pdfs:
                return {'status': 'error', 'error': f"PDF '{pdf_id}' not loaded. Use pdf_load first."}
            
            pdf = self.loaded_pdfs[pdf_id]
            page_count = len(pdf.pages)
            
            # Determine pages to extract
            if page_number is not None:
                # Single page
                if page_number < 1 or page_number > page_count:
                    return {'status': 'error', 'error': f"Page {page_number} out of range (1-{page_count})"}
                pages_to_extract = [page_number - 1]  # Convert to 0-based
                
            elif start_page is not None or end_page is not None:
                # Page range
                start = (start_page or 1) - 1  # Convert to 0-based
                end = (end_page or page_count) - 1
                
                if start < 0 or end >= page_count or start > end:
                    return {'status': 'error', 'error': f"Invalid page range: {start_page}-{end_page}"}
                    
                pages_to_extract = range(start, end + 1)
                
            else:
                # All pages
                pages_to_extract = range(page_count)
            
            # Extract text from specified pages
            extracted_text = []
            for page_idx in pages_to_extract:
                page = pdf.pages[page_idx]
                text = page.extract_text() or ""
                extracted_text.append({
                    'page': page_idx + 1,  # Convert back to 1-based
                    'text': text
                })
            
            # Combine text if multiple pages
            if len(extracted_text) == 1:
                result_text = extracted_text[0]['text']
                page_info = f"page {extracted_text[0]['page']}"
            else:
                result_text = "\n\n".join([f"--- Page {item['page']} ---\n{item['text']}" for item in extracted_text])
                page_info = f"pages {extracted_text[0]['page']}-{extracted_text[-1]['page']}"
            
            return {
                'status': 'success',
                'result': {
                    'text': result_text,
                    'page_count': len(extracted_text),
                    'character_count': len(result_text),
                    'message': f"Extracted {len(result_text)} characters from {page_info}"
                }
            }
            
        except Exception as e:
            return {'status': 'error', 'error': f"Text extraction failed: {str(e)}"}

    def _to_dataframe(
        self,
        pdf_id: str,
        page_number: int,
        table_index: Optional[int] = None,
        pandas_executor = None
    ) -> Dict[str, Any]:
        """
        Extract table from PDF and convert to pandas DataFrame
        
        Args:
            pdf_id: ID of loaded PDF
            page_number: Page containing table (1-based)
            table_index: Which table on page (0-based, None = all tables)
            pandas_executor: PandasToolExecutor instance for DataFrame storage
            
        Returns:
            Dict with dataframe_id(s)
        """
        try:
            # Validate PDF is loaded
            if pdf_id not in self.loaded_pdfs:
                return {'status': 'error', 'error': f"PDF '{pdf_id}' not loaded. Use pdf_load first."}
            
            pdf = self.loaded_pdfs[pdf_id]
            page_count = len(pdf.pages)
            
            # Validate page number
            if page_number < 1 or page_number > page_count:
                return {'status': 'error', 'error': f"Page {page_number} out of range (1-{page_count})"}
            
            page = pdf.pages[page_number - 1]  # Convert to 0-based
            
            # Extract tables from page
            tables = page.extract_tables()
            
            if not tables:
                return {
                    'status': 'error',
                    'error': f"No tables found on page {page_number}. Try pdf_extract_text to see page content."
                }
            
            # Import pandas here (circular dependency avoidance)
            try:
                import pandas as pd
            except ImportError:
                return {'status': 'error', 'error': "pandas is required but not installed"}
            
            # Determine which tables to convert
            if table_index is not None:
                if table_index < 0 or table_index >= len(tables):
                    return {
                        'status': 'error',
                        'error': f"Table index {table_index} out of range (found {len(tables)} tables on page)"
                    }
                tables_to_convert = [(table_index, tables[table_index])]
            else:
                tables_to_convert = list(enumerate(tables))
            
            # Convert to DataFrame(s)
            created_dataframes = []
            
            for idx, table_data in tables_to_convert:
                # Convert table to DataFrame
                # First row as headers
                if len(table_data) > 1:
                    headers = table_data[0]
                    data = table_data[1:]
                    df = pd.DataFrame(data, columns=headers)
                else:
                    df = pd.DataFrame(table_data)
                
                # Store in pandas executor if provided
                if pandas_executor:
                    # Use pandas executor's storage mechanism
                    pandas_executor.dataframes[f"df_{pandas_executor.df_counter + 1}"] = df
                    pandas_executor.df_counter += 1
                    pandas_executor.last_df_id = f"df_{pandas_executor.df_counter}"
                    df_id = pandas_executor.last_df_id
                else:
                    df_id = f"df_from_pdf_{pdf_id}_p{page_number}_t{idx}"
                
                created_dataframes.append({
                    'dataframe_id': df_id,
                    'table_index': idx,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns)
                })
            
            if len(created_dataframes) == 1:
                result = created_dataframes[0]
                result['message'] = f"Created DataFrame '{result['dataframe_id']}' with {result['rows']} rows and {result['columns']} columns"
            else:
                result = {
                    'dataframes': created_dataframes,
                    'count': len(created_dataframes),
                    'message': f"Created {len(created_dataframes)} DataFrames from page {page_number}"
                }
            
            return {'status': 'success', 'result': result}
            
        except Exception as e:
            return {'status': 'error', 'error': f"Table extraction failed: {str(e)}"}

    def _get_metadata(self, pdf_id: str) -> Dict[str, Any]:
        """
        Get metadata about loaded PDF
        
        Args:
            pdf_id: ID of loaded PDF
            
        Returns:
            Dict with metadata
        """
        try:
            if pdf_id not in self.loaded_pdfs:
                return {'status': 'error', 'error': f"PDF '{pdf_id}' not loaded. Use pdf_load first."}
            
            metadata = self.pdf_metadata.get(pdf_id, {})
            pdf = self.loaded_pdfs[pdf_id]
            
            return {
                'status': 'success',
                'result': {
                    'pdf_id': pdf_id,
                    'filename': metadata.get('filename'),
                    'filepath': metadata.get('filepath'),
                    'page_count': len(pdf.pages),
                    'first_page_preview': metadata.get('first_page_preview', '')
                }
            }
            
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to get metadata: {str(e)}"}

    def _close(self, pdf_id: str) -> Dict[str, Any]:
        """
        Close and unload PDF from memory
        
        Args:
            pdf_id: ID of loaded PDF
            
        Returns:
            Status dict
        """
        try:
            if pdf_id not in self.loaded_pdfs:
                return {'status': 'error', 'error': f"PDF '{pdf_id}' not loaded"}
            
            pdf = self.loaded_pdfs[pdf_id]
            pdf.close()
            
            del self.loaded_pdfs[pdf_id]
            if pdf_id in self.pdf_metadata:
                del self.pdf_metadata[pdf_id]
            
            if self.last_pdf_id == pdf_id:
                self.last_pdf_id = None
            
            return {
                'status': 'success',
                'result': f"Closed PDF '{pdf_id}'"
            }
            
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to close PDF: {str(e)}"}

    def _list_pdfs(self) -> Dict[str, Any]:
        """
        List all loaded PDFs
        
        Returns:
            Dict with PDF list
        """
        try:
            pdf_list = []
            for pdf_id, pdf in self.loaded_pdfs.items():
                metadata = self.pdf_metadata.get(pdf_id, {})
                pdf_list.append({
                    'pdf_id': pdf_id,
                    'filename': metadata.get('filename'),
                    'page_count': len(pdf.pages)
                })
            
            return {
                'status': 'success',
                'result': {
                    'pdfs': pdf_list,
                    'count': len(pdf_list),
                    'last_pdf_id': self.last_pdf_id
                }
            }
            
        except Exception as e:
            return {'status': 'error', 'error': f"Failed to list PDFs: {str(e)}"}

    def get_state(self) -> Dict[str, Any]:
        """Get current state of PDF executor"""
        return {
            'loaded_pdfs': list(self.loaded_pdfs.keys()),
            'last_pdf_id': self.last_pdf_id,
            'total_pdfs': len(self.loaded_pdfs)
        }

    def clear_state(self):
        """Clear all loaded PDFs"""
        for pdf in self.loaded_pdfs.values():
            try:
                pdf.close()
            except:
                pass
        self.loaded_pdfs.clear()
        self.pdf_metadata.clear()
        self.last_pdf_id = None



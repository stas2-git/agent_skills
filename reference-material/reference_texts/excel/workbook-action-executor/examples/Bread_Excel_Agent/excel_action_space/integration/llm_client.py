"""
LiteLLM + Tool Executor Integration
Complete end-to-end system for LLM-driven Excel automation
"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from litellm import completion
from excel_action_space.tools.unified_executor import UnifiedExcelExecutor

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
CUSTOM_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
CUSTOM_API_KEY = os.getenv("OPENAI_API_KEY")
CUSTOM_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

# Validate required configuration
if not CUSTOM_API_KEY:
    raise ValueError(
        "Missing OPENAI_API_KEY environment variable.\n"
        "Please copy .env.example to .env and configure your API credentials.\n"
        "See README.md for setup instructions."
    )

# Set environment variables for litellm
os.environ["OPENAI_API_BASE"] = CUSTOM_API_BASE
os.environ["OPENAI_API_KEY"] = CUSTOM_API_KEY


class LLMExcelAutomation:
    """
    Integrates LiteLLM with UnifiedExcelExecutor
    Handles the full workflow from user prompt to Excel file with both openpyxl and pandas
    """

    def __init__(self, tools_file=None, use_minimal_tools=False, use_unified=True, enable_logging=False):
        # Load tool definitions
        if tools_file is None:
            # Use absolute path based on current file location
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Use unified definitions by default
            if use_unified:
                tools_file = os.path.join(current_dir, '..', 'tools', 'unified_definitions.json')
            else:
                tools_file = os.path.join(current_dir, '..', 'tools', 'definitions.json')

        if use_minimal_tools:
            # Use only essential tools for better multi-tool calling
            self.tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "openpyxl_workbook",
                        "description": "Create a new Excel workbook",
                        "parameters": {"type": "object", "properties": {}, "required": []}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "openpyxl_worksheet_append",
                        "description": "Add a row of data to the worksheet",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "iterable": {
                                    "type": "array",
                                    "description": "List of values to append as a row"
                                }
                            },
                            "required": ["iterable"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "openpyxl_workbook_save",
                        "description": "Save the workbook to a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filename": {
                                    "type": "string",
                                    "description": "Path to save the file"
                                }
                            },
                            "required": ["filename"]
                        }
                    }
                }
            ]
        else:
            with open(tools_file, 'r') as f:
                tools_data = json.load(f)
                self.tools = tools_data['tools']

        # Initialize executor
        self.executor = UnifiedExcelExecutor()

        # Conversation history with system prompt
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an investment banking analyst that is a professional at Excel. You will be given Excel tasks to complete."
                )
            }
        ]

        # Initialize logging if enabled
        self.enable_logging = enable_logging
        self.tool_call_log = []
        self.log_file_path = None
        
        if self.enable_logging:
            # Create model_logs directory at project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, '..', '..')
            log_dir = os.path.join(project_root, 'model_logs')
            Path(log_dir).mkdir(exist_ok=True)
            
            # Generate timestamped log filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.log_file_path = os.path.join(log_dir, f"run_{timestamp}.json")
            print(f"📝 Logging enabled: {self.log_file_path}")

    def process_user_request(self, user_prompt, verbose=True):
        """
        Process a user request and execute the necessary Excel operations

        Args:
            user_prompt: What the user wants to do with Excel
            verbose: Print detailed progress

        Returns:
            Final response and execution results
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"USER REQUEST: {user_prompt}")
            print('='*60)

        # Add user message to history
        self.messages.append({"role": "user", "content": user_prompt})

        # Get LLM response with tool calls
        response = completion(
            model=CUSTOM_MODEL_NAME,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=0,  # Set temperature to 0 for deterministic output
            max_tokens=32000,
            api_base=CUSTOM_API_BASE,
            api_key=CUSTOM_API_KEY
        )

        assistant_message = response.choices[0].message
        # Convert to dict, handling both Pydantic v1 and v2
        # Only add if there's actual content or tool calls
        message_dict = assistant_message.model_dump() if hasattr(assistant_message, 'model_dump') else assistant_message.dict()
        
        # Only add message if it has content or tool calls
        if (message_dict.get('content') and message_dict['content'].strip()) or message_dict.get('tool_calls'):
            self.messages.append(message_dict)

        # Check if the model wants to use tools
        if assistant_message.tool_calls:
            if verbose:
                print(f"\n📊 LLM generated {len(assistant_message.tool_calls)} tool calls:")
                # Debug: show all tool calls
                for tc in assistant_message.tool_calls:
                    print(f"  Tool: {tc.function.name}, Args: {tc.function.arguments}")

            tool_results = []

            # Execute each tool call
            for i, tool_call in enumerate(assistant_message.tool_calls):
                tool_name = tool_call.function.name
                try:
                    # Parse arguments (they come as JSON string)
                    arguments = json.loads(tool_call.function.arguments)
                except:
                    arguments = {}

                # Log the tool call
                self._log_tool_call(tool_name, arguments)

                if verbose:
                    print(f"\n{i+1}. Executing: {tool_name}")
                    if arguments:
                        print(f"   Arguments: {arguments}")

                # Execute the tool
                result = self.executor.execute_tool(tool_name, arguments)

                if verbose:
                    if result['status'] == 'success':
                        # Handle both 'result' and 'message' keys
                        output = result.get('result', result.get('message', 'Success'))
                        print(f"   ✅ Result: {output}")
                    else:
                        print(f"   ❌ Error: {result['error']}")

                # Add tool result to conversation
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })

            # Add tool results to messages
            self.messages.extend(tool_results)

            # Allow the model to continue calling tools if needed
            # Keep looping until the model stops calling tools
            max_iterations = 500  # Increased to allow more complex workflows
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # Get response from LLM (it might call more tools or just respond)
                response = completion(
                    model=CUSTOM_MODEL_NAME,
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0,
                    max_tokens=32000,  # Increased to handle 319+ tool sequences with full JSON overhead
                    api_base=CUSTOM_API_BASE,
                    api_key=CUSTOM_API_KEY
                )

                assistant_message = response.choices[0].message

                # Check if more tools are being called
                if assistant_message.tool_calls:
                    if verbose:
                        print(f"\n📊 Tool call #{iteration}: LLM calling tool '{assistant_message.tool_calls[0].function.name}'...")

                    # Add assistant message to history
                    # Only add if there's actual content or tool calls
                    message_dict = assistant_message.model_dump() if hasattr(assistant_message, 'model_dump') else assistant_message.dict()
                    
                    if (message_dict.get('content') and message_dict['content'].strip()) or message_dict.get('tool_calls'):
                        self.messages.append(message_dict)

                    # Execute these new tool calls
                    tool_results = []
                    for i, tool_call in enumerate(assistant_message.tool_calls):
                        tool_name = tool_call.function.name
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except:
                            arguments = {}

                        # Log the tool call
                        self._log_tool_call(tool_name, arguments)

                        if verbose:
                            print(f"  Executing: {tool_name}")
                            if arguments:
                                print(f"    Args: {arguments}")

                        result = self.executor.execute_tool(tool_name, arguments)

                        if verbose:
                            if result['status'] == 'success':
                                # Handle both 'result' and 'message' keys
                                output = result.get('result', result.get('message', 'Success'))
                                print(f"    ✅ {output}")
                            else:
                                print(f"    ❌ {result['error']}")

                        tool_results.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": json.dumps(result)
                        })

                    self.messages.extend(tool_results)
                    # Continue the loop to see if more tools are needed

                else:
                    # No more tool calls, we have the final response
                    final_message = assistant_message.content
                    
                    # Only add message if content is non-empty
                    if final_message and final_message.strip():
                        self.messages.append({"role": "assistant", "content": final_message})

                        if verbose:
                            print(f"\n{'='*60}")
                            print("ASSISTANT RESPONSE:")
                            print(final_message)

                        # Save log before returning
                        self._save_log()
                        return final_message
                    else:
                        # No content but task completed via tools
                        if verbose:
                            print(f"\n{'='*60}")
                            print("ASSISTANT RESPONSE: Task completed via tool calls")
                        
                        # Save log before returning
                        self._save_log()
                        return "Task completed successfully"

            # If we hit max iterations, return what we have
            self._save_log()
            return "Reached maximum iterations"

        else:
            # No tools needed, just return the response
            final_content = assistant_message.content
            
            # Only add message if content is non-empty
            if final_content and final_content.strip():
                self.messages.append({"role": "assistant", "content": final_content})
                
                if verbose:
                    print(f"\n{'='*60}")
                    print("ASSISTANT RESPONSE:")
                    print(final_content)

                # Save log before returning
                self._save_log()
                return final_content
            else:
                # Empty response - shouldn't happen but handle gracefully
                if verbose:
                    print(f"\n{'='*60}")
                    print("ASSISTANT RESPONSE: (empty response)")
                
                # Save log before returning
                self._save_log()
                return "No response provided"

    def _log_tool_call(self, tool_name, arguments):
        """Log a tool call to the in-memory log"""
        if not self.enable_logging:
            return
        
        self.tool_call_log.append({
            "sequence_number": len(self.tool_call_log) + 1,
            "tool": tool_name,
            "arguments": arguments
        })

    def _save_log(self):
        """Save the accumulated tool call log to file"""
        if not self.enable_logging or not self.log_file_path:
            return
        
        log_data = {
            "metadata": {
                "model": CUSTOM_MODEL_NAME,
                "total_tool_calls": len(self.tool_call_log)
            },
            "tool_calls": self.tool_call_log
        }
        
        with open(self.log_file_path, 'w') as f:
            json.dump(log_data, f, indent=2)

    def get_executor_state(self):
        """Get current state of the Excel executor"""
        return self.executor.get_state()

    def reset(self):
        """Reset the system for a new task"""
        self.executor = UnifiedExcelExecutor()
        # Keep the system message, clear the rest
        self.messages = self.messages[:1] if self.messages else []
        # Reset tool call log but keep logging enabled if it was
        if self.enable_logging:
            self.tool_call_log = []
            # Generate new log file for the new session
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, '..', '..')
            log_dir = os.path.join(project_root, 'model_logs')
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.log_file_path = os.path.join(log_dir, f"run_{timestamp}.json")
            print(f"📝 New log file: {self.log_file_path}")


def test_simple_workflow(enable_logging=False):
    """Test a simple Excel creation workflow"""
    print("\n" + "="*70)
    print("TEST: Excel Creation with ALL Tools Available")
    print("="*70)

    # Use ALL tools - testing with bigger context window model
    automation = LLMExcelAutomation(use_minimal_tools=False, enable_logging=enable_logging)  # Changed to False to use all tools
    print(f"Using {len(automation.tools)} tools available")

    # Simple test
    result = automation.process_user_request(
        """

        Investment Banking: 3-Statement Modeling Test (90 Minutes) – Otis Worldwide [OTIS]

        In this case study, you will build a full 3-statement model for Otis, a leading provider of elevators and escalators and related services, starting from a blank sheet in Excel.

        You have 90 minutes to complete this exercise, including the data input for the historical financial statements and the projections over the next 5 years (FY 22 – 26).

        We have provided you with the company's latest 10-K (annual report) in Excel format and the latest investor presentation in PDF format.

        [Note: Update file paths to match your local files when running this test case]

        This is an open-ended case study, so the projection methods, level of detail, and consolidations/simplifications are up to you. The only requirements are as follows:

        1) Revenue Projections – You should use something more than a simple percentage growth rate to project the company’s Revenue.

        2) Minimum Cash – Assume a $3 billion minimum Cash balance in the projected years.

        3) Acquisitions, Debt, Dividends, and Stock Repurchases – Follow the company’s guidance in its investor presentation for these and use common sense regarding Debt issuances vs. repayments and the interest rate in the projected period.

        4) Model Formatting – You do not need to color-code extensively, create separate header/footer formatting, or do anything else complicated due to the time limit. However, please include the basics, such as different number formats for dollars vs. percentages vs. dates.

        5) Company Claims – Make sure you can use your model to assess whether the company’s claims about its expected cumulative FCF, growth rates, margins, dividends, stock repurchases, and FCF conversion are plausible.

        There are no case study questions to answer. Simply finish this model and meet the requirements above.
        """
    )

    print(f"\nFinal state: {automation.get_executor_state()}")
    
    # Note: Model decides filename dynamically - check directory for created files
    print("\n✅ Workflow complete - check current directory for created Excel file")


def test_recording_execution(recording_file_path, enable_logging=False):
    """Execute a recorded Excel workflow from JSON file"""
    import json
    import os
    
    print("\n" + "="*70)
    print("RECORDING EXECUTION MODE")
    print("="*70)
    
    # Check if file exists
    if not os.path.exists(recording_file_path):
        print(f"❌ Error: File not found: {recording_file_path}")
        return
    
    # Read the recording file
    try:
        with open(recording_file_path, 'r') as f:
            recording_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    print(f"\n📁 Loaded recording: {recording_file_path}")
    print(f"   Total steps: {recording_data.get('total_steps', 'unknown')}")
    
    # Format the tool sequence for the LLM
    tool_sequence = recording_data.get('tool_sequence', [])
    if not tool_sequence:
        print("❌ Error: No tool sequence found in recording")
        return
    
    # Create a formatted instruction for the LLM
    instructions = "Open the workbook at path 'income_statement.xlsx' and execute the following Excel operations in order. Make sure to save your workbook before you finish:\n\n"
    for i, step in enumerate(tool_sequence, 1):
        tool = step.get('tool', 'unknown')
        params = step.get('params', {})
        instructions += f"{i}. Call {tool} with parameters: {json.dumps(params)}\n"
    
    # instructions += "\nCreate a new workbook and execute all these operations"
    
    print("\n🤖 Sending to LLM for execution...")
    print("-" * 70)
    
    # Execute with LLM
    automation = LLMExcelAutomation(use_minimal_tools=False, enable_logging=enable_logging)
    result = automation.process_user_request(instructions)
    
    print("\n" + "="*70)
    print(f"✅ Recording execution complete!")
    print(f"Final state: {automation.get_executor_state()}")
    print("="*70)




def test_interactive_mode(enable_logging=False):
    """Interactive mode for testing"""
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70)
    print("Enter Excel commands (type 'quit' to exit, 'reset' to start fresh)")

    automation = LLMExcelAutomation(enable_logging=enable_logging)

    while True:
        user_input = input("\n> ").strip()

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'reset':
            automation.reset()
            print("✅ System reset - starting fresh")
            continue
        elif user_input.lower() == 'state':
            print(f"Current state: {automation.get_executor_state()}")
            continue

        try:
            result = automation.process_user_request(user_input)
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n👋 Goodbye!")


def main(recording_file=None, enable_logging=False):
    """Main function to run tests"""
    print("\n" + "="*70)
    print("LLM EXCEL AUTOMATION SYSTEM")
    print("="*70)

    # Check configuration
    if not CUSTOM_API_KEY or "YOUR_" in CUSTOM_API_KEY:
        print("\n⚠️  Please configure your API credentials in this file first!")
        return

    print(f"\n📋 Configuration:")
    print(f"  Model: {CUSTOM_MODEL_NAME}")
    print(f"  API Base: {CUSTOM_API_BASE}")

    # If recording file provided via command line, execute it directly
    if recording_file:
        test_recording_execution(recording_file, enable_logging)
        return

    print("\nChoose an option:")
    print("1. Run test with all tools")
    print("2. Interactive mode")
    print("3. Execute Excel recording from file")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == '1':
        test_simple_workflow(enable_logging)
    elif choice == '2':
        test_interactive_mode(enable_logging)
    elif choice == '3':
        recording_path = input("\nEnter path to recording JSON file: ").strip()
        test_recording_execution(recording_path, enable_logging)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
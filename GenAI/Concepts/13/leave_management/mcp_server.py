import json
import os
from mcp.server.fastmcp import FastMCP
from leave_management import LeaveManagementSystem

# Get script directory and verify Mock_Data.json
script_dir = os.path.dirname(os.path.abspath(__file__))
mock_data_filename = "Mock_Data.json"
mock_data_path = os.path.join(script_dir, mock_data_filename)

# Debug: List files in directory
files_in_dir = os.listdir(script_dir)
print(f"Files in directory: {files_in_dir}")
print(f"Using mock data path: {mock_data_path}")

# Initialize leave management system
leave_system = LeaveManagementSystem(mock_data_path)

# Initialize MCP server
mcp = FastMCP("sjsu-leave-management")

# Define MCP tools
@mcp.tool()
def check_leave_balance(employee_name: str) -> dict:
    """Check an employee's leave balance and history."""
    return leave_system.check_leave_balance(employee_name)

@mcp.tool()
def apply_for_leave(employee_name: str, leave_date: str) -> dict:
    """Apply for a leave on a specific date."""
    return leave_system.apply_for_leave(employee_name, leave_date)

@mcp.tool()
def get_all_employees() -> dict:
    """List all employees in the system."""
    return leave_system.get_all_employees()

@mcp.tool()
def get_holiday_calendar() -> dict:
    """Retrieve the holiday calendar."""
    return leave_system.get_holiday_calendar()

# Run server
if __name__ == "__main__":
    print("Starting SJSU Leave Management MCP Server...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error running server with stdio: {e}")
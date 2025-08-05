import json
import re
from datetime import datetime

class LeaveManagementSystem:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.data = self._load_data()

    def _load_data(self) -> dict:
        """Load data from Mock_Data.json or return default structure."""
        try:
            with open(self.data_file_path, "r") as file:
                data = json.load(file)
                if "Leaves_Data_Internal_Employees" not in data or "holiday_calendar" not in data:
                    raise ValueError("Missing required keys in JSON")
                return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return {
                "Leaves_Data_Internal_Employees": {
                    "Alice Johnson": {"balance": 10, "history": ["2024-12-12", "2025-01-02"]},
                    "Bob Smith": {"balance": 5, "history": []},
                    "Charlie Davis": {"balance": 8, "history": ["2025-01-02"]}
                },
                "holiday_calendar": [
                    "2025-01-01",
                    "2025-01-20",
                    "2025-02-17",
                    "2025-05-26",
                    "2025-07-04",
                    "2025-09-01",
                    "2025-11-27",
                    "2025-11-28",
                    "2025-12-25",
                    "2025-12-31"
                ]
            }

    def _save_data(self) -> bool:
        """Save data to Mock_Data.json."""
        try:
            with open(self.data_file_path, "w") as file:
                json.dump(self.data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def check_leave_balance(self, employee_name: str) -> dict:
        """Check an employee's leave balance and history."""
        employees = self.data.get("Leaves_Data_Internal_Employees", {})
        if employee_name not in employees:
            return {
                "success": False,
                "message": f"Employee '{employee_name}' not found."
            }
        return {
            "success": True,
            "employee_name": employee_name,
            "leave_balance": employees[employee_name]["balance"],
            "leave_history": employees[employee_name]["history"]
        }

    def apply_for_leave(self, employee_name: str, leave_date: str) -> dict:
        """Apply for a leave, enforcing business rules."""
        if not self._is_valid_date_format(leave_date):
            return {
                "success": False,
                "message": "Invalid date format. Please use YYYY-MM-DD."
            }

        try:
            datetime.strptime(leave_date, "%Y-%m-%d")
        except ValueError:
            return {
                "success": False,
                "message": "Invalid date. Ensure the date is valid (e.g., correct month/day)."
            }

        employees = self.data.get("Leaves_Data_Internal_Employees", {})
        holiday_calendar = self.data.get("holiday_calendar", [])

        if employee_name not in employees:
            return {
                "success": False,
                "message": f"Employee '{employee_name}' not found."
            }

        if leave_date in holiday_calendar:
            return {
                "success": False,
                "message": f"Cannot apply for leave on {leave_date} as it is a holiday."
            }

        if leave_date in employees[employee_name]["history"]:
            return {
                "success": False,
                "message": f"Leave has already been applied for {leave_date}."
            }

        if employees[employee_name]["balance"] <= 0:
            return {
                "success": False,
                "message": f"Insufficient leave balance: {employees[employee_name]['balance']} days."
            }

        employees[employee_name]["history"].append(leave_date)
        employees[employee_name]["balance"] -= 1

        if not self._save_data():
            employees[employee_name]["history"].remove(leave_date)
            employees[employee_name]["balance"] += 1
            return {
                "success": False,
                "message": "Failed to save leave application due to a system error."
            }

        return {
            "success": True,
            "message": f"Leave successfully applied for {leave_date}.",
            "updated_balance": employees[employee_name]["balance"],
            "updated_history": employees[employee_name]["history"]
        }

    def get_all_employees(self) -> dict:
        """List all employee names."""
        employees = self.data.get("Leaves_Data_Internal_Employees", {})
        return {
            "success": True,
            "employee_names": sorted(list(employees.keys()))
        }

    def get_holiday_calendar(self) -> dict:
        """Retrieve the holiday calendar."""
        holiday_calendar = self.data.get("holiday_calendar", [])
        return {
            "success": True,
            "holidays": sorted(holiday_calendar)
        }

    def _is_valid_date_format(self, date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_string))
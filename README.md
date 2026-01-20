# Sales Data Analytics System

## Project Overview
This project is a modular Python system designed to process messy sales transaction logs. It handles data ingestion from non-standard text files, performs strict business logic validation, integrates with a live currency API, and outputs a cleaned dataset for reporting.



## System Architecture
The project is structured modularly to ensure scalability and maintainability:
- `main.py`: The entry point that coordinates the workflow.
- `utils/file_handler.py`: Manages file I/O and handles non-UTF-8 encoding (`latin-1`).
- `utils/data_processor.py`: Contains the core cleaning and analysis logic.
- `utils/api_handler.py`: Connects to an external API for real-time exchange rates.
- `data/`: Directory for input raw text files.
- `output/`: Directory for generated CSV reports.

## Data Cleaning & Validation Rules
The system automatically filters out "invalid" records based on the following criteria:
1. **Structural Integrity**: Records must have all 8 pipe-delimited columns.
2. **Transaction ID**: Must start with the character 'T'.
3. **Missing Data**: Records with empty `CustomerID` or `Region` are removed.
4. **Numeric Validation**: 
    - `Quantity` and `UnitPrice` must be positive (> 0).
    - Removes formatting characters (like commas) from currency and quantity strings.
5. **String Sanitization**: Commas are removed from `ProductName` to prevent CSV formatting issues.

## Setup & Usage
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/NvnHeist/sales-analytics-system.git](https://github.com/NvnHeist/sales-analytics-system.git)
   cd sales-analytics-system

# Prompt to Create `validate_feeds.py` (v2)

## 1. Objective

Create a Python script named `validate_feeds.py` that validates the structural integrity and data correctness of two generated feed files: `G_account_feed.csv` and `G_glossary_feed.csv`. This prompt is an updated version reflecting new requirements for field logic. The script should produce a human-readable report in Markdown format.

## 2. Script Structure

The script should contain the following components:
- **Global Constants:** Define paths for the account feed, glossary feed, and the output results file.
- **`validate_account_feed()` function:** Contains all validation logic for the account feed.
- **`validate_glossary_feed()` function:** Contains all validation logic for the glossary feed.
- **`write_results_to_markdown()` function:** Writes the validation results to a Markdown file.
- **A main execution block** (`if __name__ == "__main__":`) that calls the validation functions and the writing function in order.

## 3. Detailed Functional Requirements

### File Paths
Define these constants at the top of the script:
- `ACCOUNT_FEED_PATH = "C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv"`
- `GLOSSARY_FEED_PATH = "C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv"`
- `RESULTS_FILE_PATH = "C:\Users\zhenq\LocalDesktop\G\output\test_results.md"

### `validate_account_feed()` Function

This function must perform the following checks:

1.  **File Reading:** Open and read `ACCOUNT_FEED_PATH`, separating the content into a header, detail rows, and a trailer. Implement `try-except FileNotFoundError` to gracefully handle cases where the file does not exist, printing an appropriate message and marking the check as `FAIL`.
2.  **Header Validation:**
    - Check that the header has exactly 7 fields.
    - Check that the `feedType` (field at index 1) is exactly `'USER_ACC'`.
    - Check that the `endOfHeaderIndicator` (field at index 6) is exactly `'#||'`.
3.  **Trailer Validation:**
    - Check that the trailer has exactly 3 fields.
    - Check that the `recordCount` (field at index 1) correctly matches the number of detail rows.
    - Check that the `endOfFileIndicator` (field at index 2) is exactly `'EOF'`.
4.  **Detail Row Validation (iterate through each row, starting line numbering from 2 for detail rows):**
    - **Status Check:** `userAccountStatus` (index 4) must be `'ACTV'`.
    - **Email Domain Check:** The processed email (index 7) must end with either `'@CIBCMELLON.COM'` (with one 'C') or `'@BNY.COM'`. If this check fails, print a detailed message including the line number and the failing email domain (e.g., `[FAIL] Line {i}: Invalid email domain: {row[7]}`)).
    - **`personalAccount` Logic:**
        - If the email (index 7) ends with `'@CIBCMELLON.COM'`, the `personalAccount` flag (index 5) must be `'Y'`.
        - If the email (index 7) ends with `'@BNY.COM'`, the `personalAccount` flag (index 5) must be `'N'`. If this check fails, print a detailed message including the line number and the failing email (e.g., `[FAIL] Line {i}: Incorrect personalAccount flag for email {row[7]}`)).
    - **`applicationRole` Format Check:**
        - This check applies to the field at index 12.
        - The `applicationRole` is constructed from `ACTIVITY/ROLE` values only.
        - If the `applicationRole` string is not empty, splitting it by a semicolon (`;`) must not result in any empty parts. An empty `applicationRole` string is considered valid. If this check fails, print a detailed message including the line number and the failing `applicationRole` string (e.g., `[FAIL] Line {i}: Invalid applicationRole format: '{row[12]}'`).

### `validate_glossary_feed()` Function

This function must perform the following checks:

1.  **File Reading:** Open and read `GLOSSARY_FEED_PATH`, separating the content into a header, detail rows, and a trailer. Implement `try-except FileNotFoundError` to gracefully handle cases where the file does not exist, printing an appropriate message and marking the check as `FAIL`.
2.  **Header Validation:**
    - Check that the header has exactly 7 fields.
    - Check that the `feedType` (field at index 1) is exactly `'GLOSSARY'`.
3.  **Trailer Validation:**
    - Check that the `recordCount` (field at index 1) correctly matches the number of detail rows.
4.  **Detail Row Validation:**
    - **Uniqueness Check:** All values for `attributeValueValue` (field at index 2), which is constructed from `ACTIVITY/ROLE` values only, must be unique across all detail rows.

### Output and Reporting

- Create a helper function `print_check(message, status)` that prints the result of a check to the console (e.g., `PASS` or `FAIL`) and stores the formatted result in a global list for later use.
- The `write_results_to_markdown()` function should write all the stored results to `RESULTS_FILE_PATH`, including a title and a generation timestamp formatted as `*Generated on: YYYY-MM-DD HH:MM:SS*`.

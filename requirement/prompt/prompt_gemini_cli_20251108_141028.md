# Prompt to Create `generate_feeds.py` (v2)

## 1. Objective
Create a Python script named `generate_feeds.py` that generates two CSV feed files: `G_account_feed.csv` and `G_glossary_feed.csv`. The script must implement all data transformation, filtering, and formatting rules as specified below.

## 2. General Requirements
- Use `pandas` and `csv` libraries.
- Use `datetime.datetime.now(datetime.UTC)` for timestamps.
- The script should define file paths as global constants.
- The script must contain two main functions: `generate_account_feed()` and `generate_glossary_feed()`.
- The main execution block (`if __name__ == "__main__":`) should call both functions.

## 3. `generate_account_feed()` Requirements

### Input
- `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`

### Output
- `C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv`

### Logic
1.  **Header Row:**
    - **Fields:** Must contain 7 fields.
    - **Field 1 (Timestamp):** `execution_timestamp` in `YYYY/MM/dd HH:MM UTC` format.
    - **Field 2 (`feedType`):** `'USER_ACC'`.
    - **Field 3 (`source`):** `'CDSX'`.
    - **Field 4 (`endPoint`):** `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`.
    - **Field 5 (`recordCount`):** Empty string `''`.
    - **Field 6 (`fileTransmissionHash`):** Empty string `''`.
    - **Field 7 (`endOfHeaderIndicator`):** `'#||'`.
    - All fields must be enclosed in double quotes.
2.  **Trailer Row:**
    - **Fields:** Must contain 3 fields.
    - **Field 1 (Timestamp):** `execution_timestamp` in `YYYY/MM/dd HH:MM UTC` format.
    - **Field 2 (`recordCount`):** The total number of detail rows.
    - **Field 3 (`endOfFileIndicator`):** `'EOF'`.
    - All fields must be enclosed in double quotes.
3.  **Filtering:** Read the input CSV (`latin1` encoding) and filter for rows where `STATUS` is `'ACTV'` and `EMAIL` ends with `@cibcmellon.com` or `@bny.com`.
4.  **Grouping:** Group the filtered data by `USER ID`.
5.  **Detail Row Construction (for each user group):**
    - **`personalAccount` (index 5):** `'Y'` if email ends with `@cibcmellon.com`, else `'N'`.
    - **`email` (index 7):** Remove `cmt.` or `com.` prefix from the source email and convert the result to uppercase.
    - **`entitlement` (index 11):** This field must be an **empty string (`''`)**.
    - **`applicationRole` (index 12):**
        - For each row within a user's group, create a `role_part` string.
        - To create the `role_part`, first sanitize the following fields by replacing any internal semicolons (`;`) with colons (`:`):
            - `ACTIVITY/ROLE`
            - `ACTIVITY LIMIT`
            - `CURRENCY`
        - Join these sanitized parts with a space to form the `role_part`.
        - Aggregate all non-empty `role_part` strings for the user.
        - Join the aggregated `role_part` strings with a semicolon (`;`) to create the final `application_role` string.
    - **Final Processing:**
        - Before writing, apply a `clean_value` function to each field that removes trailing whitespace and replaces double-quotes with single-quotes.
        - Apply a `truncate_value` function to each field based on predefined lengths.
        - After truncation, ensure the final `applicationRole` field (index 12) does not have a trailing semicolon by using `.rstrip(';')`.

## 4. `generate_glossary_feed()` Requirements

### Input
- `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`
- `C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx`

### Output
- `C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv`

### Logic
1.  **Header Row:**
    - **Fields:** Must contain 7 fields.
    - **Field 1 (Timestamp):** `execution_timestamp` in `YYYY/MM/dd HH:MM UTC` format.
    - **Field 2 (`feedType`):** `'GLOSSARY'`.
    - **Field 3 (`source`):** `'CDSX'`.
    - **Field 4 (`endPoint`):** `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`.
    - **Field 5 (`recordCount`):** Empty string `''`.
    - **Field 6 (`fileTransmissionHash`):** Empty string `''`.
    - **Field 7 (`endOfHeaderIndicator`):** `'#||'`.
    - All fields must be enclosed in double quotes.
2.  **Trailer Row:**
    - **Fields:** Must contain 3 fields.
    - **Field 1 (Timestamp):** `execution_timestamp` in `YYYY/MM/dd HH:MM UTC` format.
    - **Field 2 (`recordCount`):** The total number of detail rows.
    - **Field 3 (`endOfFileIndicator`):** `'EOF'`.
    - All fields must be enclosed in double quotes.
3.  **`attributeName` (index 1):** This field must be hardcoded as `"ApplicationRole"`.
4.  **`attributeValueValue` (index 2):**
    - For each row in the source CSV, create a value by:
        1.  Sanitizing the `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` fields by replacing any internal semicolons (`;`) with colons (`:`).
        2.  Joining these sanitized parts with a space.
    - After creating this value for all rows, identify the unique values to serve as the basis for the glossary detail rows.
5.  **`definition-English Desc` (index 3):** Look up the description from `glossary.xlsx`. If not found, use the default text: `"Glossary description not available. Value is considered to be self-explanatory."`.
6.  **Other Fields:** The `endPointName` is `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`, `definition-French Desc` is blank, and `privilegeClassification` is `'000'`.

Create a Python script named `generate_feeds.py` that generates two CSV feed files: `G_account_feed.csv` and `G_glossary_feed.csv`.

The script should perform the following actions:

### **1. Input and Output Files:**
- **Input Files:**
    - `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`
    - `C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx`
- **Output Files:**
    - `C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv`
    - `C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv`

### **2. General Script Structure:**
- The script should contain two main functions: `generate_account_feed()` and `generate_glossary_feed()`.
- The main execution block (`if __name__ == "__main__":`) should call both of these functions.
- The script must include a helper function `clean_value(value)` that removes trailing spaces from strings and replaces any double quotes (`"`) with single quotes (`'`).
- The script must also include a helper function `truncate_value(value, max_length)` that truncates any string value that is longer than the specified `max_length`.

### **3. Source Data Filtering:**
- Before processing, the data from `cmt_genuseraccess_20251105.csv` must be filtered to include only records where:
    - `STATUS` is 'ACTV'.
    - The `EMAIL` domain is either `@cibcmellon.com` or `@bny.com`.
- This filter must be applied independently for both the account feed and the glossary feed generation.

### **4. `generate_account_feed()` Function Details:**

- **Output File:** `G_account_feed.csv`
- **Header Record:**
    - `execution_timestamp`, 'USER_ACC', 'CDSX', 'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities)', '', '', '#||'
- **Detail Records (16 columns):**
    - Group the filtered source data by `USER ID`.
    - For each `USER ID`, create a single detail record with the following fields, truncated to the specified length:
        1.  `endPoint` (256): Static value: `'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities'`
        2.  `domain` (4): Static value: `'CIBC'`
        3.  `name` (50): The `USER ID` from the source file.
        4.  `applicationMapID` (10): Static value: `'127246'`
        5.  `userAccountStatus` (20): The `STATUS` from the source file.
        6.  `personalAccount` (1): `'Y'` if the email ends with `@cibcmellon.com`, otherwise `'N'`.
        7.  `LANID` (50): Leave blank.
        8.  `email` (100): The `EMAIL` from the source file, with any `cmt.` or `com.` prefix removed, converted to uppercase.
        9.  `lastLogin` (20): Leave blank.
        10. `applicationExtractDate` (20): The script's execution timestamp.
        11. `accountUserName` (100): The `USER NAME` from the source file.
        12. `entitlement` (2000): Leave blank.
        13. `applicationRole` (2000): An aggregation of all roles for the user. For each role, combine `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` with a semicolon. Then, join all aggregated role strings with a semicolon. Any semicolons within the original values should be replaced with colons.
        14. `additionalNotes` (250): Leave blank.
        15. `accountCreationDate` (20): Leave blank.
        16. `accountModifyDate` (20): Leave blank.
- **Trailer Record:**
    - `execution_timestamp`, total count of detail records, 'EOF'

### **5. `generate_glossary_feed()` Function Details:**

- **Output File:** `G_glossary_feed.csv`
- **Header Record:**
    - `execution_timestamp`, 'GLOSSARY', 'CDSX', 'MAP_127246_CIBCMellon_CDS_PTM_Processing', '', '', '#||'
- **Detail Records (6 columns):**
    - Create a unique entry for each distinct combination of `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` in the filtered source data.
    - For each unique entry, create a single detail record with the following fields, truncated to the specified length:
        1.  `endPointName` (256): Static value: `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`
        2.  `attributeName` (30): Static value: `'ApplicationRole'`
        3.  `attributeValueValue` (2000): A combination of `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY`, joined by semicolons. Any semicolons within the original values should be replaced with colons.
        4.  `definition-English Desc` (2000): Look up the `ACTIVITY/ROLE` value in the `ApplicationRole` column of `glossary.xlsx`. If a match is found, use the corresponding `EnglishDescription`. If no match is found, use the default text: `"Glossary description not available. Value is considered to be self-explanatory."`
        5.  `definition-French Desc` (2000): Leave blank.
        6.  `privilegeClassification` (3): Static value: `'000'`
- **Trailer Record:**
    - 'MAP_127246_CIBCMellon_CDS_PTM_Processing', total count of detail records, 'EOF'

All fields in both output files should be processed by the `clean_value` and `truncate_value` functions before being written. The CSV files should be written with all fields quoted.
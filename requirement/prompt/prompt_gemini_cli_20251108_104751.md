Create a Python script named `generate_feeds.py` that performs the following two functions: `generate_account_feed` and `generate_glossary_feed`.

**File Paths:**
- Input CMT Genuseraccess CSV file: `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`
- Input Glossary Excel file: `C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx`
- Output Account Feed CSV file: `C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv`
- Output Glossary Feed CSV file: `C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv`

**1. `generate_account_feed` function:**

- Read the `cmt_genuseraccess_20251105.csv` file.
- Filter the data to include only rows where `STATUS` is 'ACTV' and `EMAIL` ends with '@cibcmellon.com' or '@bny.com'.
- Create a header row for the CSV file with the following values: execution timestamp, 'USER_ACC', 'CDSX', 'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities', '', '', '#||'.
- Group the filtered data by 'USER ID'.
- For each user group, create a detail row with the following logic:
    - `personal_account`: 'Y' if email ends with '@cibcmellon.com', else 'N'.
    - `processed_email`: Remove 'cmt.' or 'com.' prefix from the email and convert to uppercase.
    - `application_role`: Concatenate 'ACTIVITY/ROLE', 'ACTIVITY LIMIT', and 'CURRENCY' with spaces in between, and then join multiple roles with a semicolon.
    - The detail row should contain the following fields in order: 'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities', 'CIBC', user_id, '127246', status, personal_account, '', processed_email, '', execution_timestamp, account_user_name, '', application_role, '', '', ''.
- Clean and truncate the values in the detail row.
- Create a trailer row with the execution timestamp, the total number of detail rows, and 'EOF'.
- Write the header, detail, and trailer rows to the `G_account_feed.csv` file.

**2. `generate_glossary_feed` function:**

- Read the `cmt_genuseraccess_20251105.csv` and `glossary.xlsx` files.
- Filter the CMT data similar to the `generate_account_feed` function.
- Create a header row for the CSV file with the following values: execution timestamp, 'GLOSSARY', 'CDSX', 'MAP_127246_CIBCMellon_PTM_processing', '', '', '#||'.
- Create an 'attributeValueValue' column by concatenating 'ACTIVITY/ROLE', 'ACTIVITY LIMIT', and 'CURRENCY' with colons.
- Create unique glossary entries based on the 'attributeValueValue' column.
- For each unique entry, create a detail row with the following logic:
    - `attribute_name`: "ApplicationRole".
    - `english_desc`: Look up the description from the `glossary.xlsx` file based on 'ACTIVITY/ROLE'. If not found, use a default value.
    - The detail row should contain the following fields in order: 'MAP_127246_CIBCMellon_PTM_processing', attribute_name, attribute_value_value, english_desc, '', '000'.
- Clean and truncate the values in the detail row.
- Create a trailer row with the execution timestamp, the total number of detail rows, and 'EOF'.
- Write the header, detail, and trailer rows to the `G_glossary_feed.csv` file.

The script should call both functions when executed.

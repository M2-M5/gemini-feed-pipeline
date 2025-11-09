# Prompt for creating `generate_feeds.py`

## Objective
Create a Python script named `generate_feeds.py` that generates two CSV feed files: `G_account_feed.csv` and `G_glossary_feed.csv`.

## Input Files
1.  `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`: A CSV file containing user access data.
2.  `C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx`: An Excel file containing descriptions for application roles.

## Output Files
1.  `C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv`: The generated account feed file.
2.  `C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv`: The generated glossary feed file.

## Script Requirements

### General
- Use the `pandas` and `csv` libraries.
- Use `datetime.datetime.now(datetime.UTC)` to generate timestamps in the format `%Y/%m/%d %H:%M UTC`.
- Implement error handling for file not found and other exceptions.
- The script should be executable from the command line and call the functions to generate both feeds.

### `generate_account_feed` function
1.  **Timestamp:** Generate an `execution_timestamp`.
2.  **Read Data:** Read `cmt_genuseraccess_20251105.csv` with `latin1` encoding.
3.  **Filter Data:** Filter the DataFrame to include only rows where `STATUS` is `ACTV` and `EMAIL` ends with `@cibcmellon.com` or `@bny.com`.
4.  **Header Row:** The header for the account feed CSV should be: `[execution_timestamp, 'USER_ACC', 'CDSX', 'MAP_127246_CIBCMellon_CDS_PTM_Processing', '', '', '#||']`.
5.  **Group Data:** Group the filtered data by `USER ID`.
6.  **Process Groups:** For each user group:
    - Determine `personal_account`: 'Y' if email ends with `@cibcmellon.com`, else 'N'.
    - Process `email`: remove `cmt.` or `com.` prefix if present, and convert to uppercase.
    - Concatenate `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` to form the `application_role` string, separated by semicolons.
    - Construct a `detail_row` with the following fields:
        - `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`
        - `'CIBC'`
        - `user_id`
        - `'127246'`
        - `STATUS`
        - `personal_account`
        - `''` (LANID)
        - `processed_email`
        - `''` (lastLogin)
        - `execution_timestamp`
        - `USER NAME`
        - `''` (entitlement)
        - `application_role`
        - `''` (additionalNotes)
        - `''` (accountCreationDate)
        - `''` (accountModifyDate)
    - Clean and truncate values in the detail row.
7.  **Trailer Row:** The trailer row should be: `[execution_timestamp, number_of_detail_rows, 'EOF']`.
8.  **Write CSV:** Write the header, detail, and trailer rows to `G_account_feed.csv`.

### `generate_glossary_feed` function
1.  **Timestamp:** Generate an `execution_timestamp`.
2.  **Read Data:** Read `cmt_genuseraccess_20251105.csv` (latin1) and `glossary.xlsx`.
3.  **Filter Data:** Filter the CMT data similar to the account feed.
4.  **Header Row:** The header for the glossary feed CSV should be: `[execution_timestamp, 'GLOSSARY', 'CDSX', 'MAP_127246_CIBCMellon_CDS_PTM_Processing', '', '', '#||']`.
5.  **Create `attributeValueValue`:** Create a new column `attributeValueValue` by concatenating `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` with colons.
6.  **Unique Entries:** Create a DataFrame with unique `attributeValueValue` entries.
7.  **Process Rows:** For each unique entry:
    - `attribute_name` is "ApplicationRole".
    - Look up the `EnglishDescription` in the glossary DataFrame based on `ACTIVITY/ROLE`. If not found, use "Glossary description not available. Value is considered to be self-explanatory.".
    - `french_desc` is an empty string.
    - `privilege_classification` is "000".
    - Construct a `detail_row` with:
        - `'MAP_127246_CIBCMellon_CDS_PTM_Processing'`
        - `attribute_name`
        - `attribute_value_value`
        - `english_desc`
        - `french_desc`
        - `privilege_classification`
    - Clean and truncate values.
8.  **Trailer Row:** The trailer row should be: `[execution_timestamp, number_of_detail_rows, 'EOF']`.
9.  **Write CSV:** Write the header, detail, and trailer rows to `G_glossary_feed.csv`.

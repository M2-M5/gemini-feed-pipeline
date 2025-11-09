# Prompt to create `generate_feeds.py`

## Objective
Create a Python script named `generate_feeds.py` that generates two CSV feed files: `G_account_feed.csv` and `G_glossary_feed.csv`. The script should process data from a source CSV file (`cmt_genuseraccess_20251105.csv`) and an Excel glossary file (`glossary.xlsx`), applying specific filtering, transformations, and formatting rules.

## Input Files
- `C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251105.csv`: Main source data for both feeds.
- `C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx`: Used for looking up English descriptions for the glossary feed.

## Output Files
- `C:\Users\zhenq\LocalDesktop\G\output\G_account_feed.csv`: The generated account feed file.
- `C:\Users\zhenq\LocalDesktop\G\output\G_glossary_feed.csv`: The generated glossary feed file.

## Common Logic and Utilities

### `clean_value(value)` function
- Removes trailing whitespace from string values.
- Replaces double quotes (`"`) with single quotes (`'`) in string values.

### `truncate_value(value, max_length)` function
- Truncates string values to `max_length` if their length exceeds it.

### Execution Timestamp
- A UTC timestamp in the format `YYYY/MM/dd HH:MM UTC` should be generated at the start of each feed generation process and used in header and trailer records.

## Account Feed Generation (`generate_account_feed` function)

### Data Loading and Filtering
- Read `cmt_genuseraccess_20251105.csv` using `latin1` encoding.
- Filter rows where:
    - `STATUS` column is 'ACTV'.
    - `EMAIL` column ends with `@cibcmellon.com` or `@bny.com`.

### Output Structure (`G_account_feed.csv`)

#### Header
- Fields: `execution_timestamp`, `"USER_ACC"`, `"CDSX"`, `"MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities"`, `""`, `""`, `"#||" `.
- Each value must be surrounded by double quotes.
- No space outside the double quotes.
- A comma is the only delimiter between fields.

#### Detail Rows
- Group data by `USER ID`.
- For each user, extract the first row's `EMAIL` and `USER NAME`.
- **Field Mappings and Transformations**:
    - `endPoint`: `"MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities"` (literal string).
    - `domain`: `"CIBC"` (literal string).
    - `name`: Value from `USER ID` column.
    - `applicationMapID`: `"127246"` (literal string).
    - `userAccountStatus`: Value from `STATUS` column.
    - `personalAccount`: `"Y"` if `EMAIL` ends with `@cibcmellon.com`, else `"N"`.
    - `LANID`: Empty string `""`.
    - `processed_email`: Value from `EMAIL` column. Remove `cmt.` or `com.` prefix if present. Convert to uppercase.
    - `lastLogin`: Empty string `""`.
    - `applicationExtractDate`: `execution_timestamp`.
    - `accountUserName`: Value from `USER NAME` column.
    - `entitlement`: Empty string `""`.
    - `applicationRole`:
        - For each row within a user's group, concatenate `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` with a space as a `role_part`. Only include non-empty parts in the space-separated string.
        - Multiple `role_part`s for a single user should be joined by a semicolon (`;`).
    - `additionalNotes`: Empty string `""`.
    - `accountCreationDate`: Empty string `""`.
    - `accountModifyDate`: Empty string `""`.
- Apply `clean_value` to all detail row items.
- Apply `truncate_value` to all detail row items based on the following lengths: `[256, 4, 50, 10, 20, 1, 50, 100, 20, 20, 100, 2000, 2000, 250, 20, 20]`.

#### Trailer
- Fields: `execution_timestamp`, `len(detail_rows)` (count of detail records), `"EOF"`.
- Each value must be surrounded by double quotes.
- No space outside the double quotes.
- A comma is the only delimiter between fields.

## Glossary Feed Generation (`generate_glossary_feed` function)

### Data Loading and Filtering
- Read `cmt_genuseraccess_20251105.csv` using `latin1` encoding.
- Read `glossary.xlsx`.
- Filter rows from `cmt_genuseraccess_20251105.csv` where:
    - `STATUS` column is 'ACTV'.
    - `EMAIL` column ends with `@cibcmellon.com` or `@bny.com`.

### Output Structure (`G_glossary_feed.csv`)

#### Header
- Fields: `execution_timestamp`, `"GLOSSARY"`, `"CDSX"`, `"MAP_127246_CIBCMellon_CDS_PTM_Processing"`, `""`, `""`, `"#||" `.
- Each value must be surrounded by double quotes.
- No space outside the double quotes.
- A comma is the only delimiter between fields.

#### Detail Rows
- Create `attributeValueValue` by concatenating `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY` from `df_cmt` with a semicolon (`;`). Replace any semicolons within these individual fields with colons (`:`).
- Extract unique entries based on the generated `attributeValueValue`.
- **Field Mappings and Transformations**:
    - `endPointName`: `"MAP_127246_CIBCMellon_CDS_PTM_Processing"` (literal string).
    - `attributeName`: `"ApplicationRole"` (literal string).
    - `attributeValueValue`: The unique concatenated value.
    - `definition-English Desc`: Look up `EnglishDescription` from `glossary.xlsx` where `ApplicationRole` matches the `ACTIVITY/ROLE` from the current row. If not found, use `"Glossary description not available. Value is considered to be self-explanatory." `.
    - `definition-French Desc`: Empty string `""`.
    - `privilegeClassification`: `"000"` (literal string).
- Apply `clean_value` to all detail row items.
- Apply `truncate_value` to all detail row items based on the following lengths: `[256, 30, 2000, 2000, 2000, 3]`.

#### Trailer
- Fields: `execution_timestamp`, `len(detail_rows)` (count of detail records), `"EOF"`.
- Each value must be surrounded by double quotes.
- No space outside the double quotes.
- A comma is the only delimiter between fields.

## Error Handling
- Implement `try-except` blocks to catch `FileNotFoundError` for input files and general `Exception` for other errors, printing informative messages.

## Main Execution Block
- Call `generate_account_feed()` and `generate_glossary_feed()` when the script is executed directly.

## Current `generate_feeds.py` for reference:
```python
import pandas as pd
import datetime
import csv

# Define file paths
PTM_ACCOUNTS_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\requirement\\PTM-NeedsToBeCreated.xlsx"
FEED_ACCOUNTS_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\requirement\\feed_files_requirement_20251101.xlsx"
CMT_GENUSERACCESS_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\input\\cmt_genuseraccess_20251105.csv"
GLOSSARY_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\input\\glossary.xlsx"
ACCOUNT_OUTPUT_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\output\\G_account_feed.csv"
GLOSSARY_OUTPUT_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\output\\G_glossary_feed.csv"

def clean_value(value):
    if isinstance(value, str):
        return value.rstrip().replace('"', "'")
    return value

def truncate_value(value, max_length):
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length]
    return value

def generate_account_feed():
    # 1. Execution Timestamp
    execution_timestamp = datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M UTC')

    try:
        # Load data
        df_cmt = pd.read_csv(CMT_GENUSERACCESS_FILE, encoding='latin1')

        # Filter rows
        df_filtered = df_cmt[
            (df_cmt['STATUS'] == 'ACTV') &
            (df_cmt['EMAIL'].str.endswith('@cibcmellon.com', na=False) | df_cmt['EMAIL'].str.endswith('@bny.com', na=False))
        ].copy()

        # Prepare data for CSV
        header_row = [
            execution_timestamp, 'USER_ACC', 'CDSX', 'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities',
            '', '', '#||'
        ]

        # Group by user
        grouped = df_filtered.groupby('USER ID')

        detail_rows = []
        lengths = [256, 4, 50, 10, 20, 1, 50, 100, 20, 20, 100, 2000, 2000, 250, 20, 20]

        for user_id, group in grouped:
            first_row = group.iloc[0]
            email = first_row['EMAIL']
            
            personal_account = 'Y' if email.endswith('@cibcmellon.com') else 'N'

            processed_email = email
            if processed_email.startswith('cmt.'):
                processed_email = processed_email[4:]
            elif processed_email.startswith('com.'):
                processed_email = processed_email[4:]
            processed_email = processed_email.upper()

            account_user_name = first_row['USER NAME']

            application_role_parts = []
            for _, row in group.iterrows():
                activity_role = str(row['ACTIVITY/ROLE']) if pd.notna(row['ACTIVITY/ROLE']) else ''
                activity_limit = str(row['ACTIVITY LIMIT']) if pd.notna(row['ACTIVITY LIMIT']) else ''
                currency = str(row['CURRENCY']) if pd.notna(row['CURRENCY']) else ''
                
                parts = [p for p in [activity_role, activity_limit, currency] if p]
                role_part = ' '.join(parts)
                if role_part:
                    application_role_parts.append(role_part)
            
            application_role = ';'.join(application_role_parts)

            detail_row = [
                'MAP_127246_CDS_CIBCM_(Canadian_Depository_for_Securities', # endPoint
                'CIBC', # domain
                user_id, # name
                '127246', # applicationMapID
                first_row['STATUS'], # userAccountStatus
                personal_account,
                '',  # LANID
                processed_email,
                '',  # lastLogin
                execution_timestamp,  # applicationExtractDate
                account_user_name,
                '',  # entitlement
                application_role,
                '',  # additionalNotes
                '',  # accountCreationDate
                '',  # accountModifyDate
            ]
            
            cleaned_detail_row = [clean_value(item) for item in detail_row]
            truncated_row = [truncate_value(str(item), length) for item, length in zip(cleaned_detail_row, lengths)]
            detail_rows.append(truncated_row)

        trailer_row = [
            execution_timestamp, len(detail_rows), 'EOF'
        ]

        with open(ACCOUNT_OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerow(header_row)
            writer.writerows(detail_rows)
            writer.writerow(trailer_row)
        
        print(f"Successfully transformed data to {ACCOUNT_OUTPUT_FILE}")

    except FileNotFoundError as e:
        print(f"Error: One of the input files was not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def generate_glossary_feed():
    execution_timestamp = datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M UTC')

    try:
        df_cmt = pd.read_csv(CMT_GENUSERACCESS_FILE, encoding='latin1')
        df_glossary = pd.read_excel(GLOSSARY_FILE)

        # Filter rows
        df_cmt = df_cmt[
            (df_cmt['STATUS'] == 'ACTV') &
            (df_cmt['EMAIL'].str.endswith('@cibcmellon.com', na=False) | df_cmt['EMAIL'].str.endswith('@bny.com', na=False))
        ].copy()

        header_row = [
            execution_timestamp,  # headerDateFormat
            'GLOSSARY',           # feedType
            'CDSX',               # source
            'MAP_127246_CIBCMellon_CDS_PTM_Processing', # endPoint
            '',                   # recordCount (in trailer)
            '',                   # fileTransmissionHash
            '#||'                 # endOfHeaderIndicator
        ]

        detail_rows = []
        lengths = [256, 30, 2000, 2000, 2000, 3]

        # Create attributeValueValue and then find unique entries
        df_cmt['attributeValueValue'] = df_cmt.apply(lambda row: ';'.join(filter(None, [
            str(row['ACTIVITY/ROLE']) if pd.notna(row['ACTIVITY/ROLE']) else '',
            str(row['ACTIVITY LIMIT']) if pd.notna(row['ACTIVITY LIMIT']) else '',
            str(row['CURRENCY']) if pd.notna(row['CURRENCY']) else ''
        ])).replace(';', ':'), axis=1)

        df_unique_glossary_entries = df_cmt.drop_duplicates(subset=['attributeValueValue'])

        for _, row in df_unique_glossary_entries.iterrows():
            activity_role = str(row['ACTIVITY/ROLE']) if pd.notna(row['ACTIVITY/ROLE']) else ''
            attribute_value_value = row['attributeValueValue']

            attribute_name = "ApplicationRole"

            # Lookup english description using activity_role
            english_desc_series = df_glossary[df_glossary['ApplicationRole'] == activity_role]['EnglishDescription']
            english_desc = english_desc_series.iloc[0] if not english_desc_series.empty else "Glossary description not available. Value is considered to be self-explanatory."
            
            french_desc = ""

            privilege_classification = "000"

            detail_row = [
                'MAP_127246_CIBCMellon_CDS_PTM_Processing',
                attribute_name,
                attribute_value_value,
                english_desc,
                french_desc,
                privilege_classification
            ]
            
            cleaned_detail_row = [clean_value(item) for item in detail_row]
            truncated_row = [truncate_value(str(item), length) for item, length in zip(cleaned_detail_row, lengths)]
            detail_rows.append(truncated_row)

        trailer_row = [
            execution_timestamp,
            len(detail_rows),
            'EOF'
        ]

        with open(GLOSSARY_OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerow(header_row)
            writer.writerows(detail_rows)
            writer.writerow(trailer_row)
        
        print(f"Successfully transformed data to {GLOSSARY_OUTPUT_FILE}")

    except FileNotFoundError as e:
        print(f"Error: One of the input files was not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_account_feed()
    generate_glossary_feed()
```
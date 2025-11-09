# Test Plan: Feed File Generation

## 1. Test Objectives

This test plan outlines the procedures for validating the `generate_feeds.py` script. The primary objectives are to ensure:

*   **Correctness**: The generated feed files (`G_account_feed.csv` and `G_glossary_feed.csv`) are accurate and conform to the specified format.
*   **Completeness**: All active and relevant records from the source files are processed and included in the output files.
*   **Robustness**: The script handles malformed data, missing inputs, and other edge cases gracefully.
*   **Data Integrity**: Data transformations, cleaning, and truncation are applied correctly.

## 2. Test Scenarios

### 2.1. Account Feed (`G_account_feed.csv`)

| Scenario ID | Description                                                                 |
| :---------- | :-------------------------------------------------------------------------- |
| AC-01       | **Valid Input**: Run the script with a valid `cmt_genuseraccess_20251105.csv` file. |
| AC-02       | **Filtering Logic**: Ensure only records with `STATUS` 'ACTV' are included.     |
| AC-03       | **Email Filtering**: Verify that only records with emails ending in `@cibcmellon.com` or `@bny.com` are processed. |
| AC-04       | **Data Transformation**: Check the correctness of transformations (e.g., `personal_account`, `processed_email`, `account_user_name`). |
| AC-05       | **Field Concatenation**: Validate the `application_role` field is correctly concatenated. |
| AC-06       | **Header and Trailer**: Confirm the header and trailer rows are correctly formatted and populated. |
| AC-07       | **Missing Input File**: Run the script without the `cmt_genuseraccess_20251105.csv` file. |
| AC-08       | **Empty Input File**: Run the script with an empty `cmt_genuseraccess_20251105.csv` file. |
| AC-09       | **Malformed Data**: Input file contains records with missing values for key fields (e.g., `EMAIL`, `USER ID`). |

### 2.2. Glossary Feed (`G_glossary_feed.csv`)

| Scenario ID | Description                                                                 |
| :---------- | :-------------------------------------------------------------------------- |
| GL-01       | **Valid Input**: Run the script with valid `cmt_genuseraccess_20251105.csv` and `glossary.xlsx` files. |
| GL-02       | **Unique Entries**: Ensure the glossary feed contains only unique `attributeValueValue` entries. |
| GL-03       | **Description Lookup**: Verify that the `EnglishDescription` is correctly looked up from `glossary.xlsx`. |
| GL-04       | **Default Description**: If a description is not found, ensure the default text is used. |
| GL-05       | **Header and Trailer**: Confirm the header and trailer rows are correctly formatted. |
| GL-06       | **Missing Glossary File**: Run the script without the `glossary.xlsx` file. |

### 2.3. CSV Formatting Rules

*   Each value must be surrounded by double quotes.
*   No space outside the double quotes.
*   A comma is the only delimiter between fields.

### 2.4. Glossary Feed Requirements

#### Header

| Field | Value | Mandatory/Conditional | Notes |
| :--- | :--- | :--- | :--- |
| headerDateFormat | "YYYY/MM/dd HH:mm UTC" | Mandatory | | 
| feedType | "GLOSSARY" | Mandatory | | 
| source | "CDSX" | Mandatory | | 
| endPoint | "MAP_127246_CIBCMellon_PTM_processing" | Mandatory | | 
| recordCount | | Conditional | Leave this field blank | 
| fileTransmissionHash | | Optional | Leave this field blank | 
| endOfHeaderIndicator | "#||" | Mandatory | | 

#### Trailer

| Field | Value | Mandatory/Conditional | Notes |
| :--- | :--- | :--- | :--- |
| trailerDateFormat | "YYYY/MM/dd HH:mm UTC" | Mandatory | | 
| recordCount | | Conditional | Must be provided | 
| endOfFileIndicator | "EOF" | Mandatory | | 

#### Detail

| Field | Value | Mandatory/Conditional | Max Length |
| :--- | :--- | :--- | :--- |
| endPointName | "MAP_127246_CIBCMellon_PTM_processing" | Mandatory | 256 |
| attributeName | "ApplicationRole" | Mandatory | 30 |
| attributeValueValue | Map include "Activity/Role" "Activity limit" "Currency" columns source file | Mandatory | 2000 |
| definition-English Desc | Definitions shall be from GLOSSARY.xlsx Definitions displays after attriabuteValueValue matched applicationRole | Mandatory | 2000 |
| definition-French Desc | | Optional | 2000 |
| privilegeClassification | "000" | Mandatory | 3 |

### 2.5. Account Feed Requirements

#### Header

| Field | Value | Mandatory/Conditional | Notes |
| :--- | :--- | :--- | :--- |
| headerDateFormat | "YYYY/MM/dd HH:mm UTC" | Mandatory | |
| feedType | "USER_ACC" | Mandatory | |
| source | "CDSX" | Mandatory | Insert name of application source system |
| endPoint | "MAP_127246_CIBCMellon_PTM_processing" | Mandatory | |
| recordCount | | Conditional | This field is to be left blank (null). |
| fileTransmissionHash | | Optional | Leave this field blank. |
| endOfHeaderIndicator | "#||" | Mandatory | |

#### Trailer

| Field | Value | Mandatory/Conditional | Notes |
| :--- | :--- | :--- | :--- |
| trailerDateFormat | "YYYY/MM/dd HH:mm UTC" | Mandatory | |
| recordCount | | Conditional | Must be provided in trailer record |
| endOfFileIndicator | "EOF" | Mandatory | |

#### Detail

| Field | Value | Mandatory/Conditional | Max Length |
| :--- | :--- | :--- | :--- |
| endPoint | "MAP_127246_CIBCMellon_PTM_processing" | Mandatory | 256 |
| domain | "CIBC" | Mandatory | 4 |
| name | data field "User ID" from source file | Mandatory | 50 |
| applicationMapID | "127246" | Optional | 10 |
| userAccountStatus | "ACTV" | Mandatory | 20 |
| personalAccount | "Y" for "@cibcmellon.com" domain, "N" for "@bny.com" domain | Mandatory | 1 |
| LANID | | Conditional | 50 |
| email | from "email" data field from source file, prefix "CMT." must be removed, field must be uppercase | Conditional | 100 |
| lastLogIn | N/A | Optional | 20 |
| applicationExtractDate | "YYYY/MM/dd HH:mm UTC" | Mandatory | 20 |
| accountUserName | retrieve from data field "User Name" source file | Optional | 100 |
| entitlement | | Conditional | 2000 each, Multivalued attributes |
| applicationRole | Map this field to include "Activity/Role", "Activity limit", and "Currency" columns from the source file. For each role, these three values should be joined by a space. Multiple roles should then be separated by a semicolon ";". | Conditional | 2000 each, Multivalued attributes |
| additionalNotes | | Optional | 250 each, Multivalued attributes |
| accountCreationDate | | Optional | 20 |
| accountModifyDate | | Optional | 20 |

## 3. Expected Outcomes

| Scenario ID | Expected Outcome                                                                                                |
| :---------- | :-------------------------------------------------------------------------------------------------------------- |
| AC-01       | `G_account_feed.csv` is generated successfully with the correct data.                                           |
| AC-02       | The output file contains no records with `STATUS` other than 'ACTV'.                                            |
| AC-03       | The output file contains no records with emails other than the specified domains.                               |
| AC-04       | Transformed fields match the logic defined in the script.                                                       |
| AC-05       | `application_role` is a semicolon-separated string of `ACTIVITY/ROLE`, `ACTIVITY LIMIT`, and `CURRENCY`.          |
| AC-06       | The header contains the execution timestamp and correct titles. The trailer contains the record count.          |
| AC-07       | The script prints a "File not found" error and exits gracefully.                                                |
| AC-08       | The script generates an empty feed file with only a header and a trailer (with a record count of 0).            |
| AC-09       | The script handles missing values without crashing, and the corresponding fields in the output are empty.         |
| GL-01       | `G_glossary_feed.csv` is generated successfully.                                                                |
| GL-02       | No duplicate `attributeValueValue` rows exist in the output.                                                    |
| GL-03       | `EnglishDescription` in the output matches the corresponding entry in `glossary.xlsx`.                          |
| GL-04       | The `EnglishDescription` field is populated with "Glossary description not available...".                       |
| GL-05       | The header and trailer are correct.                                                                             |
| GL-06       | The script prints a "File not found" error and exits gracefully.                                                |

## 4. Validation Methods

*   **Automated Scripting**: Python scripts will be used to read the generated CSV files and assert the expected outcomes.
*   **Manual Inspection**: For complex data transformations, manual inspection of the output files will be performed.
*   **CLI Execution**: Tests involving missing files or script errors will be validated by running `generate_feeds.py` from the command line and checking the output.

## 5. Edge Case Coverage

1.  **Character Encoding**: The input files use `latin1` encoding. The test suite should include a file with special characters (e.g., `é`, `ç`) to ensure they are handled correctly.
2.  **Large File Processing**: Test the script's performance and memory usage with a large input file (e.g., >1 million records) to identify potential bottlenecks.
3.  **Data Truncation**: Input data for fields with length limits (e.g., `account_user_name`) should exceed the maximum length to verify that truncation is applied correctly.

## 6. Logging & Archiving

*   **Test Execution Logs**: All test runs will be logged to a file, including the date, time, scenario ID, and pass/fail status.
*   **Output Archiving**: The generated feed files from each test run will be archived in a timestamped directory (e.g., `test_results/YYYYMMDD_HHMMSS/`) for future reference and comparison.
*   **Defect Tracking**: Any failures will be logged as issues in a defect tracking system, with links to the relevant logs and archived files.
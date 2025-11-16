import csv
import re
import datetime
import sys

import csv
import re
import datetime
import sys

# Global variables for file paths, to be set by command-line arguments
ACCOUNT_FEED_PATH = None
GLOSSARY_FEED_PATH = None
RESULTS_FILE_PATH = "C:\\Users\\zhenq\\LocalDesktop\\G\\output\\test_results.md"

TEST_RESULTS = []

def print_check(message, status):
    result = 'PASS' if status else 'FAIL'
    print(f"- {message}: {result}")
    TEST_RESULTS.append(f"- {message}: **{result}**\n")



def validate_account_feed():
    """Validates the G_account_feed.csv file based on test_plan.md."""
    print("\n--- Validating Account Feed ---")
    TEST_RESULTS.append("\n## Account Feed Validation\n")
    


    try:
        with open(ACCOUNT_FEED_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
    except FileNotFoundError:
        print_check(f"Account feed file not found at {ACCOUNT_FEED_PATH}", False)
        return

    header = lines[0]
    trailer = lines[-1]
    detail_rows = lines[1:-1]

    print_check("Header has 7 fields", len(header) == 7)
    print_check("Header feedType is 'USER_ACC'", header[1] == 'USER_ACC')
    print_check("Header endOfHeaderIndicator is '#||'", header[6] == '#||')
    print_check("Trailer has 3 fields", len(trailer) == 3)
    print_check("Trailer recordCount matches detail rows", int(trailer[1]) == len(detail_rows))
    print_check("Trailer endOfFileIndicator is 'EOF'", trailer[2] == 'EOF')

    all_status_actv = True
    all_emails_valid = True
    all_personal_accounts_valid = True
    all_app_roles_valid = True
    all_detail_rows_correct_length = True

    for i, row in enumerate(detail_rows, 2): # Start from line 2 for logging
        if len(row) != 16:
            all_detail_rows_correct_length = False
            print(f"  [FAIL] Line {i}: Detail row does not have 16 fields. Found {len(row)} fields.")
            continue # Skip other checks for this malformed row

        if row[4] != 'ACTV':
            all_status_actv = False
        
        if not (row[7].endswith('@CIBCMELLON.COM') or row[7].endswith('@BNY.COM')):
            all_emails_valid = False
            print(f"  [FAIL] Line {i}: Invalid email domain: {row[7]}")

        if (row[7].endswith('@CIBCMELLON.COM') and row[5] != 'Y') or \
           (row[7].endswith('@BNY.COM') and row[5] != 'N'):
            all_personal_accounts_valid = False
            print(f"  [FAIL] Line {i}: Incorrect personalAccount flag for email {row[7]}")

        roles = row[12].split(';')
        # Check for empty roles between semicolons
        if row[12].strip() != '' and not all(role.strip() for role in roles):
            all_app_roles_valid = False
            print(f"  [FAIL] Line {i}: Invalid applicationRole format: '{row[12]}'")

    print_check("All detail rows have 16 fields", all_detail_rows_correct_length)
    print_check("All userAccountStatus are 'ACTV'", all_status_actv)
    print_check("All emails have correct domain", all_emails_valid)
    print_check("personalAccount logic is correct", all_personal_accounts_valid)
    print_check("applicationRole format is correct", all_app_roles_valid)

def validate_glossary_feed():
    """Validates the G_glossary_feed.csv file based on test_plan.md."""
    print("\n--- Validating Glossary Feed ---")
    TEST_RESULTS.append("\n## Glossary Feed Validation\n")



    try:
        with open(GLOSSARY_FEED_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
    except FileNotFoundError:
        print_check(f"Glossary feed file not found at {GLOSSARY_FEED_PATH}", False)
        return

    header = lines[0]
    trailer = lines[-1]
    detail_rows = lines[1:-1]

    print_check("Header has 7 fields", len(header) == 7)
    print_check("Header feedType is 'GLOSSARY'", header[1] == 'GLOSSARY')
    print_check("Trailer recordCount matches detail rows", int(trailer[1]) == len(detail_rows))

    attribute_values = []
    all_detail_rows_correct_length = True
    for i, row in enumerate(detail_rows, 2):
        if len(row) != 6:
            all_detail_rows_correct_length = False
            print(f"  [FAIL] Line {i}: Detail row does not have 6 fields. Found {len(row)} fields.")
            continue
        attribute_values.append(row[2])
    
    print_check("All detail rows have 6 fields", all_detail_rows_correct_length)
    print_check("attributeValueValue entries are unique", len(attribute_values) == len(set(attribute_values)))

def write_results_to_markdown():
    """Writes the collected test results to a markdown file."""
    with open(RESULTS_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(f"# Feed Validation Test Results\n")
        f.write(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        f.writelines(TEST_RESULTS)
    print(f"\nResults saved to {RESULTS_FILE_PATH}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_feeds.py <account_feed_path> <glossary_feed_path>")
        sys.exit(1)
    
    ACCOUNT_FEED_PATH = sys.argv[1]
    GLOSSARY_FEED_PATH = sys.argv[2]

    validate_account_feed()
    validate_glossary_feed()
    
    write_results_to_markdown()
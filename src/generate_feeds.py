import pandas as pd
import datetime
import csv

# Define file paths
CMT_GENUSERACCESS_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\input\\cmt_genuseraccess_20251105.csv"
GLOSSARY_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\input\\glossary.xlsx"
ACCOUNT_OUTPUT_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\output\\gt_account_feed.csv"
GLOSSARY_OUTPUT_FILE = "C:\\Users\\zhenq\\LocalDesktop\\G\\output\\gt_glossary_feed.csv"

def clean_value(value):
    if isinstance(value, str):
        return value.rstrip().replace('"', "'")
    return value

def truncate_value(value, max_length):
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length]
    return value

def generate_account_feed():
    execution_timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y/%m/%d %H:%M UTC')

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
            execution_timestamp, 'USER_ACC', 'CDSX', 'MAP_127246_CIBCMellon_CDS_PTM_Processing',
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
                activity_role = str(row['ACTIVITY/ROLE']).replace(';', ':') if pd.notna(row['ACTIVITY/ROLE']) else ''
                activity_limit = str(row['ACTIVITY LIMIT']).replace(';', ':') if pd.notna(row['ACTIVITY LIMIT']) else ''
                currency = str(row['CURRENCY']).replace(';', ':') if pd.notna(row['CURRENCY']) else ''
                # last_update_date = str(row['LAST UPDATE DATE']).replace(';', ':') if pd.notna(row['LAST UPDATE DATE']) else ''
                
                parts = [p for p in [activity_role, activity_limit, currency] if p]
                role_part = ' '.join(parts)
                if role_part:
                    application_role_parts.append(role_part)
            
            application_role = ';'.join(application_role_parts)
            # Ensure no trailing semicolon after truncation
            application_role = application_role.rstrip(';')

            detail_row = [
                'MAP_127246_CIBCMellon_CDS_PTM_Processing', # endPoint
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
                '',  # entitlement (reverted to empty string)
                application_role,
                '',  # additionalNotes
                '',  # accountCreationDate
                '',  # accountModifyDate
            ]
            
            cleaned_detail_row = [clean_value(item) for item in detail_row]
            truncated_row = [truncate_value(str(item), length) for item, length in zip(cleaned_detail_row, lengths)]
            # Ensure no trailing semicolon after truncation for application_role
            truncated_row[12] = truncated_row[12].rstrip(';')
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
    execution_timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y/%m/%d %H:%M UTC')

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
        df_cmt['attributeValueValue'] = df_cmt.apply(
            lambda row: ' '.join(filter(None, [
                str(row['ACTIVITY/ROLE']).replace(';', ':') if pd.notna(row['ACTIVITY/ROLE']) else '',
                str(row['ACTIVITY LIMIT']).replace(';', ':') if pd.notna(row['ACTIVITY LIMIT']) else '',
                str(row['CURRENCY']).replace(';', ':') if pd.notna(row['CURRENCY']) else ''
            ])),
            axis=1
        )

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

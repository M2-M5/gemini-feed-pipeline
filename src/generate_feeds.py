import pandas as pd
import datetime
import csv

# Define file paths
CMT_GENUSERACCESS_FILE = "C:\Users\zhenq\LocalDesktop\G\input\cmt_genuseraccess_20251115.csv"
GLOSSARY_FILE = "C:\Users\zhenq\LocalDesktop\G\input\glossary.xlsx"
ACCOUNT_OUTPUT_FILE = "C:\Users\zhenq\LocalDesktop\G\output\gt_account_feed.csv"
GLOSSARY_OUTPUT_FILE = "C:\Users\zhenq\LocalDesktop\G\output\gt_glossary_feed.csv"

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
        lengths = [256, 4, 50, 10, 20, 1, 50, 100, 20, 20, 100, 450, 450, 250, 20, 20]

        for user_id, group in grouped:
            first_row = group.iloc[0]
            email = first_row['EMAIL']
            
            personal_account = 'Y' if email.endswith('@cibcmellon.com') else 'N'

            email = email
            if email.startswith('cmt.'):
                email = email[4:]
            elif email.startswith('com.'):
                email = email[4:]
            email = email.upper()

            accountUserName = first_row['USER NAME']

            application_role_parts = []
            for _, row in group.iterrows():
                activity_role = str(row['ACTIVITY/ROLE']).replace(';', ':') if pd.notna(row['ACTIVITY/ROLE']) else ''
                if activity_role:
                    application_role_parts.append(activity_role)
            
            applicationRole = ';'.join(application_role_parts)
            # Ensure no trailing semicolon after truncation
            applicationRole = applicationRole.rstrip(';')

            detail_row = [
                'MAP_127246_CIBCMellon_CDS_PTM_Processing', # endPoint
                'CIBC', # domain
                user_id, # name
                '127246', # applicationMapID
                first_row['STATUS'], # userAccountStatus
                personal_account, # personalAccount
                '',  # LANID
                email,  # email
                '',  # lastLogIn
                execution_timestamp,  # applicationExtractDate
                accountUserName,  # accountUserName
                '',  # entitlement
                applicationRole, # applicationRole
                '',  # additionalNotes
                '',  # accountCreationDate
                '',  # accountModifyDate
            ]
            
            cleaned_detail_row = [clean_value(item) for item in detail_row]
            truncated_row = [truncate_value(str(item), length) for item, length in zip(cleaned_detail_row, lengths)]
            # Ensure no trailing semicolon after truncation for applicationRole
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
        lengths = [256, 322, 450, 1024, 1024, 3]

        # Create attributeValueValue and then find unique entries
        df_cmt['attributeValueValue'] = df_cmt.apply(
            lambda row: str(row['ACTIVITY/ROLE']).replace(';', ':') if pd.notna(row['ACTIVITY/ROLE']) else '',
            axis=1
        )

        df_unique_glossary_entries = df_cmt.drop_duplicates(subset=['attributeValueValue'])

        for _, row in df_unique_glossary_entries.iterrows():
            activity_role = str(row['ACTIVITY/ROLE']) if pd.notna(row['ACTIVITY/ROLE']) else ''
            field2attributeValueValue = row['attributeValueValue']

            attributeName = "ApplicationRole"

            # Lookup english description using activity_role
            english_desc_series = df_glossary[df_glossary['ApplicationRole'] == activity_role]['EnglishDescription']
            definition_English_Desc = english_desc_series.iloc[0] if not english_desc_series.empty else "Glossary description not available. Value is considered to be self-explanatory."
            
            definition_French_Desc = ""

            privilegeClassification = "000"

            detail_row = [
                'MAP_127246_CIBCMellon_CDS_PTM_Processing',
                attributeName,
                field2attributeValueValue,
                definition_English_Desc,
                definition_French_Desc,
                privilegeClassification
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

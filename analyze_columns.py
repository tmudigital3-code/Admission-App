import pandas as pd

# Read the adm_25-26.csv file
df_new = pd.read_csv('adm_25-26.csv', nrows=1)
new_columns = set(df_new.columns.tolist())

# Expected columns from the current dashboard
expected_columns = {
    'Date of Admission',
    'enquiry date',
    'Date of Birth',
    'Gender',
    'Category',
    'Religion',
    'Programme Name',
    'Program Level',
    'Student Status',
    'erp20may_State',
    'Source',
    'Family Annual Income',
    'Prequalification Percentage'
}

# Check which expected columns are present in the new file
present_columns = expected_columns.intersection(new_columns)
missing_columns = expected_columns.difference(new_columns)

print("Present columns:")
for col in present_columns:
    print(f"  - {col}")

print("\nMissing columns:")
for col in missing_columns:
    print(f"  - {col}")

# Look for potential mappings
print("\nPotential mappings for missing columns:")
new_col_list = list(new_columns)
mapping_suggestions = {}

for missing_col in missing_columns:
    suggestions = []
    for new_col in new_col_list:
        # Check for partial matches
        if missing_col.lower().replace(' ', '_') in new_col.lower() or \
           new_col.lower().replace(' ', '_') in missing_col.lower().replace(' ', '_'):
            suggestions.append(new_col)
    if suggestions:
        mapping_suggestions[missing_col] = suggestions
        print(f"  {missing_col} -> {suggestions}")

# Check for specific mappings
print("\nSpecific column mappings found:")
# Date of Admission
if 'Date of Admission' not in new_columns and 'Date of Joining' in new_columns:
    print("  Date of Admission -> Date of Joining")

# erp20may_State
if 'erp20may_State' not in new_columns and 'State' in new_columns:
    print("  erp20may_State -> State")

# Programme Name
if 'Programme Name' not in new_columns and 'Course Name' in new_columns:
    print("  Programme Name -> Course Name")

# Program Level
if 'Program Level' not in new_columns and 'Year' in new_columns:
    print("  Program Level -> Year")

# Family Annual Income
if 'Family Annual Income' not in new_columns and 'Guardian Annual Income' in new_columns:
    print("  Family Annual Income -> Guardian Annual Income")

# Prequalification Percentage
if 'Prequalification Percentage' not in new_columns and 'Pre. Inst. Percentage of Mark' in new_columns:
    print("  Prequalification Percentage -> Pre. Inst. Percentage of Mark")

# enquiry date - this might be missing
print("\nNote: 'enquiry date' column is not present in the new file and may need to be handled separately")
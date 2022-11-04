# importing important libraries
import pandas as pd
import json as js
import hashlib

# reading the nft properties file
print("This program generates a sha_25 hash for each row in the csv and adds the value to a column in the csv")
filename = input('Input csv filepath: ')
csv_file = pd.read_csv(filename)

# these blocks of code creates key value pairs of the individual attributes of the nfts
attributes = csv_file['Attributes']
keys_all = []
keys_per_row = []
values_per_row = []

for i in attributes:
    j = i.replace(": ", ":")
    gg = j.split("; ")
    li_key = []
    li_value = []
    for a in gg:
        k = a.split(":")
        keys_all.append(k[0].strip())
        li_key.append(k[0].strip())
        li_value.append(k[1])
    keys_per_row.append(li_key)
    values_per_row.append(li_value)
    
unique_keys = set(keys_all)

new_dict = {}
for i in unique_keys:
    new_dict[i] = []
    
for i,j in zip(keys_per_row, values_per_row):
    for x,y in zip(i,j):
        new_dict[x]+=[y]

# adding the generated key value pairs into the dataframe of nft properties
for i in new_dict.keys():
    csv_file[i] = new_dict[i]

# these blocks of code generates the sha_256 
sha_256 = []

def sha256_gen(fn):
    return hashlib.sha256(open(fn, 'rb').read()).hexdigest()

for col, row in csv_file.iterrows():
    out_file = open("myfile.json", "w") 
    json_file = js.dump({
        "format": "CHIP-0007",
        "series_number": row["Series Number"],
        "filename": row["Filename"],
        "name": row['Name'],
        "description": row['Description'],
        "minting_tool": row['TEAM NAMES'],
        "sensitive_content": False,
        "gender": row["Gender"],
        "attributes":[
            {
                "trait_type": "hair",
                "value": row['hair'],
            },
            {
                "trait_type": "eyes",
                "value": row['eyes'],
            },
            {
                "trait_type": "clothing",
                "value": row['clothing'],
            },
            {
                "trait_type": "accessories",
                "value": row['accessories'],
            },
            {
                "trait_type": "teeth",
                "value": row['teeth'],
            },
            {
                "trait_type": "strength",
                "value": row['strength'],
            },
            {
                "trait_type": "weakness",
                "value": row['weakness'],
            },
            {
                "trait_type": "expressions",
                "value": row['expressions'],
            },
        ],
        "collection": {
            "name": row['Name'],
            "id": row["UUID"]
        }
    }, out_file)
    out_file.close()
    
    sha256_hash = sha256_gen("myfile.json")
    sha_256.append(sha256_hash)

#adding the sha_256 to each row of the nft properties file
submission_csv = pd.read_csv(filename)
submission_csv['sha_256'] = sha_256

print("Output file created successfully")
#downloading the result
submission_csv.to_csv("output.csv")
import json
import os

src_dir = r'C:\Users\salom\OneDrive\Documentos\DRAMA\MelpomeneSARA516\input'
src_file = os.path.join(src_dir, 'dmf_input.json')

tgt_dir = r'C:\Users\salom\OneDrive\Documentos\DRAMA\MelpomeneSARA516_100\input'
out_file = os.path.join(tgt_dir, 'dmf_input.json')

mass_factor = 1/100 # change this depending on the scale
linear_factor = mass_factor ** (1/3)

if not os.path.exists(tgt_dir):
    os.makedirs(tgt_dir)

with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

objects = data['missionDefinition']['satelliteDefinitions'][0]['3dModel']['objects']

print(f"Scaling down {len(objects)} components...")
print(f"Mass factor: {mass_factor} | Linear factor: {linear_factor}")

geom_keys = ['width', 'length', 'height', 'radius', 'innerRadius', 'positionX', 'positionY', 'positionZ']

for obj in objects:
    if 'mass' in obj:
        obj['mass'] *= mass_factor
        
    for key in geom_keys:
        if key in obj:
            obj[key] *= linear_factor

# scale total dry mass if present
sat_def = data['missionDefinition']['satelliteDefinitions'][0]
if 'dryMass' in sat_def:
    sat_def['dryMass'] *= mass_factor

with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"Done. Scaled file saved to {out_file}")
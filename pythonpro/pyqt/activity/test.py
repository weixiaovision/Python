import xml.etree.ElementTree as ET


tree = ET.parse('update.xml')
root = tree.getroot()
for child in root[0]:
    print(child.text)

for child in root[1]:
    print(child.text)

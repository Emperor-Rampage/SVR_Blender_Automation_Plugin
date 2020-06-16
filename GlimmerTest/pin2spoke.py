#
# PIN2SPOKE
#
# A utility script to harvest pinned objects from an objects.gltf file produced by hubs;
# save those objects, with their transforms and source URLs, into an sqlite database; 
# and then write out a "legacy" spoke file containing those objects.
#

import sys
import json
import sqlite3
import uuid

if (len(sys.argv)!=4):
    print("Two arguments required: objects gltf file, and spoke file.")
    sys.exit()

gltf_filename = sys.argv[1]
spoke_filename = sys.argv[2]
room_name =  sys.argv[3]

print ("Importing gltf: " + gltf_filename + " exporting spoke: " + spoke_filename)

db = sqlite3.connect('../ocf_rooms.db')
c = db.cursor()

#First, check if the room name exists, if not insert it.
select_query = "SELECT id FROM room WHERE name='" + room_name + "';"
c.execute(select_query)
rows = c.fetchall()
if (len(rows)==0):
    insert_query = "INSERT INTO room (name) VALUES ('" + room_name + "');"
    c.execute(insert_query)
    db.commit()
    c.execute(select_query)
    rows = c.fetchall()
    
room_id = rows[0][0]
print("Room ID: " + str(room_id))

with open(gltf_filename, "r") as read_file:
    file_data = json.load(read_file)
    read_file.close()

#out_str = json.dumps(file_data,indent=4)
#print(out_str)


#NOW: we need to step through the file, and load all the nodes
for obj in file_data:
    print(str(obj))
    if (obj == "scenes"):
        print(str(file_data["scenes"][0]["name"]))
        #print(str(obj[0]["name"]))
        for i in file_data["scenes"][0]["nodes"]:
            print("index: " + str(i))
    if (obj == "nodes"):
        print("NODES")
        
for n in file_data["nodes"]:
    t_x = 0.0
    t_y = 0.0
    t_z = 0.0
    r_x = 0.0
    r_y = 0.0
    r_z = 0.0
    s_x = 1.0
    s_y = 1.0
    s_z = 1.0
    name = ""
    media_url = ""
    media_id = ""
    
    if "translation" in n:
        t_x = round(n["translation"][0],3)
        t_y = round(n["translation"][1],3)
        t_z = round(n["translation"][2],3)
        
    if "rotation" in n:
        r_x = round(n["rotation"][0],3)
        r_y = round(n["rotation"][1],3)
        r_z = round(n["rotation"][2],3)
        
    if "scale" in n:
        s_x = round(n["scale"][0],3)
        s_y = round(n["scale"][1],3)
        s_z = round(n["scale"][2],3)

    if "name" in n:
        name = n["name"]
    
    if "extensions" in n:
        if "HUBS_components" in n["extensions"]:
            if "media" in n["extensions"]["HUBS_components"]:
                media_url = n["extensions"]["HUBS_components"]["media"]["src"]
                media_id  = n["extensions"]["HUBS_components"]["media"]["id"]

    new_uuid = uuid.uuid4()
    
    #room_id = 1 # TEMP, figure this out somehow, or just make it an arg?

    
    print("Translation:  " + str(t_x) + "  " + str(t_y) + "  " + str(t_z))
    print("Rotation:  " + str(r_x) + "  " + str(r_y) + "  " + str(r_z))
    print("Scale:  " + str(s_x) + "  " + str(s_y) + "  " + str(s_z))
    print("Media URL: " + media_url + " id " + media_id)

    query = "SELECT id FROM item WHERE name='" + name + "';"
    print(query)
    c.execute(query)
    rows = c.fetchall()
    if (len(rows)==0):
        query = "INSERT INTO item (name,uuid,room_id,media_id,media_url," + \
                "trans_x,trans_y,trans_z,rot_x,rot_y,rot_z,scale_x,scale_y,scale_z) " + \
                "VALUES ('" + name + "','" + str(new_uuid) + "'," + str(room_id) + \
                ",'" + media_id + "','" + media_url + "'," + \
                str(t_x) + "," + str(t_y) + "," + str(t_z) + "," + \
                str(r_x) + "," + str(r_y) + "," + str(r_z) + "," + \
                str(s_x) + "," + str(s_y) + "," + str(s_z) + ");"
        print(query)
        c.execute(query)


db.commit()

### Part two: open the existing spoke file, import the JSON, add new nodes to the tree, and save it again.

with open(spoke_filename, "r") as read_file:
    file_data = json.load(read_file)
    read_file.close()

with open(spoke_filename+ "_indent", "w") as write_file:
    json.dump(file_data, write_file, indent=4 )
    write_file.close()
    
    
root_uuid = file_data["root"]

num_ents = len(file_data["entities"])
for k in file_data["entities"]:
    last_key = k

last_index = file_data["entities"][last_key]["index"]
last_parent = file_data["entities"][last_key]["parent"]

print("entities: " + str(num_ents) + " last index: " + str(last_index) + " room UUID root: " + str(root_uuid))

query = "SELECT * FROM item WHERE room_id=" + str(room_id) + ";"
c.execute(query)
rows = c.fetchall()
for row in rows:
    item_uuid = row[1]
    name = row[2]
    media_url = row[3]
    media_id = row[4]
    t_x = row[5]
    t_y = row[6]
    t_z = row[7]
    r_x = row[8]
    r_y = row[9]
    r_z = row[10]
    s_x = row[11]
    s_y = row[12]
    s_z = row[13]
    print("Scale: " + str(s_x) + " " + str(s_y) + " " + str(s_z))
    last_index += 1

    file_data["entities"][str(item_uuid)] = { "name" : name }
    file_data["entities"][str(item_uuid)]["components"] = []
    file_data["entities"][str(item_uuid)]["components"].append({ "name": "transform"})
    file_data["entities"][str(item_uuid)]["components"][0]["props"] = {}
    file_data["entities"][str(item_uuid)]["components"][0]["props"]["position"] = {"x": t_x, "y": t_y, "z": t_z } 
    file_data["entities"][str(item_uuid)]["components"][0]["props"]["rotation"] = {"x": r_x, "y": r_y, "z": r_z } 
    file_data["entities"][str(item_uuid)]["components"][0]["props"]["scale"] = {"x": s_x, "y": s_y, "z": s_z } 

    file_data["entities"][str(item_uuid)]["components"].append({ "name": "visible"})
    file_data["entities"][str(item_uuid)]["components"][1]["props"] = {"visible": "true"}
    
    file_data["entities"][str(item_uuid)]["components"].append({ "name": "gltf-model"})
    file_data["entities"][str(item_uuid)]["components"][2]["props"] = {"src": media_url, "attribution": None}
    
    file_data["entities"][str(item_uuid)]["components"].append({ "name": "shadow"})
    file_data["entities"][str(item_uuid)]["components"][3]["props"] = {"cast": False, "receive": False}
    
    file_data["entities"][str(item_uuid)]["components"].append({ "name": "collidable"})
    file_data["entities"][str(item_uuid)]["components"][4]["props"] = {}
    
    file_data["entities"][str(item_uuid)]["components"].append({ "name": "walkable"})
    file_data["entities"][str(item_uuid)]["components"][5]["props"] = {}

    file_data["entities"][str(item_uuid)]["parent"] = str(root_uuid)
    file_data["entities"][str(item_uuid)]["index"] = last_index
    
with open(spoke_filename+ "_pins", "w") as write_file:
    json.dump(file_data, write_file, indent=4 )
    write_file.close()
    
db.close()

##########################################

#jsonString = "{ \"scenes\": [ ] }\n"


#query = "SELECT * FROM room;"
#c.execute(query)
#rows = c.fetchall()


#with open(spoke_filename, "w") as write_file:
#    json.dump(file_data, write_file, indent=4 )

#sample_data = {
#    "president": {
#        "name": "Zaphod Beeblebrox",
#        "species": "Betelgeusian"
#    }
#}

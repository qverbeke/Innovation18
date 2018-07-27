import csv, requests

#read file into list
with open("kb_log.csv") as csvfile:
    filereader = csv.reader(csvfile)
    data = [r for r in filereader]

#array to hold all feature variables
feature_array = []

#all feature variables
total_time = 0.0
char_per_min = 0.0
avg_depress = []
avg_time_between_keypresses = []
lshift_percent = 0.0
rshift_oercent = 0.0
capslock_percent = 0.0
correction_percent = 0.0
percent_bspace_held = 0.0
percent_bspace_notheld = 0.0
percent_delete_held = 0.0
percent_delete_notheld = 0.0

#for writer
ofile = open('pre-proccess.csv', 'w', newline ='')
writer = csv.writer(ofile, delimiter=',')

#get total length of typing period
num_chars = 0
for item in data:
    total_time += float(item[1])
    num_chars += 1

#get characters per minute
multiplier = 60 / total_time
char_per_min = num_chars * multiplier

feature_array.append(total_time)
feature_array.append(char_per_min)

row = []
row.append(total_time)
writer.writerow(row)
row = []
row.append(char_per_min)
writer.writerow(row)

#get average key depress time
depressdict = {}
depressdict['1'] = [0,0]
depressdict['2'] = [0,0]
depressdict['3'] = [0,0]
depressdict['4'] = [0,0]

iterdata = iter(data)
next(iterdata)
for item in iterdata:
    if item[0] == "1" or item[0] == "2" or item[0] == "3" or item[0] == "4":
        if item[3] == "Release":
            depressdict[item[0]][0]+=1
            depressdict[item[0]][1] += float(item[1])
        else:
            continue

avg_depress = []
for item in depressdict:
    if depressdict[item][0] != 0:
        avg_depress.append(depressdict[item][1] / depressdict[item][0])
    else:
        avg_depress.append(0)
        
writer.writerow(avg_depress)

#get average if there is no typing in a specific zone
zone_depress_count = 0
zone_depress_total_time = 0

for item in avg_depress:
    if item == 0:
        continue
    else:
        zone_depress_count += 1
        zone_depress_total_time += item

zone_depress_avg = zone_depress_total_time / zone_depress_count

for item in avg_depress:
    if item == 0:
        feature_array.append(zone_depress_avg)
    else:
        feature_array.append(item)


#Time Between Key Presses
#Dictionary: First number is number of key presses between a zone. Second number is total time between all key presses between a zone
dict = {}
dict['1-1'] = [0,0]
dict['1-2'] = [0,0]
dict['1-3'] = [0,0]
dict['1-4'] = [0,0]
dict['2-1'] = [0,0]
dict['2-2'] = [0,0]
dict['2-3'] = [0,0]
dict['2-4'] = [0,0]
dict['3-1'] = [0,0]
dict['3-2'] = [0,0]
dict['3-3'] = [0,0]
dict['3-4'] = [0,0]
dict['4-1'] = [0,0]
dict['4-2'] = [0,0]
dict['4-3'] = [0,0]
dict['4-4'] = [0,0]

#skip first two lines (not needed for this feature metric)
iterdata = iter(data)
next(iterdata)
next(iterdata)
previousvalue = data[1][0] + '-'
for item in iterdata:
    if item[0] == "1" or item[0] == "2" or item[0] == "3" or item[0] == "4":
        if item[3] == "Press":
            curvalue = item[0]
            try:
                dict[previousvalue + curvalue][1] = dict[previousvalue + curvalue][1] + float(item[1])
            except(KeyError):
                pass
        elif item[3] == "Release":
            continue
        try:
            dict[previousvalue + curvalue][0] = dict[previousvalue + curvalue][0] + 1
        except(KeyError):
            pass
        previousvalue = curvalue + '-'

#holds avg time between keypresses across zones in order the dictionary above is formatted
avg_time_between_keypresses = []        
for item in dict:
    if dict[item][0] != 0:
        avg_time_between_keypresses.append(dict[item][1] / dict[item][0])
    else:
        avg_time_between_keypresses.append(0)

#for feature array
atbk_count = 0
atbk_total_time = 0

for item in avg_time_between_keypresses:
    if item == 0:
        continue
    else:
        atbk_count += 1
        atbk_total_time += item

atbk_avg = atbk_total_time / atbk_count

for item in avg_time_between_keypresses:
    if item == 0:
        feature_array.append(atbk_avg)
    else:
        feature_array.append(item)




writer.writerow(avg_time_between_keypresses)

#Capitalization method
num_lshift = 0
num_rshift = 0
num_capslock = 0
lshift_percent = 0
rshift_percent = 0
capslock_percent = 0

for item in data:
    if item[0] == "Lshift":
        num_lshift += 1
    elif item[0] == "Rshift":
        num_rshift += 1
    elif item[0] == "Capital":
        num_capslock += 1

total_caps = num_lshift + num_rshift + num_capslock
if total_caps != 0: lshift_percent = num_lshift / total_caps
if total_caps != 0: rshift_percent = num_rshift / total_caps
if total_caps != 0: capslock_percent = num_capslock / total_caps

row = []
row.append(lshift_percent)
row.append(rshift_percent)
row.append(capslock_percent)
feature_array.append(lshift_percent)
feature_array.append(rshift_percent)
feature_array.append(capslock_percent)
writer.writerow(row)

#Correction percentage
num_backspace = 0
num_bspace_held = 0
num_bspace_notheld = 0
num_delete = 0
num_delete_held = 0
num_delete_notheld = 0
num_correction_keys = 0
num_pressed = 0
curvalue = "null"
for item in data:
    if item[0] == "Back":
        curvalue = "Back"
        if item[3] == "Press":
            num_pressed += 1
            continue
        elif item[3] == "Release":
            if num_pressed > 1:
                num_bspace_held += 1
                num_correction_keys += 1
                curvalue = "null"
                num_pressed = 0
            else:
                num_pressed = 0
                continue
    elif item[0] == "Delete":
        curvalue = "Delete"
        if item[3] == "Press":
            num_pressed += 1
            continue
        elif item[3] == "Release":
            if num_pressed > 1:
                num_delete_held += 1
                num_correction_keys += 1
                curvalue = "null"
                num_pressed = 0
            else:
                num_pressed = 0
                continue
    else:
        if curvalue == "Back":
            num_bspace_notheld += 1
            num_correction_keys += 1
            curvalue = "null"
        elif curvalue == "Delete":
            num_delete_notheld += 1
            num_correction_keys += 1
            curvalue = "null"

correction_percent = num_correction_keys / num_chars

row = []
row.append(correction_percent)
feature_array.append(correction_percent)
writer.writerow(row)

#Percent Correction Keys held/not held
num_backspace = num_bspace_held + num_bspace_notheld
num_delete = num_delete_held + num_delete_notheld

if num_backspace != 0: percent_bspace_held = num_bspace_held / num_backspace
if num_backspace != 0: percent_bspace_notheld = num_bspace_notheld / num_backspace
if num_delete != 0: percent_delete_held = num_delete_held / num_delete
if num_delete != 0: percent_delete_notheld = num_delete_notheld / num_delete

row = []
row.append(percent_bspace_held)
row.append(percent_bspace_notheld)
row.append(percent_delete_held)
row.append(percent_delete_notheld)
feature_array.append(percent_bspace_held)
feature_array.append(percent_bspace_notheld)
feature_array.append(percent_delete_held)
feature_array.append(percent_delete_notheld)
writer.writerow(row)

writer.writerow(feature_array)
print(feature_array)
requests.post("http://10.63.201.94:6969", data={"name":"Quinny","array": feature_array})

ofile.close()



    
    





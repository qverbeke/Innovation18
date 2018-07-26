import win32api, win32console, win32gui, pythoncom, pyHook, time, csv
#import tyler/quinns thing
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

#List of ascii values corresponding to their 'sector' on the keyboard
sector = {'81':'1','87':'1','69':'1','82':'1','84':'1','65':'1',
          '83':'1','68':'1','70':'1','71':'1','90':'2',
          '88':'2','67':'2','86':'2','72':'3','74':'3','75':'3',
          '76':'3','Oem_1':'3','80':'3','79':'3',
          '73':'3','85':'3','89':'3','Oem_Comma':'4','Oem_period':'4',
          '77':'4','78':'4','66':'4','Oem_2':'4','Oem_3':'4'}
num = {'1':'5','2':'5','3':'5','4':'5','5':'5','6':'5','7':'5','8':'5','9':'5','0':'5'}
          

row = '' #for the csv
#opening the CSV for adding new rows
ofile = open('kb_log.csv', 'w', newline ='')
writer = csv.writer(ofile, delimiter=',')

def OnKeyboardPress(event):
    row=[]
    #Global variables so we can tell time from key release and press        
    global writer,last_time
    #initial press time marked here
    temp = last_time
    last_time = time.time()
    #if the key is a letter
    if len(event.Key) == 1:
        #converts to ascii values from key name
        asc = ord(event.Key)
        asc = str(asc)
        try:
            #keeps track of the last sector pressed key and the next
            current_sect = num[event.Key]
            key="Num"
        except KeyError:
            asc = ord(event.Key)
            asc = str(asc)
            current_sect = sector[asc]
            key = "Asc"
    else:
        key = event.Key
        current_sect = event.Key
    row.append(current_sect)
    row.append(timeToKey(temp,last_time))
    row.append(key)
    row.append('Press')
    print(row)
    if timeToKey(temp,last_time) < 10.0:
        writer.writerow(row)
    else:
        ofile.close()
        writer = opener()
        print('Written to file.')
    return event.KeyID

def OnKeyboardRelease(event):
    print(event.Key)
    global last_sect,current_sect,ofile,writer,last_time
    temp = last_time
    last_time = time.time()
    row = []
    if len(event.Key) == 1:
        #converts to ascii values from key name
        asc = ord(event.Key)
        asc = str(asc)
        try:
            #keeps track of the last sector pressed key and the next
            current_sect = num[event.Key]
            key="Num"
        except KeyError:
            asc = ord(event.Key)
            asc = str(asc)
            current_sect = sector[asc]
            key = "Asc"
    else:
        key = event.Key
        current_sect = event.Key
    row.append(current_sect)
    row.append(timeToKey(temp,last_time))
    row.append(key)
    row.append("Release")
    print(row)
    writer.writerow(row)
    return event.KeyID

def timeToKey(start,end):
    return end-start

def opener():
    out = open('kb_log.csv', 'a', newline ='')
    return csv.writer(out, delimiter=',')
    
last_time = 0.0

if __name__ == '__main__':
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardPress
    hm.KeyUp = OnKeyboardRelease
    hm.HookKeyboard()
    pythoncom.PumpMessages()

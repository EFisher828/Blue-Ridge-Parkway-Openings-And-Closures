import urllib.request
import shapefile as shp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.patheffects as pe
import datetime
from datetime import datetime as dt
from bs4 import BeautifulSoup
from matplotlib import rcParams
rcParams['font.family'] = 'Century Gothic'

url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html,features='html.parser')

fullString = str(soup)

split1 = fullString.split('A listing of the open/closure status of gated road sections of the parkway. Arranged by Milepost from north to south on the parkway, and includes crossroads for reference.')
split2 = str(split1[2])
split3 = split2.split('\n</tbody>')
table = str(split3[0])

def splitIntoTRs():
    table1 = table.split('</tr>')

    Status = []
    Name = []
    count = 0
    for i in table1:
        if count > 0 and count < (len(table1)-2):
            divideTR = str(i).split('<p>')

            marker1 = str(divideTR[1])
            marker2 = marker1.split('</p>')
            marker = str(marker2[0])

            if len(marker) > 6:

                try:
                    print(divideTR[1])
                    status1 = str(divideTR[3])
                    status2 = status1.split('</p>')
                    status = str(status2[0])
                except:
                    Status.append('Open')

                try:
                    fix1 = status.split(' <br/>\n')
                    fix2 = str(fix1[1])
                    Status.append(fix2)
                    Name.append(name)
                except:
                    try:
                        fix1 = status.split(' ')
                        fix2 = str(fix1[1])
                        Status.append(fix2)
                        Name.append(name)
                    except:
                        Status.append(status)
            else:
                pass

        count = count + 1

    return Status

statusList = splitIntoTRs()
#statusList=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
locations = ['Richland Balsam','Black Balsam','Graveyard Fields','Mt. Pisgah','Craggy Gardens','Mt. Mitchell','Crabtree Falls','Moses Cone']
locationsIndex = [36,35,33,32,20,18,16,5]

print(statusList)
print(len(statusList))

file = open('NCshapeNames.txt')

fig = plt.figure(figsize=(11,7))
ax = plt.axes()
ax.axis('off')

def colorDecider(status):
    if status == 'Open':
        return '#72ef64'
    elif status == 'Closed':
        return '#ff1e2a'
    else:
        return '#72ef64'

    
sectionCount = 0
for line in file:
    sf = shp.Reader('nc-shapefiles/'+line[:-2])

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='{}'.format(colorDecider(statusList[sectionCount])), linewidth=9)
    sectionCount = sectionCount + 1

sf = shp.Reader('Blue Ridge Parkway Full.shp')

for shape in sf.shapeRecords():
    for i in range(len(shape.shape.parts)):
        i_start = shape.shape.parts[i]
        if i==len(shape.shape.parts)-1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[i+1]
        e = [i[0] for i in shape.shape.points[i_start:i_end]]
        f = [i[1] for i in shape.shape.points[i_start:i_end]]
        plt.plot(e,f, color='black', linewidth=0.7)

img = mpimg.imread('BRP NC Background.png')
imgplot = plt.imshow(img, extent=[-83.378,-80.877,35.192,36.598])

plt.xlim(-83.378,-80.877)
plt.ylim(35.192,36.598)

height = 0.36
locationsCount = 0
for l in locations: 
    fig.text(0.89,height,l,color='{}'.format(colorDecider(statusList[locationsIndex[locationsCount]])),size=15,ha='center',fontweight='bold')
    height = height - 0.04
    locationsCount = locationsCount + 1
fig.text(0.89,0.395,'Notable Locations',color='white',size=13,ha='center',fontstyle='italic',fontweight='bold')

rect = patches.Rectangle((-81.403, 35.201), 0.5, 0.58, linewidth=0, edgecolor='none', facecolor='#545454')
ax.add_patch(rect)

cityFile = open('NC Big Cities.csv')
csvCount = 0
for line in cityFile:
    if csvCount > 0:
        bigSplit = str(line).split(',')
        name = str(bigSplit[0])
        lon = eval(bigSplit[1])
        lat = eval(bigSplit[2])
        plt.text(lon,lat,name,fontstyle='italic',color='white',size=23,ha='center',fontweight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])
    else:
        pass
    csvCount = csvCount + 1

cityFile = open('NC Small Cities.csv')
csvCount = 0
for line in cityFile:
    if csvCount > 0:
        bigSplit = str(line).split(',')
        name = str(bigSplit[0])
        lon = eval(bigSplit[1])
        lat = eval(bigSplit[2])
        plt.text(lon,lat,name,fontstyle='italic',color='white',size=19,ha='center',fontweight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])
    else:
        pass
    csvCount = csvCount + 1

#Time Formatting and Placement
time = dt.strftime(dt.now(),"%b %d\n%I:%M %p")
fig.text(0.89,0.438,time,color='white',size=18,ha='center',weight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])

#Credit
fig.text(0.6,0.07,"Courtesy of @CarolinaWxGroup",color='white',size=16,ha='center',weight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

fig.savefig('output/BRP-Status-NC.png', dpi=200, bbox_inches='tight',pad_inches = 0)

#Virginia

statusList = []

split2 = str(split1[1])
split3 = split2.split('\n</tbody>')
table = str(split3[0])

statusList = splitIntoTRs()
#statusList=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
locations = ['Fancy Gap','Mabry Mill','Rocky Knob','Peaks of Otter','Apple Orch Mtn','Bluff Mtn','Ravens Roost','Humpback Rocks']
locationsIndex = [21,18,17,10,9,7,2,2]

print(statusList)
print(len(statusList))

file2 = open('VAshapeNames.txt')

fig = plt.figure(figsize=(11,7))
ax = plt.axes()
ax.axis('off')

def colorDecider(status):
    if status == 'Open':
        return '#72ef64'
    elif status == 'Closed':
        return '#ff1e2a'
    else:
        return '#72ef64'

    
sectionCount = 0
for line2 in file2:
    sf = shp.Reader('va-shapefiles/'+line2[:-2])

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='{}'.format(colorDecider(statusList[sectionCount-1])), linewidth=9)
    sectionCount = sectionCount + 1

sf = shp.Reader('Blue Ridge Parkway Full.shp')

for shape in sf.shapeRecords():
    for i in range(len(shape.shape.parts)):
        i_start = shape.shape.parts[i]
        if i==len(shape.shape.parts)-1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[i+1]
        e = [i[0] for i in shape.shape.points[i_start:i_end]]
        f = [i[1] for i in shape.shape.points[i_start:i_end]]
        plt.plot(e,f, color='black', linewidth=0.7)

img = mpimg.imread('BRP VA Background.png')
imgplot = plt.imshow(img, extent=[-81.681,-78.722,36.506,38.169])

plt.xlim(-81.681,-78.722)
plt.ylim(36.506,38.169)

height = 0.36
locationsCount = 0
for l in locations: 
    fig.text(0.89,height,l,color='{}'.format(colorDecider(statusList[locationsIndex[locationsCount]])),size=15,ha='center',fontweight='bold')
    height = height - 0.04
    locationsCount = locationsCount + 1
fig.text(0.89,0.395,'Notable Locations',color='white',size=13,ha='center',fontstyle='italic',fontweight='bold')

rect = patches.Rectangle((-79.34, 36.519), 0.578, 0.67, linewidth=0, edgecolor='none', facecolor='#545454')
ax.add_patch(rect)

cityFile = open('VA Big Cities.csv')
csvCount = 0
for line in cityFile:
    if csvCount > 0:
        bigSplit = str(line).split(',')
        name = str(bigSplit[0])
        lon = eval(bigSplit[1])
        lat = eval(bigSplit[2])
        plt.text(lon,lat,name,fontstyle='italic',color='white',size=23,ha='center',fontweight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])
    else:
        pass
    csvCount = csvCount + 1

cityFile = open('VA Small Cities.csv')
csvCount = 0
for line in cityFile:
    if csvCount > 0:
        bigSplit = str(line).split(',')
        name = str(bigSplit[0])
        lon = eval(bigSplit[1])
        lat = eval(bigSplit[2])
        plt.text(lon,lat,name,fontstyle='italic',color='white',size=19,ha='center',fontweight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])
    else:
        pass
    csvCount = csvCount + 1

#Time Formatting and Placement
time = dt.strftime(dt.now(),"%b %d\n%I:%M %p")
fig.text(0.89,0.43,time,color='white',size=18,ha='center',weight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])

#Credit
fig.text(0.6,0.07,"Courtesy of @CarolinaWxGroup",color='white',size=16,ha='center',weight='bold',path_effects=[pe.withStroke(linewidth=1, foreground="black")])

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

fig.savefig('output/BRP-Status-VA.png', dpi=200, bbox_inches='tight',pad_inches = 0)

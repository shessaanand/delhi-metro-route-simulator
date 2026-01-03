import time

def toMins(tStr):
    try:
        vals=tStr.split(":")
        if len(vals)!=2:
            return -1
        h=int(vals[0])
        m=int(vals[1])
        if h>23 or m>59:
            return -1
        return h*60+m
    except:
        return -1

def toStr(val):
    hr=val//60
    mn=val%60
    sHr=str(hr)
    sMn=str(mn)
    if len(sHr)==1:
        sHr="0"+sHr
    if len(sMn)==1:
        sMn="0"+sMn
    return sHr+":"+sMn

def isPeak(m):
    busy=False
    # Morning 8-10
    if m>=480 and m<600:
        busy=True
    # Evening 5-7
    if m>=1020 and m<1140:
        busy=True
    if busy:
        return 4
    else:
        return 8

def getSched(tStr):
    curr=toMins(tStr)
    if curr==-1:
        return None
    end=1380
    if curr>=end:
        return None
    lst=[]
    arr=0
    start=360
    if curr<start:
        arr=start
    else:
        gap=isPeak(curr)
        rem=curr%gap
        wait=gap-rem
        if wait==gap:
            wait=0
        arr=curr+wait
    for k in range(4):
        lst.append(toStr(arr))
        gap=isPeak(arr)
        arr=arr+gap
    return lst

def nextTrain(tStr):
    lst=getSched(tStr)
    if lst==None:
        return None
    return lst[0]

def calcFare(mins, day):
    # Check if it is Sunday or Holiday
    isSun=False
    d=day.lower()
    if "sun" in d or "holiday" in d:
        isSun=True

    if isSun:
        # Discounted Fares (Sunday/Holiday)
        if mins<=5:
            return 11
        elif mins<=12:
            return 11
        elif mins<=25:
            return 21
        elif mins<=45:
            return 32
        elif mins<=65:
            return 43
        else:
            return 54
    else:
        # Standard Fares (Mon-Sat)
        if mins<=5:
            return 11
        elif mins<=12:
            return 21
        elif mins<=25:
            return 32
        elif mins<=45:
            return 43
        elif mins<=65:
            return 54
        else:
            return 64

def readData():
    path="metro_data.txt"
    f=open(path,"r")
    raw=f.readlines()
    f.close()
    db=[]
    for row in raw:
        clean=row.strip()
        parts=clean.split(",")
        item=[]
        for i in parts:
            item.append(i.strip())
        if len(item)>=5:
            if item[0]!="Line":
                ln=item[0].lower()
                u=item[1].lower()
                v=item[2].lower()
                tm=int(item[3])
                r1=[u,v,tm,ln]
                db.append(r1)
                r2=[v,u,tm,ln]
                db.append(r2)
    return db

def findPath(db,src,dst):
    q=[]
    start=[[0,0],[src],""]
    q.append(start)
    vis={}
    while len(q)>0:
        q.sort()
        curr=q.pop(0)
        cost=curr[0]
        cTr=cost[0]
        cTm=cost[1]
        cPath=curr[1]
        cLn=curr[2]
        here=cPath[-1]
        if here==dst:
            return cPath
        key=here+cLn
        skip=False
        if key in vis:
            old=vis[key]
            if old[0]<cTr:
                skip=True
            elif old[0]==cTr and old[1]<=cTm:
                skip=True
        if skip:
            continue
        vis[key]=[cTr,cTm]
        for r in db:
            if r[0]==here:
                nTr=cTr
                pen=0
                if cLn!="" and cLn!=r[3]:
                    nTr+=1
                    pen=12
                nTm=cTm+r[2]+pen
                newP=[]
                for s in cPath:
                    newP.append(s)
                newP.append(r[1])
                pkg=[[nTr,nTm],newP,r[3]]
                q.append(pkg)
    return None

def showTime(db):
    ln=input("Enter line name: ").strip().lower()
    st=input("Enter station name: ").strip().lower()
    tm=input("Enter current time (HH:MM): ").strip()
    ok=False
    for r in db:
        if r[3]==ln:
            if r[0]==st:
                ok=True
            if r[1]==st:
                ok=True
    if ok:
        res=getSched(tm)
        if res:
            print("Next metro at "+res[0])
            s=""
            for i in range(1,len(res)):
                s+=res[i]+", "
            print("Subsequent metros at: "+s[:-2])
        else:
            print("Invalid time or metro closed.")
    else:
        print("Invalid line or station.")

def doPlan(data):
    src=input("Enter source station: ").strip().lower()
    dest=input("Enter destination station: ").strip().lower()
    timeIn=input("Enter current time (HH:MM): ").strip()
    dayIn=input("Enter Day (Mon/Sun): ").strip()
    srcValid=False
    destValid=False
    for row in data:
        if row[0]==src:
            srcValid=True
        if row[0]==dest:
            destValid=True
    if not srcValid or not destValid:
        print("Invalid stations.")
        return
    path=findPath(data,src,dest)
    if not path:
        print("No path found.")
        return
    print("Journey Plan:")
    nextT=nextTrain(timeIn)
    if not nextT:
        print("Invalid time or metro closed.")
        return
    print("Next metro at "+nextT)
    currMins=toMins(nextT)
    startMins=currMins
    currLine=""
    pathLen=len(path)
    for i in range(pathLen - 1):
        stnA=path[i]
        stnB=path[i+1]
        travelT=0
        travelL=""
        for row in data:
            if row[0]==stnA:
                if row[1]==stnB:
                    travelT=row[2]
                    travelL=row[3]
                    break
        if currLine!="" and currLine != travelL:
            arrTime=toStr(currMins)
            depTime=nextTrain(arrTime)
            print("Transfer to "+travelL+" at "+stnA+". Next train leaves "+depTime)
            currMins=toMins(depTime)
        currMins+=travelT
        currLine=travelL
        print("Arrive at "+stnB+" at "+toStr(currMins))
    totalMins=currMins-startMins
    print("Total time: "+str(totalMins)+" mins")
    fare=calcFare(totalMins,dayIn)
    print("Estimated Fare: Rs. "+str(fare))

def showStns(data):
    lineName=input("Enter line name: ").strip().lower()
    stations=[]
    isFound=False
    for row in data:
        if row[3]==lineName:
            isFound=True
            if row[0] not in stations:
                stations.append(row[0])
            if row[1] not in stations:
                stations.append(row[1])
    if isFound:
        stations.sort()
        print("--- Stations on "+lineName+" line ---")
        for stn in stations:
            print(stn)
    else:
        print("Line not found.")

def runApp():
    try:
        db=readData()
    except:
        print("Error: File not found.")
        return
    while True:
        print("======================================================")
        print("WELCOME TO THE DELHI METRO ROUTE AND SCHEDULE SIMULATOR")
        print("======================================================")
        print("Type the following numbers to choose the following options (1-4)")
        print("1. Metro Timings Module")
        print("2. Ride Journey Planner")
        print("3. All Stations Viewer as per Line")
        print("4. Exit")
        ch=input("Enter choice: ").strip()
        if ch=="1":
            showTime(db)
        elif ch=="2":
            doPlan(db)
        elif ch=="3":
            showStns(db)
        elif ch=="4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
        print("")

runApp()

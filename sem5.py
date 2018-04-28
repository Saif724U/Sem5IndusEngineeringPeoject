import math
#all in radians
def movement():
	axisproper=calibaxis()
	#angles=getangle(axisproper[0],axisproper[1],axisproper[2],[1,2,3])
	changematrix=getchangebasismatrix([[1,0,0],[0,1,0],[0,0,1]],axisproper)
	count=0	
	grama=[1,2,3]
	while(count < 4):	
		angles=multpspec(changematrix,grama,[0,0,0])	
		print str(count)+". angles --> "		
		print (angles)
		#now the device has rotatedby 3 radians in z, 2 in y, 1 in x
		temp=multp([[math.cos(3),-math.sin(3),0],[math.sin(3),math.cos(3),0],[0,0,1]],[[math.cos(2),0,math.sin(2)],[0,1,0],[-math.sin(2),0,math.cos(2)]],[[0,0,0],[0,0,0],[0,0,0]])
		temp1=multp(temp,[[1,0,0],[0,math.cos(1),-math.sin(1)],[0,math.sin(1),math.cos(1)]],[[0,0,0],[0,0,0],[0,0,0]])
		axisproper=multp(temp1,axisproper,[[0,0,0],[0,0,0],[0,0,0]])
		grama=multpspec(temp1,grama,[0,0,0])
		changematrix=getchangebasismatrix([[1,0,0],[0,1,0],[0,0,1]],axisproper)
		count+=1
		
def calibaxis():
	#sending 1,2,3 as start
	verticalaxis=getaxis(1,2,3)
	print "Vertical Axis --> "
	print(verticalaxis)
	#sending 4,5,6 as movement	
	horizontalaxis=getaxis(4-verticalaxis[0],5-verticalaxis[1],6-verticalaxis[2])
	print "Horizontal Axis --> "
	print(horizontalaxis)
	#calc other axis
	sudoperpaxis=cross(horizontalaxis,verticalaxis)	
	perpaxis=getaxis(sudoperpaxis[0],sudoperpaxis[1],sudoperpaxis[2])
	print "Perpendicular Axis --> "
	print(perpaxis)
	resultaxis=[verticalaxis,horizontalaxis,perpaxis]
	return resultaxis
	

def getaxis(i,j,k):
	magn=((i**(2))+(j**(2))+(k**(2)))**(0.5)
	downaxisX=i/magn
	downaxisY=j/magn
	downaxisZ=k/magn			
	axisArr=[downaxisX,downaxisY,downaxisZ]	
	return axisArr

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c
	
def dot(a,b):
	return ((a[0]*b[0])+(a[1]*b[1])+(a[2]*b[2]))

def magn(a):
	return ((a[0]**2)+(a[1]**2)+(a[2]**2))**(0.5)

def getangle(a1,a2,a3,r):
	vertang=math.acos(dot(a1,r)/(magn(a1)*magn(r)))
	horizontalang=math.acos(dot(a2,r)/(magn(a2)*magn(r)))
	perpang=math.acos(dot(a3,r)/(magn(a3)*magn(r)))
	angles=[vertang,horizontalang,perpang]	
	return angles 

###############################inverting matrices################################

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

###################################end of inverting matrices#####################

##multiplying matrices



def multp(X,Y,result):
	for i in range(len(X)):
		# iterate through columns of Y
		for j in range(len(Y[0])):
       			# iterate through rows of Y
       			for k in range(len(Y)):
           			result[i][j] += X[i][k] * Y[k][j]
	return result
	
def multpspec(X,Y,result):
	for i in range(len(X)):
		for j in range(len(Y)):
			result[i]+=X[i][j]*Y[j]
	return result

#change basis from x to y
def getchangebasismatrix(x,y):
	result=multp(getMatrixInverse(y),x,[[0,0,0],[0,0,0],[0,0,0]])
	return result


movement()

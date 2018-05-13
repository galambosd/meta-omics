library('rPython')

python.load('test.py')

a <- c(5,4,3)
b<- c(4,5,6)

c<-python.call("test",a,b)
print(c)

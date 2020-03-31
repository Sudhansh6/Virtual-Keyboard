## Some important code packets relating to various conepts

### Using Default parameters 
```python
def fun1(a,l=[]):
	l.append(a)
	return l

def fun2(a,l=None):
	if l is None: #you can use l==None too
		l=[]
	l.append(a)
	return l
  
print(fun1(3))
print(fun1(5))
print(fun2(3))
print(fun2(5))
  ```
### Using variable number of parameters
``` python
def variable_arg(*arg):
	for x in arg:
		print(x)

def variable_kwrds(**kwrds):
	for name, value in kwrds.items():
		print(name,":", value)
    
a1,a2,a3=[1,2,3,4],{'lock':'key','up':'down'},[]   
variable_arg(1,"a")
variable_arg(*a1,5,6)
variable_arg(a1,67)
variable_kwrds(a='apple',b='ball',**a2) #doesnt work without **
    ```

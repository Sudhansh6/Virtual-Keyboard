## Some important code packets relating to various concepts

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
> Output:  
```
[3]  
[3,5]  
[3]  
[5]
```
 
### Using variable number of parameters
``` python
def variable_arg(*arg):
	for x in arg:
		print(x)

def variable_kwrds(**kwrds):
	for name, value in kwrds.items():
		print(name," : ", value)
    
a1,a2,a3=[1,2],{'lock':'key','up':'down'},[]   
variable_arg(1,"a")
variable_arg(*a1,5,6)
variable_arg(a1,67)
variable_kwrds(a='apple',b='ball',**a2) #doesnt work without **
   ```
 > Output:  
``` 
 1  
 a  
 1  
 2  
 5  
 6  
 [1,2]  
 67  
 a : apple  
 b : ball  
 lock : key  
 up : down 
 ``` 
 
### Documentation
```python
def my_function():
     """Do nothing, but document it.

     No, really, it doesn't do anything.
    """
    pass
print(my_function.__doc__)
```
>Output:  
```
Do nothing, but document it. 
	No, really it doesn't do anything.
```
	
    

## Coding Conventions
- Use 4-space indentation, and no tabs.  
4 spaces are a good compromise between small indentation (allows greater nesting depth) and large indentation (easier to read). Tabs introduce confusion, and are best left out.
- Wrap lines so that they don’t exceed 79 characters.  
This helps users with small displays and makes it possible to have several code files side-by-side on larger displays.
- Use blank lines to separate functions and classes, and larger blocks of code inside functions.
When possible, put comments on a line of their own.
- Use docstrings.
- Use spaces around operators and after commas, but not directly inside bracketing constructs: a = f(1, 2) + g(3, 4).
- Name your classes and functions consistently; the convention is to use UpperCamelCase for classes and lowercase_with_underscores for functions and methods. Always use self as the name for the first method argument.

## Important points
- `a.append(b)` is less efficient than `a = a + [b]`.
- `del` can be used to delete elements in a list.
- `list(zip(*matrix))` can be used to append a matrix to a list. 
- reversed(list) can be used to iterate through a list in reverse direction.
- sorted(set) returns sorted set without altering the original set.
- Comparisons can be chained (**and** between the condiions).
- When sequences are compared, it is done in lexicographic order.

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
> Output :  
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
 > Output :  
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
Documentation can be used to describe the role of a function. In other words, it can be used to mention what the function does with the input and what it returns as the output.  
These Documentation Strings are stored in \_\_doc\_\_ and can be accessed by `function_name.__doc__`    
```python
def my_function():
     """Do nothing, but document it.

     No, really, it doesn't do anything.
    """
    pass
print(my_function.__doc__)
```
>Output :  
```
Do nothing, but document it. 
	No, really it doesn't do anything.
```

### Function Annotations
```python
def f(ham: str, eggs: str = 'eggs') -> str:
     print("Annotations:", f.__annotations__)
     print("Arguments:", ham, eggs)
     return ham + ' and ' + eggs
f('spam')
```
>Output :
```
Annotations: {'ham': <class 'str'>, 'return': <class 'str'>, 'eggs': <class 'str'>}
Arguments: spam eggs
'spam and eggs'
```
---
## Concepts
- ### Lists and inbuilt functions ``[]``
	Lists can be modified and used as Stacks, Queues, Matrices and other Data structures. Lists are very similar to strings (indexing,slicing,delete,mutable etc..)
	- `list.append(x)`  
	Add an item to the end of the list. Equivalent to a[len(a):] = [x].  
	- `list.extend(iterable)`  
	Extend the list by appending all the items from the iterable. Equivalent to a[len(a):] = iterable.  
	- `list.insert(i, x)`  
	Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x).  
	- `list.remove(x)`  
	Remove the first item from the list whose value is equal to x. It raises a ValueError if there is no such item.  
	- `list.pop([i])`  
	Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. (The square brackets around the i in the method signature denote that the parameter is optional, not that you should type square brackets at that position. You will see this notation frequently in the Python Library Reference.)  
	- `list.clear()`  
	Remove all items from the list. Equivalent to del a[:].  
	- `list.index(x[, start[, end]])`  
	Return zero-based index in the list of the first item whose value is equal to x. Raises a ValueError if there is no such item.
	The optional arguments start and end are interpreted as in the slice notation and are used to limit the search to a particular subsequence of the list. The returned index is computed relative to the beginning of the full sequence rather than the start argument.  
	- `list.count(x)`  
	Return the number of times x appears in the list.  
	- `list.sort(key=None, reverse=False)`  
	Sort the items of the list in place 
	- `list.reverse()`  
	Reverse the elements of the list in place. 
	- `list.copy()`  
	Return a shallow copy of the list. Equivalent to a[:].  
	- **`list(zip(*matrix))`**  
	This can be used to append a higher dimension list to another.
	- **`del a[[start]:[end]]
	Used to delete some elements in a list.

- ### [Shallow copy and Deep copy](https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/)
- ### Tuples  ``()``
	A tuple consists of a number of values separated by commas. They are immutable but they can contain mutable objects.
	- To create a singleton tuple, the following can be done,  
	` t= 'apple',`
	- Sequence unpacking can be achieved in the following manner,  
	```python
	t=1,2,3
	a,b,c =t
	print(b,c,a)
	```
	>Output :  
	``` 2 3 1 ```  
	
- ### Sets  ``{}``
	Sets are unordered (No indexing) sequences with no suplicate entries. Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union(`a|b`), intersection(`a&b`), difference(`a-b`), and symmetric difference(`a^b`).  
	- This can be done in case of lists and sets (**NEW SYNTAX**)
	```python
	a = {x for x in 'abracadabra' if x not in 'abc'}
	print(a)
	```
	>Output :  
	``` {'r','d'} ```
- ### Dictionaries ``{ : , : }``
	Dictionary is a *set* of key value pairs. Keys function as indexes for dictionaries.
	- Iterating through a dictionary \-
	```python
	knights = {'gallahad': 'the pure', 'robin': 'the brave'}
	for k, v in knights.items():
    		print(k, v)
   	 ```
    > Output :
    ``` 
    gallahad the pure 
    robin the brave
    ```
   -
   ```python
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):
       print('What is your {0}?  It is {1}.'.format(q, a))
     ```

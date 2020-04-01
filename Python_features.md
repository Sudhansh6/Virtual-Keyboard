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
- Use `write()` (similar to `print()`) to write into a file.
- Use `str()` and `repr()` to convert stuff(even tuples) into strings(`repr()` prints string quotes and backslashes too).
- !s,!r,!a, : can be used with string literals.
- positionals and keywords are applicable in string formatting literals(`str.format()`).
- `f = open ('file_name','w')` r - reading, w -writing, a - appending, r+ - reading and writing, b - binary, r is assumed if void.
- You can loop over lines in a file using `for line in f: `. You can also use `list(f)` or `f.readLines()` to read all lines.
- `f.write(string)` writes the contents of string to the file, returning the number of characters written.
- `f.tell()` returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.
- To change the file object’s position, use f.seek(offset, whence). The position is computed from adding offset to a reference point; the reference point is selected by the whence argument. A whence value of 0 measures from the beginning of the file, 1 uses the current file position, and 2 uses the end of the file as the reference point. whence can be omitted and defaults to 0, using the beginning of the file as the reference point.
- Python supports nested functions.


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
### Formatted string literals
To use formatted string literals, begin a string with f or F before the opening quotation mark or triple quotation mark. Inside this string, you can write a Python expression between { and } characters that can refer to variables or literal values.
1. ```python
	year = 2016
	event = 'Referendum'
	f'Results of the {year} {event}'
	```
	> Output :  
	```
	'Results of the 2016 Referendum'
	```
2. ```python
	yes_votes = 42_572_654
	no_votes = 43_132_495
	percentage = yes_votes / (yes_votes + no_votes)
	'{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)
	```
	>Output : 
	``` ' 42572654 YES votes  49.67%' ```
### File reading 
1.	```python
	with open('workfile') as f:
	    read_data = f.read()

	# We can check that the file has been automatically closed.
	f.closed
	```
	> Output :  
	``` True ```
2.	```python
	f.read()
	f.read()
	```
	> Output :  
	```
	' This is the entire file.\n'
	''
	```
3.	```python
	f.readline()
	f.readline()
	f.readline()
	```
	> Output : 
	```
	'This is the first line.\n'
	'Second line.\n'
	''
	```
### Exception Handling
1.	```python
	while True:
	    try:
		x = int(input("Please enter a number: "))
		break
	    except ValueError:
		print("Oops!  That was no valid number.  Try again...")
	```
2. 	```python
	except (RuntimeError, TypeError, NameError):
	pass
	```
3. >
	```python
	class B(Exception):
	    pass
	class C(B):
	    pass
	class D(C):
	    pass

	for cls in [B, C, D]:
	    try:
		raise cls()
	    except D:
		print("D")
	    except C:
		print("C")
	    except B:
		print("B")
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
 - ### [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

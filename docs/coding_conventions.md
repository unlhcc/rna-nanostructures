# Coding Conventions and Styles

## [Python](https://www.python.org/dev/peps/pep-0008/)

### Naming

- Variables: lowercase underscore: `variable_name =`
- Global Variables: double undersore: `__global_var__ =`
- Functions: lowercase underscore: `def func_hello:`
- Class Names: CapCase: `ClassName:`

### Indentation & Commenting
```python

# Block comments
# Lets us use multiple lines
def function:
  x = 1   
  if x == 5: # inline comment
    print("hello")
  return x
```

### Programming Recommendations
- Don't compare boolean values to True or False using ==

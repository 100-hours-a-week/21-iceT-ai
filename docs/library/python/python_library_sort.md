# `Sorting` Techniques

Python lists have a built-in `list.sort()` method that modifies the list
in-place. There is also a `sorted()` built-in function that builds a new
sorted list from an iterable.
In this document, we explore the various techniques for sorting data using Python.

## Sorting Basics

A simple ascending sort is very easy: just call the `sorted()` function. It
returns a new sorted list:

```python
>>> sorted([5, 2, 3, 1, 4])
[1, 2, 3, 4, 5]

```

You can also use the `list.sort()` method. It modifies the list
in-place (and returns `None` to avoid confusion). Usually it’s less convenient
than `sorted()` - but if you don’t need the original list, it’s slightly
more efficient.

```python
>>> a = [5, 2, 3, 1, 4]
>>> a.sort()
>>> a
[1, 2, 3, 4, 5]
```

Another difference is that the `list.sort()` method is only defined for
lists. In contrast, the `sorted()` function accepts any iterable.

```python
>>> sorted({1: 'D', 2: 'B', 3: 'B', 4: 'E', 5: 'A'})
[1, 2, 3, 4, 5]

```




## Key Functions

Both `list.sort()` and `sorted()` have a *key* parameter to specify a
function (or other callable) to be called on each list element prior to making
comparisons.
For example, here’s a case-insensitive string comparison:

```python
>>> sorted("This is a test string from Andrew".split(), key=str.casefold)
['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']

```

The value of the *key* parameter should be a function (or other callable) that
takes a single argument and returns a key to use for sorting purposes. This
technique is fast because the key function is called exactly once for each
input record.
A common pattern is to sort complex objects using some of the object’s indices
as keys. For example:

```python
>>> student\_tuples = [
...     ('john', 'A', 15),
...     ('jane', 'B', 12),
...     ('dave', 'B', 10),
... ]
>>> sorted(student\_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

```
The same technique works for objects with named attributes. For example:

```python
>>> class Student:
...     def \_\_init\_\_(self, name, grade, age):
...         self.name = name
...         self.grade = grade
...         self.age = age
...     def \_\_repr\_\_(self):
...         return repr((self.name, self.grade, self.age))

>>> student\_objects = [
...     Student('john', 'A', 15),
...     Student('jane', 'B', 12),
...     Student('dave', 'B', 10),
... ]
>>> sorted(student\_objects, key=lambda student: student.age)   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

```
Objects with named attributes can be made by a regular class as shown
above, or they can be instances of `dataclass` or
a named tuple.




## Operator Module Functions and Partial Function Evaluation

The key function patterns shown above are very common, so Python provides
convenience functions to make accessor functions easier and faster. The
`operator` module has `itemgetter()`,
`attrgetter()`, and a `methodcaller()` function.

Using those functions, the above examples become simpler and faster:

```python
>>> from operator import itemgetter, attrgetter

>>> sorted(student\_tuples, key=itemgetter(2))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

>>> sorted(student\_objects, key=attrgetter('age'))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```

The operator module functions allow multiple levels of sorting. For example, to
sort by *grade* then by *age*:

```python
>>> sorted(student\_tuples, key=itemgetter(1,2))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

>>> sorted(student\_objects, key=attrgetter('grade', 'age'))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
```

The `functools` module provides another helpful tool for making
key-functions. The `partial()` function can reduce the
arity of a multi-argument
function making it suitable for use as a key-function.

```python
>>> from functools import partial
>>> from unicodedata import normalize

>>> names = 'Zoë Åbjørn Núñez Élana Zeke Abe Nubia Eloise'.split()

>>> sorted(names, key=partial(normalize, 'NFD'))
['Abe', 'Åbjørn', 'Eloise', 'Élana', 'Nubia', 'Núñez', 'Zeke', 'Zoë']

>>> sorted(names, key=partial(normalize, 'NFC'))
['Abe', 'Eloise', 'Nubia', 'Núñez', 'Zeke', 'Zoë', 'Åbjørn', 'Élana']
```




## Ascending and Descending

Both `list.sort()` and `sorted()` accept a *reverse* parameter with a
boolean value. This is used to flag descending sorts. For example, to get the
student data in reverse *age* order:

```python
>>> sorted(student\_tuples, key=itemgetter(2), reverse=True)
[('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

>>> sorted(student\_objects, key=attrgetter('age'), reverse=True)
[('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
```

## Sort Stability and Complex Sorts

Sorts are guaranteed to be stable. That means that
when multiple records have the same key, their original order is preserved.

```python
>>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
>>> sorted(data, key=itemgetter(0))
[('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]
```

Notice how the two records for *blue* retain their original order so that
`('blue', 1)` is guaranteed to precede `('blue', 2)`.

This wonderful property lets you build complex sorts in a series of sorting
steps. For example, to sort the student data by descending *grade* and then
ascending *age*, do the *age* sort first and then sort again using *grade*:

```python
>>> s = sorted(student\_objects, key=attrgetter('age'))     # sort on secondary key
>>> sorted(s, key=attrgetter('grade'), reverse=True)       # now sort on primary key, descending
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```

This can be abstracted out into a wrapper function that can take a list and
tuples of field and order to sort them on multiple passes.

```python
>>> def multisort(xs, specs):
...     for key, reverse in reversed(specs):
...         xs.sort(key=attrgetter(key), reverse=reverse)
...     return xs

>>> multisort(list(student\_objects), (('grade', True), ('age', False)))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```

The Timsort algorithm used in Python
does multiple sorts efficiently because it can take advantage of any ordering
already present in a dataset.



## Decorate-Sort-Undecorate

This idiom is called Decorate-Sort-Undecorate after its three steps:

* First, the initial list is decorated with new values that control the sort order.
* Second, the decorated list is sorted.
* Finally, the decorations are removed, creating a list that contains only the
initial values in the new order.

For example, to sort the student data by *grade* using the DSU approach:

```python
>>> decorated = [(student.grade, i, student) for i, student in enumerate(student\_objects)]
>>> decorated.sort()
>>> [student for grade, i, student in decorated]               # undecorate
[('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
```

This idiom works because tuples are compared lexicographically; the first items
are compared; if they are the same then the second items are compared, and so
on.

It is not strictly necessary in all cases to include the index *i* in the
decorated list, but including it gives two benefits:

* The sort is stable – if two items have the same key, their order will be
preserved in the sorted list.
* The original items do not have to be comparable because the ordering of the
decorated tuples will be determined by at most the first two items. So for
example the original list could contain complex numbers which cannot be sorted
directly.




## Comparison Functions

Unlike key functions that return an absolute value for sorting, a comparison
function computes the relative ordering for two inputs.

For example, a balance scale
compares two samples giving a relative ordering: lighter, equal, or heavier.
Likewise, a comparison function such as `cmp(a, b)` will return a negative
value for less-than, zero if the inputs are equal, or a positive value for
greater-than.

It is common to encounter comparison functions when translating algorithms from
other languages. Also, some libraries provide comparison functions as part of
their API. For example, `locale.strcoll()` is a comparison function.

To accommodate those situations, Python provides
`functools.cmp\_to\_key` to wrap the comparison function
to make it usable as a key function:

```python
sorted(words, key=cmp\_to\_key(strcoll))  # locale-aware sort order
```






## Partial Sorts

Some applications require only some of the data to be ordered. The standard
library provides several tools that do less work than a full sort:

* `min()` and `max()` return the smallest and largest values,
respectively. These functions make a single pass over the input data and
require almost no auxiliary memory.

* `heapq.nsmallest()` and `heapq.nlargest()` return
the *n* smallest and largest values, respectively. These functions
make a single pass over the data keeping only *n* elements in memory
at a time. For values of *n* that are small relative to the number of
inputs, these functions make far fewer comparisons than a full sort.

* `heapq.heappush()` and `heapq.heappop()` create and maintain a
partially sorted arrangement of data that keeps the smallest element
at position `0`. These functions are suitable for implementing
priority queues which are commonly used for task scheduling.








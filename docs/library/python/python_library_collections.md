# `collections` – Container datatypes

This module implements specialized container datatypes providing alternatives to Python’s general purpose built-in containers:

| Name         | Description                                                       |
| ------------ | ----------------------------------------------------------------- |
| `deque`      | List-like container with fast appends and pops on either end      |
| `Counter`    | Dict subclass for counting hashable objects                       |
| `OrderedDict`| Dict subclass that remembers the order entries were added         |
| `defaultdict`| Dict subclass that calls a factory function to supply missing values |


### Counter objects

A counter tool is provided to support convenient and rapid tallies. For example:

```python
# Tally occurrences of words in a list
>>> cnt = Counter()
>>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
...     cnt[word] += 1
...
>>> cnt
Counter({'blue': 3, 'red': 2, 'green': 1})

# Find the ten most common words in Hamlet
>>> import re
>>> words = re.findall(r'\w+', open('hamlet.txt').read().lower())
>>> Counter(words).most_common(10)
[('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631),
 ('you', 554), ('a', 546), ('my', 514), ('hamlet', 471), ('in', 451)]
```

```python
class Counter([iterable-or-mapping])
```

A `Counter` is a `dict` subclass for counting hashable objects. Elements are stored as keys and their counts as values. Counts may be zero or negative.

Create from an iterable or mapping:

```python
>>> c = Counter()                           # empty counter
>>> c = Counter('gallahad')                 # from iterable
>>> c = Counter({'red': 4, 'blue': 2})      # from mapping
>>> c = Counter(cats=4, dogs=8)             # from kwargs
```

Missing keys return zero instead of raising `KeyError`:

```python
>>> c = Counter(['eggs', 'ham'])
>>> c['bacon']
0
```

To remove an element entirely, use `del`:

```python
>>> c['sausage'] = 0
>>> del c['sausage']
```

**Added in version 3.1.**  
**Changed in version 3.7:** Inherits insertion order; math operations preserve order.

#### Additional methods

- `elements()`: Iterator repeating each element as many times as its count; ignores counts < 1.
- `most_common([n])`: List of the n most common elements and counts.
- `subtract([iterable-or-mapping])`: Subtract counts from another container.
- `total()`: Sum of all counts.

#### Examples

```python
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> sorted(c.elements())
['a', 'a', 'a', 'a', 'b', 'b']

>>> Counter('abracadabra').most_common(3)
[('a', 5), ('b', 2), ('r', 2)]

>>> c.subtract(Counter(a=1, b=2, c=3, d=4))
>>> c
Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})

>>> Counter(a=10, b=5, c=0).total()
15
```

#### Mathematical operations

```python
>>> c = Counter(a=3, b=1)
>>> d = Counter(a=1, b=2)
>>> c + d      # addition
Counter({'a': 4, 'b': 3})
>>> c - d      # subtraction (only positive counts)
Counter({'a': 2})
>>> c & d      # intersection (min)
Counter({'a': 1, 'b': 1})
>>> c | d      # union (max)
Counter({'a': 3, 'b': 2})
>>> +c         # remove zero and negative
Counter({'a': 3, 'b': 1})
>>> -c         # invert sign, then remove non-positive
Counter({'b': 4})
```

---

### deque objects

```python
class deque([iterable[, maxlen]])
```

Returns a new deque initialised left-to-right from `iterable`. If `maxlen` is set, the deque is bounded: appends cause pops on the opposite end.

Deques support thread-safe, memory-efficient appends and pops from either side in O(1) time.

#### Methods

- `append(x)`, `appendleft(x)`
- `pop()`, `popleft()`
- `extend(iterable)`, `extendleft(iterable)`
- `insert(i, x)` (v3.5)
- `remove(value)`, `clear()`
- `count(x)` (v3.2), `copy()` (v3.5)
- `reverse()` (v3.2), `rotate(n=1)`

Attribute:

- `maxlen`: maximum size or `None`.

#### Example

```python
>>> from collections import deque
>>> d = deque('ghi')
>>> d.append('j')
>>> d.appendleft('f')
>>> d
deque(['f', 'g', 'h', 'i', 'j'])
>>> d.rotate(1)
>>> d
deque(['j', 'f', 'g', 'h', 'i'])
```

#### Recipes

- **Tail filter**:

  ```python
  def tail(filename, n=10):
      return deque(open(filename), n)
  ```

- **Moving average**:

  ```python
  import itertools
  def moving_average(it, n=3):
      it = iter(it)
      d = deque(itertools.islice(it, n-1))
      d.appendleft(0)
      s = sum(d)
      for x in it:
          s += x - d.popleft()
          d.append(x)
          yield s / n
  ```

- **Round-robin scheduler**:

  ```python
  def roundrobin(*iterables):
      iters = deque(map(iter, iterables))
      while iters:
          try:
              while True:
                  yield next(iters[0])
                  iters.rotate(-1)
          except StopIteration:
              iters.popleft()
  ```

---

### defaultdict objects

```python
class defaultdict(default_factory=None, /, *args, **kwargs)
```

Like a `dict` but calls `default_factory()` to supply missing values on `__getitem__`.

- `default_factory`: called when a missing key is accessed.
- Does not affect methods like `get()`—they return `None` if missing.

**Changed in version 3.9:** Added merge (`|`) and update (`|=`) operators.

#### Examples

- **Grouping into lists**:

  ```python
  s = [('yellow',1),('blue',2),('yellow',3)]
  d = defaultdict(list)
  for k,v in s:
      d[k].append(v)
  # {'yellow':[1,3], 'blue':[2]}
  ```

- **Counting**:

  ```python
  s = 'mississippi'
  d = defaultdict(int)
  for ch in s:
      d[ch] += 1
  # {'m':1,'i':4,'s':4,'p':2}
  ```

- **Constant factory**:

  ```python
  def const_factory(val):
      return lambda: val
  d = defaultdict(const_factory('<missing>'))
  d.update(name='John', action='ran')
  '%(name)s %(action)s to %(object)s' % d
  # 'John ran to <missing>'
  ```

- **Sets**:

  ```python
  d = defaultdict(set)
  for k,v in s:
      d[k].add(v)
  # {'m':{'m'}, 'i':{'i'}, ...}
  ```

---


### OrderedDict objects

Like a regular `dict` but remembers insertion order and supports efficient reordering.

- Equality checks both keys and order.
- `popitem(last=True/False)`: pop from end or front.
- `move_to_end(key, last=True/False)`: reposition an existing key.
- Supports reverse iteration of items, keys, and values.

**Changed in version 3.9:** Added merge (`|`) and update (`|=`) operators.

#### Example: LRU cache skeleton

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, maxsize=128):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
```
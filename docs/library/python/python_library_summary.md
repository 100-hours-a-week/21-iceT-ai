1. 내장 함수: 기본 내장 라이브러리

2. itertools: 순열과 조합

3. heapq: 힙(Heap) 기능 제공, 우선순위 큐 기능 구현

4. bisect: 이진 탐색(Binary Search) 기능 제공

5. collections: 덱(deque), 카운터(Counter) 등의 유용한 자료구조 포함

6. math: 필수적인 수학적 기능 제공(팩토리얼, 제곱근, 최대공약수(GCD), 삼각함수 관련 함수들과 파이같은 상수 포함)

 

## 1. 내장 함수

### sum() 함수
```python
result = sum(1, 2, 3, 4, 5)
print(result) # 15
```

### min() 함수
```python
result = min(7, 3, 5, 2)
print(result) # 2
```

### max() 함수
```python
result = max(7, 3, 5, 2)
print(result) # 7
```

### sorted() 함수
```python
result = sorted([9, 1, 8, 5, 4]) # 오름차순 정렬
print(result) # 1 4 5 8 9

result = sorted([9, 1, 8, 5, 4], reverse = True) # 내림차순 정렬
print(result) # 9 8 5 4 1

result = sorted([('홍길동', 35), ('이순신', 75), ('아무개', 50)], key = lambda x: x[1], reverse = True)
print(result) # [('이순신', 75), ('아무개', 50), ('홍길동', 35)]
```



## 2. itertools
반복되는 데이터 처리 기능 포함 라이브러리

### permutations : iterable 객체에서 r개의 데이터를 뽑아 일렬로 나열하는 모든 경우(순열)을 계산
```python
# permutations example
from itertools import permutations

data = ['A', 'B', 'C']
result = list(permutations(data, 3)) # 모든 순열 구하기
print(result) # [('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]
``` 

### combinations : iterable 객체에서 r개의 데이터를 뽑아 순서를 고려하지 않고 나열하는 모든 경우(조합)를 계산
```python
# combinations example
from itertools import combinations

data = ['A', 'B', 'C']
result = list(combinations(data, 2)) # 2개를 뽑는 모든 조합 구하기
print(result) # [('A', 'B'), ('A', 'C'), ('B', 'C')]
``` 

### product :  permutations와 같이 iterable 객체에서 r개의 데이터를 뽑아 일렬로 나열하는 모든 경우(순열)을 계산한다. 다만 원소를 중복하여 뽑는다.
```python
# product example
from itertools import product

data = ['A', 'B', 'C']
result = list(proudct(data, repeat = 2)) # 2개를 뽑는 모든 순열 구하기(중복 허용)
print(result) # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
``` 

### combinations_with_replacement : combinations와 같이 iterable 객체에서 r개의 데이터를 뽑아 순서를 고려하지 않고 나열하는 모든 경우(조합)를 계산한다. 다만 원소를 중복해서 뽑는다.
```python
# combinations_with_replacement example
from itertools import combinations_with_replacement

data = ['A', 'B', 'C']
result = list(combinations_with_replacement(data, 2)) # 2개를 뽑는 모든 조합 구하기(중복 허용)
print(result) # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
```


## 3. heapq

- 파이썬에서는 힙 기능을 위해 heapq 라이브러리를 제공함. heapq는 다익스트라 최단 경로 알고리즘을 포함해 다양한 알고리즘에서 우선순위 큐 기능을 구현하고자 할 때 사용됨. heapq 외에도 PriorityQueue 라이브러리를 사용할 수 있지만, 코딩테스트 환경에서는 보통 heapq가 더 빠르게 동작함.
- 파이썬의 힙은 최소 힙으로 구성되어 있음. 보통 최소 힙 자료구조의 최상단 원소는 항상 '가장 작은' 원소
- heapq.heappush() : 힙에 원소 삽입
- heapq.heappop() : 힙에서 원소 꺼내기
- 힙 정렬 : 최소 힙이므로, 단순히 원소를 힙에 전부 넣었다가 빼는 것 만으로도 시간복잡도 O(NlogN)에 오름차순 정렬이 완료됨.

### 최소 힙
```python
import heapq

def heapsort(iterable):
	h = []
    result = []
    # 모든 원소를 차례대로 힙에 삽입
    for value in iterable:
    	heapq.heappush(h, value)
    # 힙에 삽입된 모든 원소를 차례대로 꺼내어 담기
    for i in range(len(h)):
    	result.append(heapq.heappop(h))
    return result
    
result = heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
print(result) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 최대 힙
```python
import heapq

def heapsort(iterable):
	h = []
    result = []
    # 모든 원소를 차례대로 힙에 삽입
    for value in iterable:
    	heapq.heappush(h, -value)
    # 힙에 삽입된 모든 원소를 차례대로 꺼내어 담기
    for i in range(len(h)):
    	result.append(-heapq.heappop(h))
    return result
    
result = heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
print(result) # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

## 4. bisect

: 파이썬에서는 이진 탐색을 쉽게 구현할 수 있도록 bisect 라이브러리를 제공함. '정렬된 배열'에서 특정한 원소를 찾아야할 때 매우 효과적으로 사용됨.

- bisect_left(a, x): 정렬된 순서를 유지하면서 리스트 a에 데이터 x를 삽입할 가장 왼쪽 인덱스를 찾는 메서드 (O(logN))
- bisect_right(a, x): 정렬된 순서를 유지하도록 리스트 a에 데이터 x를 삽입할 가장 오른쪽 인덱스를 찾는 메서드 (O(logN))

### 기본 사용법
```python
from bisect import bisect_left, bisect_right

a = [1, 2, 4, 4, 8]
X = 4

print(bisect_left(a, X)) # >>> 2
print(bisect_right(a, X)) # >>> 4
```

### '정렬된 리스트'에서 '값이 특정 범위에 속하는 원소의 개수'를 구하고자 할 때, 효과적으로 사용됨
```python
from bisect import bisect_left, bisect_right

# 값이 [left_value, right_value]인 데이터의 개수를 반환하는 함수
def count_by_range(a, left_value, right_value):
	right_index = bisect_right(a, right_value)
    left_index = bisect_left(a, left_value)
    return right_index - left_index
    
# 리스트 선언
a = [1, 2, 3, 3, 3, 3, 4, 4, 8, 9]

# 값이 4인 데이터 개수 출력
print(count_by_range(a, 4, 4)) # >>> 2

# 값이 [-1, 3] 범위에 있는 데이터 개수 출력
print(count_by_range(a, -1, 3)) # >>> 6
```


## 5. collections
: 파이썬의 collections 라이브러리는 유용한 자료구조를 제공하는 표준 라이브러리. 

### deque

: 보통 파이썬에서는 deque를 사용해 큐를 구현함
: 리스트 자료형과 다르게 인덱싱, 슬라이싱 등의 기능은 사용할 수 없음.
: 연속적으로 나열된 데이터의 시작 부분이나 끝 부분에 데이터를 삽입하거나 삭제할 때 매우 효과적임.
   · popleft() : 첫 번째 원소 제거
   · pop() : 마지막 원소 제거
   · appendleft(x) : 첫 번째 인덱스에 원소 x를 삽입
   · append(x) : 마지막 인덱스에 원소 x를 삽입
: 큐 자료구조를 이용할 때, append()와 popleft() 사용하기

```python
from collections import deque

data = deque([2, 3, 4])
data.appendleft(1)
data.append(5)

print(data) # >>> deque([1, 2, 3, 4, 5])
print(list(data)) # >>> [1, 2, 3, 4, 5]
```

### Counter

: 리스트와 같은 iterable 객체가 주어졌을 때, 해당 객체 내부의 원소가 몇 번씩 등장했는지 알려줌

```python
from collections import Counter

counter = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])

print(counter['blue']) # >>> 3
print(counter['green']) # >>> 1
print(dict(counter)) # >>> {'red': 2, 'blue': 3, 'green': 1}
```

## 6. math

: 자주 사용되는 수학적인 기능을 포함하고 있는 라이브러리.

### factorial example
```python
import math

print(math.factorial(5)) # 120
```

### sqrt(제곱근) example
```python
import math

print(math.sqrt(7)) # 2.6457513110645907
```

### gcd(최대 공약수) example
```python
import math

print(math.gcd(21, 14)) # 7
```

### pi(파이), e(자연상수) example
```python
import math

print(math.pi) # 3.141592653589793
print(math.e) # 2.718281828459045
```
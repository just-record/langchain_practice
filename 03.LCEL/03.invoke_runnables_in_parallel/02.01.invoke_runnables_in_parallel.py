from operator import itemgetter

##########################################
### 기본 형태
##########################################

# 리스트의 요소에서 특정 인덱스를 추출
data = [(1, 'a'), (2, 'b'), (3, 'c')]
get_first = itemgetter(0)

# 각 튜플의 첫 번째 요소를 추출
print(get_first(data[0]))  # 출력: 1
print(get_first(data[1]))  # 출력: 2
print(get_first(data[2]))  # 출력: 3

print('-' * 50)

##########################################
### 리스트 정렬
##########################################
data = [(1, 'b'), (3, 'a'), (2, 'c')]

# 두 번째 요소를 기준으로 정렬
sorted_data = sorted(data, key=itemgetter(1))
print(sorted_data)  # 출력: [(3, 'a'), (1, 'b'), (2, 'c')]

print('-' * 50)

##########################################
### 딕셔너리 정렬
##########################################
data = [
    {'name': 'John', 'age': 25},
    {'name': 'Jane', 'age': 22},
    {'name': 'Dave', 'age': 30}
]

# 'age' 키를 기준으로 정렬
sorted_data = sorted(data, key=itemgetter('age'))
print(sorted_data)
# 출력: [{'name': 'Jane', 'age': 22}, {'name': 'John', 'age': 25}, {'name': 'Dave', 'age': 30}]

print('-' * 50)

##########################################
### 다중 인덱스 추출
##########################################
data = [
    (1, 'a', 10),
    (2, 'b', 20),
    (3, 'c', 30)
]

get_first_and_third = itemgetter(0, 2)

# 각 튜플의 첫 번째와 세 번째 요소를 추출
for item in data:
    print(get_first_and_third(item))
# 출력: (1, 10), (2, 20), (3, 30)


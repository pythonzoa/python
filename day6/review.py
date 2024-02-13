# 1. 유저에게 설날에 먹은 음식 3개를 묻고,
# 설날에 먹은 음식 리스트 나타내기

# 2. 유저에게 좋아하는 커피 프랜차이즈 영어로 입력받고
# 대문자화 하기

# 3. 유저에게 이메일 주소를 입력받고, 도메인만 출력하기
# ex) megastudy@naver.com -> naver

# 4. 영어 기사를 스크랩하여, 단어별로 리스트화해서 오름차순으로 출력하기


#1
sulfood = []
a = input("설날에 먹은 음식:")
b = input("설날에 먹은 음식:")
c = input("설날에 먹은 음식:")
sulfood.append(a)
sulfood.append(b)
sulfood.append(c)
print(f'설날에 먹은 음식 리스트 : {sulfood}')

#2
coffee = input('좋아하는 커피 브랜드 : ')
print(coffee.upper())

#3
domain = input("이메일 입력 : ")
a = domain.split('@')
b = a[1].split('.')
print(b[0])

#4
article = 'English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England.[4][5][6] The namesake of the language is the Angles, one of the ancient Germanic peoples that migrated to the island of Great Britain.'

worldlist = article.split(' ')
worldlist.sort()
print(worldlist)
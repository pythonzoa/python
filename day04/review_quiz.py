# a = int(input("나이를 입력해 주세요 : "))
#
# b = 2024 - a
#
# print("나이가",a,"살이라면, 출생년도는 ",b,"년입니다.")
#
# c = int(input("사각형의 변의 길이를 입력해주세요 : "))
#
# d = c**2
#
# print("한 변의 길이가 ",c,"cm라면, 넓이는 ",d,"cm2입니다")

#####################
# age = int(input("나이가 어떻게 되십니까?"))
# print(f"나이가 {age}살이라면, 출생년도는 {2025 - age}년입니다")
#
# side = int(input("한 변의 길이: "))
# print(f"한 변의 길이가 {side}cm이면, 넓이는 {side ** 2}cm^2 입니다.")
#
# #3번 퀴즈 밑변 높이
# line = int(input("밑변의 길이 : "))
# height = int(input("높이의 길이 : "))
# print(f"밑변이 {line}이고, 높이가{height}이면, 삼각형의 넓이는 {line*height/2}입니다")

###############
num = int(input("10,000에서 99,999 사이의 정수를 입력해주세요"))
# print(f"선택하신 숫자는 {num[0]}만{num[1]}천{num[2]}백{num[3]}십{num[4]}입니다.")
##정답##
ten_thousands = num // 10000
thousands = (num % 10000) // 1000
hundred = (num % 1000) // 100
ten = (num % 100) // 10
one = (num % 10)
print(f"{ten_thousands}만 {thousands}천 {hundred}백 {ten}십 {one}")


number = int(input("양의 정수를 입력해주세요"))
min = int(number/60)
hour = int(min/60)
print(min)
print(hour)
print(f"입력하신 초의 변환된 시간은 {hour}시간 {min-hour*60}분 {number-min*60}초입니다")

##정답##
hour = time // 3600
min = (time % 3600) // 60
sec = time % 60


num = int(input("10,000에서 99,999 사이의 정수를 입력해주세요"))
a = int(num%1000)
print(f"선택하신 숫자의 백의 자리는 {a//100}입니다")
##정답##
print(f"{num // 100} % 10")


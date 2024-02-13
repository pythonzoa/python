# dict
#MBTI
# mbti = {
#     'e' : '외향적',
#     'i' : '내향적',
#     's' : '현실적',
#     'n':'상상력이 풍부한',
#     't':'공감을 해주지 않는',
#     'f':'감성적인',
#     'p':'즉흥적',
#     'j':'계획적'
# }
#
# a = input("당신의 mbti를 입력해주세요 : ")
# b = mbti[a[0]]
# c = mbti[a[1]]
# d = mbti[a[2]]
# e = mbti[a[3]]
#
# print(f"당신은 {b}, {c}, {d}, {e}인 사람이시군요")

my_dict = {'name' : 'alice','age' : 25}
print(my_dict['name'])
print(my_dict.get('name'))
print(my_dict.get('gender','Not Specified'))

#keys
print(list(my_dict.keys()))
#values
print(list(my_dict.values()))
#items
print(list(my_dict.items()))
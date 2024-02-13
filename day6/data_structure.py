# data_structure
# [](list),{}(set),{}(dict),()(tuple)

# # set(집합, 중복 허용 안됨 ❗❗)
# a = {1,1,4,8,8,1,8}
# b = set([8,1,3,8,1,8,1,8])
# a.update({10,4})
#
# print(a)
# #print(b)
#
#
# star = ['아메','라떼','물','불']
# mega = ['조리퐁','물','불','오늘의커피']
# a = set(star)
# b = set(mega)
# a.update(b)
# print(a)

#
# article = "Messi relocated to Spain from Argentina aged 13 to join Barcelona, for whom he made his competitive debut aged 17 in October 2004. He established himself as an integral player for the club within the next three years, and in his first uninterrupted season in 2008–09 he helped Barcelona achieve the first treble in Spanish football; that year, aged 22, Messi won his first Ballon d'Or. Three successful seasons followed,"
#
# b = article.split(" ")
# c = set(b)
# d = list(c)
# d.sort()
# print(d)

article_a = "Messi relocated to Spain from Argentina aged 13 to join Barcelona, for whom he made his competitive debut aged 17 in October 2004. He established himself as an integral player for the club within the next three years, and in his first uninterrupted season in 2008–09 he helped Barcelona achieve the first treble in Spanish football; that year, aged 22, Messi won his first Ballon d'Or. Three successful seasons followed, with Messi winning four consecutive Ballons d'Or, making him the first player to win the award four times. During"
article_b = "An Argentine international, Messi is the country's all-time leading goalscorer and also holds the national record for appearances. At youth level, he won the 2005 FIFA World Youth Championship, finishing the tournament with both the Golden Ball and Golden Shoe, and an Olympic gold medal at the 2008 Summer Olympics. His style of play as a diminutive, left-footed dribbler drew comparisons with his compatriot Diego Maradona, who described Messi as his successor. After his senior debut in August 2005, Messi became the younges"

a = article_a.split(" ")
b = article_b.split(" ")

c = set(a)
d = set(b)

g = c.intersection(d)

print(a)
print(b)
print(c)
print(d)
print(g)

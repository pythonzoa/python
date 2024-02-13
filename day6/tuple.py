# quiz 영화 예매 프로그램[자료구조를 적절히 사용]

movie = {
    'action': 10000,
    'romance': 8000,
    'horror': 9000
}

food = {
    'cheese': 6000,
    'caramel': 5000,
    'popcorn': 4000
}

print(list(movie.keys())[0])

a = int(input(f"영화를 골라 주세요. 1.{list(movie.keys())[0]}, 2.{list(movie.keys())[1]}, 3.{list(movie.keys())[2]} : "))
b = int(input(f"음식를 골라 주세요. 1.{list(food.keys())[0]}, 2.{list(food.keys())[1]}, 3.{list(food.keys())[2]} : "))

print(a)

print(
    f"{list(movie.keys())[a - 1]} 영화는 {list(movie.values())[a - 1]}원, {list(movie.keys())[b - 1]} 음식은 {list(movie.values())[b - 1]}원이므로 총 {list(movie.values())[a - 1] + list(movie.values())[b - 1]}원 결재 부탁드립니다")

# 정답
theater = {
    'movie': {
        'movieList': ['액션', '로맨스', '공포'],
        'price': [1000, 100, 500]
    },
    'popcorn': {
        'popcornList': ['일반', '카라멜', '치즈'],
        'price': [5154, 8, 181]
    }
}

movie = int(input(f"{theater['movie']['movieList']} 중 하나를 선택하세요(0~2번) : "))
popcorn = int(input(f"{theater['popcorn']['popcornList']} 중 하나를 선택하세요(0~2번) : "))
print(f"영화:{theater['movie']}")

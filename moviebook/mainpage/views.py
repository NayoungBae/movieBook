from django.shortcuts import render
from django.http import HttpResponse

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

import random


# Create your views here.
def select_current(url) :

    #링크로 접속
    page = urlopen(url)
    #접속한 페이지 크롤링
    bs = BeautifulSoup(page, "html.parser")
    #body태그의 내용
    body = bs.body

    #---------------------------------------------------------

    #class="lst_detail_t1"인 태그 찾기
    #이 클래스는 원래부터 하나 있음
    target = body.find(class_="lst_detail_t1")

    #class="lst_detail_t1"인 태그에서 모든 li 태그 찾기
    #각 영화의 모든 정보(이름,포스터, 예매율, 평점, ...)
    li_list = target.find_all("li")

    #각 영화의 예매율(예매율 안 써있는 영화는 상영중 아님)
    star_list = target.find_all(class_="star_t1 b_star")

    #---------------------------------------------------------

    #딕셔너리 안에 딕셔너리 여러개 담음
    #예매순 순위로 영화 정보를 담은 딕셔너리를 또 다른 딕셔너리에 담을 예정
    movies_list1 = []             #첫번째줄. 영화 5개 담기
    movies_list2 = []             #두번째줄. 영화 5개 담기

    #현재 상영중 영화 개수
    screening = len(star_list)

    random_set = set()
    #영화를 랜덤으로 출력하기 위한 변수
    while len(random_set) < 10 :
        number = int(random.random() * screening)
        random_set.add(number)   
        #중복되는 숫자 제거를 위한 과정
              
    count = 0

    #영화 정보를 10개만 출력할것임
    for i in random_set :
        #한 영화의 정보를 담을 딕셔너리
        movie_dic = {}

        #영화 이미지
        image = li_list[i].find(class_="thumb").find("img")["src"]
        movie_dic["image"] = image

        #평점
        grade = li_list[i].find(class_="star_t1").find(class_="num").text
        movie_dic["grade"] = grade

        #딕셔너리에 값을 추가하는 일을 세는 변수
        count += 1

        if count > 5 :
            #한 영화의 정보를 담은 딕셔너리를 또다른 딕셔너리에 넣기
            movies_list2.append(movie_dic)
        else :
            #한 영화의 정보를 담은 딕셔너리를 또다른 딕셔너리에 넣기
            movies_list1.append(movie_dic)
    
    context = {"movies_list1" : movies_list1, "movies_list2" : movies_list2}        

    return context


def index(request) :
    
    #현재 상영중인 영화 순위(예매순)
    url = "https://movie.naver.com/movie/running/current.nhn"

    #예정 영화
    #url = "https://movie.naver.com/movie/running/premovie.nhn"

    context = select_current(url)  

    return render(request, 'mainpage/index.html', context)
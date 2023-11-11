# allrights_BE
사운드가 만들어내는 변화무쌍한 창작물

> 멋쟁이 사자처럼 4호선톤<br>
> "The next stop is, growling to line 4 growth station." <br>
> 
> 프로젝트 기간 : 2023.10.30 ~ 2023.11.11

<br>

## ⚙️ 개발환경 초기 셋팅
### 1. 가상환경 생성 (최초 1회만)
    windows: python -m venv {가상 환경 이름}
    mac: python3 -m venv {가상 환경 이름}
    * 가상 환경 이름은 myvenv로 통일

### 2. 가상환경 실행 
    windows: source venv/Scripts/activate
    mac: source venv/bin/activate


### 3. 라이브러리 설치
    pip install -r requirements.txt

### 4. db 마이그레이션 진행
    python manage.py makemigrations
    python manage.py migrate

### 4-2. db 마이그레이션 에러 시 해결
    python manage.py makemigrations -merge
    python manage.py migrate --run-syncdb

### 5. 서버 실행
    python manage.py runserver

<br>

## 📁 프로젝트 폴더링

```

├── config
│   ├── account
│       └── __init__.py
│       └── admin.py
│       └── apps.py
│       └── models.py
│       └── serializers.py
│       └── tests.py
│       └── urls.py
│       └── views.py
│   ├── config
│       └── __init__.py
│       └── asgi.py
│       └── settings.py
│       └── urls.py
│       └── wsgi.py
│   ├── music
│       └── __init__.py
│       └── admin.py
│       └── apps.py
│       └── models.py
│       └── serializers.py
│       └── tests.py
│       └── urls.py
│       └── views.py
│   ├── media
│   ├── static
│   ├── db.sqlite3
│   ├── manage.py
├── myvenv
└── requirements.txt
```
<br>

## [📝 Api 명세서]([링크](https://www.notion.so/b5d83e43e16c4386b3193664e2bb765d?v=0be7bd8a66004afda990722661368fa8&pvs=4))
|완료|기능명|method|headers|url|담당자|
|:---|---|---|---|---|---|
|✅|회원가입|`POST`||/account/signup/| `박소윤` |
|✅|로그인|`POST`||/account/signin/| `박소윤` |
|✅|로그인 한 회원 정보 학인|`GET`|`access`|/account/auth/| `박소윤` |
|✅|access 토큰 재발급|`POST`||/account/token/refresh/| `박소윤` |
|✅|로그아웃|`DELETE`||/account/signout/|`박소윤`|
|✅|마이페이지|`GET`||/account/mypage/\<int:user_id\>/|`박소윤`|
|✅|회원 정보 수정|`PUT`|`access`|/account/mypage/update/\<int:ser_id\>/|`박소윤`|
|✅|비밀번호 변경|`POST`|`access`|/account/password/\<int:ser_id\>/|`박소윤`|
|✅|익명 사용자 음악 작성|`POST`||/account/mypage/\<int:user_id\>/|`이서현`|
|✅|로그인 사용자 음악 작성|`POST`|`access`|/account/mypage/\<int:user_id\>/|`박소윤`|
|✅|전체 음악 조회|`GET`||/music/|`이서현`|
|✅|음악 상세 조회|`GET`||/music/\<int:music_id\>/|`이서현`|
|✅|음악 다운로드|`GET`||/music/download/\<int:music_id\>/|`이서현`|
|✅|음악 검색 조회|`POST`||/music/search/?search_words='검색어'/|`이서현`|
|✅|음악 정렬 조회|`POST`||/music/search/?sort_by=downloads/|`이서현`|
|✅|음악 좋아요|`POST`|`access`|/music/like/\<int:music_id\>/|`박소윤`|
|✅|음악 별 좋아요 유저 조회|`GET`||/music/like/\<int:music_id\>/|`박소윤`|
<br>

## 🦁 백엔드 개발자 팀원


| 박소윤 | 이서현 |
| :---------:|:----------:|
|<img width="300" alt="image" src="https://avatars.githubusercontent.com/u/102134838?v=4"> | <img width="300" alt="image" src="https://avatars.githubusercontent.com/u/80608587?v=4"> | 
| [happine2s](https://github.com/happine2s) | [newoceanwave](https://github.com/newoceanwave) |
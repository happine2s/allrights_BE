# allrights_BE

<br>

## 개발환경 초기 셋팅
### 가상환경 생성 (최초 1회만)
    windows: python -m venv {가상 환경 이름}
    mac: python3 -m venv {가상 환경 이름}
    * 가상 환경 이름은 myvenv로 통일

### 가상환경 실행 
    windows: source venv/Scripts/activate
    mac: source venv/bin/activate


### 라이브러리 설치
    pip install -r requirements.txt

### db 마이그레이션 진행
    python manage.py makemigrations
    python manage.py migrate

### db 마이그레이션 에러 시 해결
    python manage.py makemigrations -merge
    python manage.py migrate --run-syncdb

### 서버 실행
    python manage.py runserver

<br>
<br>

## 프로젝트 폴더링

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

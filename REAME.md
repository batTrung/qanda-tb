# qanda-tb

## Cài đặt

Đầu tiên, tải repository về máy tính:

```bash
git clone https://github.com/batTrung/qanda-tb.git
```

Cài đặt requirements:

```bash
cd qanda-tb
pip install -r requirements.txt
```

Tạo database:

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

Chạy development server:

```bash
python manage.py runserver
```

Mở Chrome hay FireFox : **localhost:8000**

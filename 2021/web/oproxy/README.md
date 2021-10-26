# OProxy

### Author: [Nguyen Cao Huy Hoang](https://github.com/antoinenguyen-09)

![image](https://user-images.githubusercontent.com/61876488/138734999-47bd9310-d23a-4b6f-a76e-46920f30263e.png)

[Source]()

### 1. Initial reconnaissance:

Đầu tiên chúng ta cần tạo account để login vào:

![image](https://user-images.githubusercontent.com/61876488/138804603-2b407efe-bf24-4bf2-84b0-c3d1e24cac60.png)

Sau khi xem qua sơ bộ thì ta có thể tóm tắt web app của challenge này có những chức năng như sau:

- /proxy: khi nhập vào một URL bất kì (vd như https://stackoverflow.com) rồi bấm nút "Go!" thì web app sẽ tự động redirect đến URL đó.

![image](https://user-images.githubusercontent.com/61876488/138809779-5d5d13d9-88c5-4296-91b4-d22e1e2e979a.png)

- /history?key=<key>&memcache=<memcache>: tất cả những URL mà web app này redirect đến thông qua chức năng `/proxy` sẽ được ghi lại tại đây. Nếu tạo thêm một user nữa thì ta 

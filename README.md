# DBI_202_sp22
** Phân Tích Quản Lý Điểm FLM **
# Xác Định Và Tổng Hợp Các Dữ Liệu 
## Bảng Thông Tin Các Điểm Thành Phần
###   ![image](https://user-images.githubusercontent.com/76523661/174435404-9625a8e9-0cb4-4422-bf44-80bf17562179.png) 
###   Category (hạng mục)
####       Progress Tests 
####       Assignment
####       Labs,Pe,FE
###   Type(loại) 
####       Quiz 
####       On-going
####       Pe, Fe
###   Part ( phần )
###   Weight 
####       Mô Tả: Trọng số trên từng hạng mục 
###   Completion Criteria 
####       Mô Tả: Điều kiện để thi và điểm tối thiểu để pass 
###   Duration
####       Mô Tả: Khoảng thời gian cần làm việc trong hạng mục
####       At home 
####       In lab session
###   Question Type( Loại câu hỏi ): MTC
###   No Question( Số câu hỏi )
###   Knowledge and Skill
###   Grading Guide
###   Note
--------------------------------------------------------------------------
## Bảng Môn Và Khóa Học 
### ![image](https://user-images.githubusercontent.com/76523661/174435441-24021f17-609a-4c3d-ac96-fc9184d21479.png)
### NO: number of subject
### Subject code : One subject <-> One code
### Subject name : Define of subject
### Semester : Seasons +  Years
### Group: Lớp học 
### StartDate: Thời điểm bắt đầu môn học
### EndDate: Thời điểm kết thúc môn học
### Average Mark: điểm trung bình
### Status: Not Passed OR Passed
--------------------------------------------------------------------------
## Bảng Điểm Của Sinh Viên
### ![image](https://user-images.githubusercontent.com/76523661/174435461-09a9d235-f99f-4169-8c2a-cebee1f6d4e7.png)
### Grade category (hạng mục)
#### Quiz 1 ( PT1 )
#### Quiz 2 ( PT2 )
#### Group Assignment
#### Group Project
#### Final Exam 
#### Final Exam Resit
### Grade Item ( hạng mục ) : thêm 1 row total
### Weight: Tỉ trọng điểm thành phần( cũng có ở bên FML table )
### Value: Mark
--------------------------------------------------------------------------
# Xác Định Các Thực Thể Và Các Thông Tin Thuộc Tính 
##    Xác Định Các Thực Thể 
###         Thực Thể 1: 
####               Các Thuộc Tính Cần Có
###         Thực Thể 2: 
####               Các Thuộc Tính Cần Có
###         Thực Thể 3: 
####               Các Thuộc Tính Cần Có
###         Thực Thể 4: 
####               Các Thuộc Tính Cần Có
###         Thực Thể 5: 
####               Các Thuộc Tính Cần Có
###         Thực Thể 6: 
####               Các Thuộc Tính Cần Có
--------------------------------------------------------------------------
# Phân Chia Các Entities Và Relationships
##  Entity x  <-> Entity y
###     Mô Tả:  
###     -> Xác Định Quan Hệ Giữa Entity X Và Y ( 1-1,1-n,n-n)
--------------------------------------------------------------------------
# ERD Diagram
## Image ERD
--------------------------------------------------------------------------
# Chuyển đổi
##   ERD -> Quy Chuẩn 3NF -> Bước Đầu Xác Định DataBase_Diagram
##   Xác Định Primary Key Các Table 
##   Phân Tách Các Quan Hệ ( 1-n , n-n )
###     1-n -> Tạo Foriegn Key 
###     n-n ( Table X - Table Y ) -> Tạo New_Table với Pimarykey_New_Table(Foriegn_Key_Table_X,Foriegn_Key_Table_Y)
--------------------------------------------------------------------------
##   Chuẩn Hóa Thuộc Tính Các Attribute Trên Từng Bảng 
###     Table1 : Object 1
####        Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
###     Table2 : Object 2
####        Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
###     Table3 : Object 3
####        Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
--------------------------------------------------------------------------
##   Database_Diagram
###     Hình Ảnh Và Mô Tả
--------------------------------------------------------------------------
# Triển Khai DataBase_Diagram Trên Sql_Server
##   Creat Table And Attributes
###     Code sql
###     Image + Results
##   Creat Pk And FK 
###     Code sql
###     Image + Results
##   Create Relations Beetween Table in Database
###     Code sql
###     Image + Results
##   Đưa Dữ Liệu Vào DataBase
###     Code sql
###     Image + Results
--------------------------------------------------------------------------
# Kiểm tra, Truy Xuất Dữ Liệu Từ Database
--------------------------------------------------------------------------
# Query Requirements And Results
##   Query1 :
###     Code sql
###     Image + Results

##   Query2 :
###     Code sql
###     Image + Results


##   Query3 :
###     Code sql
###     Image + Results

--------------------------------------------------------------------------
# Tổng Kết Và Tài Liệu 
## ....
## File < Link Files > SQL Của Database
## FIle < Link Files > SQL Queries Requirements


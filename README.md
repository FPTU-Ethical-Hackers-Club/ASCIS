# DBI_202_sp22
*** Phân Tích Quản Lý Điểm FLM ***
# Xác Định Và Tổng Hợp Các Dữ Liệu 
## Bảng Thông Tin Các Điểm Thành Phần
###   ![image](https://user-images.githubusercontent.com/76523661/174473470-0efadd32-427b-475b-93a6-52d2a7179314.png)
###   Category (hạng mục)
          Mô Tả: Danh sách, Tên Các Đầu Điểm
               - Progress Tests 
               - Assignment
               - Labs
               - PE ( Practice Exam )
               - FE ( Final Exam )
###   Type(loại) 
          Mô Tả: Trạng Thái Và Loại Hình Kiểm Tra
               - Quiz 
               - On-going
               - PE ( Practice Exam )
               - FE ( Final Exam )
###   Part 
          Mô Tả: Số lượng các đầu điểm trên từng hạng mục - đầu điểm
###   Weight 
          Mô Tả: Trọng số trên từng hạng mục - đầu điểm
###   Completion Criteria 
          Mô Tả: Điều kiện để thi và điểm tối thiểu để pass 
###   Duration
          Mô Tả: Khoảng thời gian cần làm việc trong hạng mục
               - At home 
               - In lab session
###   Question Type( Loại câu hỏi )
          Mô Tả: Cách Triển Khai Lấy Đầu Điểm
               - Multichoices
               - Practices 
               - Design And Present
               - Scripts

###   No Question( Số câu hỏi )
          Mô Tả: Quy Định Về Số Lượng Câu Hỏi Trong Bài Kiểm Tra 
###   Knowledge and Skill
          Mô Tả: Yêu Cầu Tiêu Chuẩn Trong Kĩ Năng Và Kiến Thức Cần Đạt Trước Khi Tham Gia
               - Đầu Điểm Theo Từng Phân Mức Chương Trình Học
               - Kĩ Năng Thực Hành
               - Kiến Thức Tập Trung Quan Trọng
###   Grading Guide
          Mô Tả: Người Chịu Trách Nghiệm Hướng Dẫn Và Quy Định Cách Thực Hiện Trình Bày Để Đạt Được Các Tiêu Chí Trên Các Hạng Mục
###   Note
          Mô Tả: Tiêu Chí, Tỉ Trọng Và Hướng Dẫn Cho Điểm Trên Các Hạng Mục
--------------------------------------------------------------------------
## Bảng Môn Và Khóa Học 
### ![image](https://user-images.githubusercontent.com/76523661/174435441-24021f17-609a-4c3d-ac96-fc9184d21479.png)
### NO
          Mô Tả: Số Lượng Môn Học, Khóa Học
### Subject code 
          Mô Tả: Mã Code Tương Ứng Trên Từng Khóa Học
### Subject name 
          Mô Tả: Định Nghĩa Và Khai Quát Chung Về Môn Học
### Semester 
          Mô Tả: Thời Gian Và Kì Học
               - Seasons 
               - Years
### Group: Lớp học 
          Mô Tả: Tên Lớp Học Theo Khóa Và Kì Học
### StartDate
          Mô Tả: Thời điểm bắt đầu môn học
### EndDate
          Mô Tả: Thời điểm kết thúc môn học
### Average Mark
          Mô Tả: Điểm trung bình
### Status
          Mô Tả: Trạng Thái Bài Nộp Của Sinh Viên
               - Not Passed 
               - Passed 
               - Passed With Conditions
--------------------------------------------------------------------------
## Bảng Điểm Của Sinh Viên
### ![image](https://user-images.githubusercontent.com/76523661/174435461-09a9d235-f99f-4169-8c2a-cebee1f6d4e7.png)
### Grade category (hạng mục)
          Mô Tả: Danh sách, Tên Các Đầu Điểm
               - Progress Tests ( Quiz )
               - Assignment ( Person, Group )
               - Labs
               - PE ( Practice Exam )
               - FE ( Final Exam )
               - Final Exam Resit
### Grade Item ( hạng mục ) 
          Mô Tả: Tên Và Tổng Đầu Điểm 
               - Item
               - Total 
### Weight
          Mô Tả: Tỉ trọng điểm thành phần, cũng có ở bên FML table (%)
### Value
          Mô Tả: Điểm Sinh Viên Đạt Được Trên Thang Điểm Quy Chuẩn
--------------------------------------------------------------------------
# Xác Định Các Thực Thể Và Các Thông Tin Thuộc Tính 
##    Xác Định Các Thực Thể 
###         Thực Thể 1: Students
               - StudentID
               - First Name 
               - Last Name
               - Address
               - Gender
               - Date Of Birth
               - Email
###         Thực Thể 2: Group Students
               - GroupID
               - Major
###         Thực Thể 3: Courses
               - CourseID
               - CourseName
               - Course_Status ( Online, Offline)
###         Thực Thể 4: Lectures
               - LectureID
               - First Name
               - Last Name
               - Gender
               - Phone
               - Date Of Birth
               - ReportTO
###         Thực Thể 5: Class
               - ClassID
               - Lecturer
               - Major
###         Thực Thể 6: Assessment
               - AssessmentID
               - Status
               - Semester
               - Start Date
               - End Date
###         Thực Thể 7: Category
               - CatID
               - Category
               - Type
               - Part
               - Weight
               - Duration
               - Quest Type
               - Number Of Questions
               - Skill
               - Grading Guide
               - Note
###         Thực Thể 8: Assessment system
               - AssessmentID
               - CourseID
               - AssigmentID
               - Weight
###         Thực thể 9: Assignment
               - AssigmentID
               - AssigmentName
               
--------------------------------------------------------------------------
# Phân Chia Các Entities Và Relationships
##  Entity Students <-> Entity Groups
    Mô Tả:  Một Student có thể đăng kí học nhiều Courses Và 1 Courses có thể có nhiều Student đăng kí học.
    -> Xác Định Quan Hệ Giữa Entity Students Và Entity Groups  là quan hệ nhiều nhiều ( n-n )
##  Entity Class <-> Entity Lectures
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 lecturer và 1 Lecturer có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Lectures là quan hệ một nhiều ( 1-n )
##  Entity Class <-> Entity Groups
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Student <-> Entity Assessment System
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Class <-> Entity Assessment System
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Courses <-> Entity Assessment System
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Class <-> Entity Assignment
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Courses <-> Entity Assignment
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( n-n )
##  Entity Category <-> Entity Assignment Systems
    Mô Tả:  Một Class chỉ có thể được phụ trách bởi đúng 1 Group và 1 Group có thể phụ trách nhiều class.
    -> Xác Định Quan Hệ Giữa Entity Class Và Entity Groups là quan hệ một nhiều ( 1-n )

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
            Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
###     Table2 : Object 2
            Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
###     Table3 : Object 3
            Các Attributes Và Định Dạng Kiểu Dữ Liệu Attributes
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


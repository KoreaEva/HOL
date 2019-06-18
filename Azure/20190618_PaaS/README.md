# PaaS 실습 과정 

## 인터넷 연결

PDEDU10F_WIFI_5G_1nd
PdEdu10f_WiFi

## 계정 설정

Azure Pass [https://www.microsoftazurepass.com/](https://www.microsoftazurepass.com/)<br>

```c
01 Q6ZZ5WCKCLI7GZUZL1
02 QHV92PUMPRLL9TJ8R6
03 Q8SB03IWQIDDS6B4LD
04 QOBJ1T55XBCO6OI49E
05 Q8XUY3B4B6BU7FUX2R
06 Q3I8IBR9OM5E1LBL5F
07 Q236E1UCUQEJWQ2M7W
08 QD2NMFNVDOCFDSBTW0
09 Q8NRTZHXG1XRJQDQHJ
10 QVUCTLLO8CQVM176IC
11 Q4DDINVSBZWEUJV8JN
12 Q78XGFB9EDH48IY88C
13 QIKL3GKX27I2YLPQJV
14 Q4OF9HMOFCUH3EVC5I
15 Q08FHGUG5UDZ1L7XRK
16 QR16EK5CBT79QHNT5O
17 QW3W1OL67UIRHINRFL
18 QXYKYUMK56SL203OL0
19 Q0J7HTMREC0KU8WO8Y
20 Q84MFZMZMLBC8Z4BLF
```

Github [http://github.com](github.com)<br>

## 설치 프로그램

1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)<br>
2. Visual Studio Code [https://code.visualstudio.com/download](https://code.visualstudio.com/download)<br>
3. MySQL Workbench [https://dev.mysql.com/downloads/workbench/](https://dev.mysql.com/downloads/workbench/)<br>


## Test Code

1. HTML Code의 업로드
```HTML
<html>
    <head>Test</head>
    <body>
        Hello World
    </body>
</html>
```
2. PHP Code 실행 확인 
```HTML
<html>
    <head>Test</head>
    <body>
        Hello World
    </body>
</html>
```

3. 구구단 출력하기
```HTML
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
<?php
 
echo "<h1>Ex. 구구단 출력하기</h1>";
 
for($i=2;$i<=9;$i++){
    echo $i."단 입니다.<br/>";
    for($j=1;$j<=9;$j++){
        echo $i." X ".$j." = ".($i*$j)."<br/>";
    }
    echo "<br/>";
}
 
?>
</body>
</html>
```

4. 데이터베이스 확인하기
```sql
show databases
```

5. 데이터베이스 생성하기
```sql
create database test_db;
```

6. 데이터베이스 선택하기
```sql
use test_db
```

7. 테이블 생성하기
```sql
CREATE TABLE member 
( 
	_id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(32) NOT NULL, 
    age int, 
    phone VARCHAR(12) 
)
```

8. 테이블 확인하기
```sql
show tables
```

9. 데이터 입력하기
```sql
INSERT INTO member(name, age, phone) 
VALUES('Bill Gates', 20, '010-1111-1111')
```

10. 데이터 확인하기
```sql
SELECT * FROM member
```

11. 데이터 입력하기
```sql
INSERT INTO member(name, age, phone) 
VALUES('Steve Jobs', 22, '010-2222-2222')
```

12. 데이터 입력하기
```sql
INSERT INTO member(name, age, phone) 
VALUES('Donald John Trump', 24, '010-3333-3333')
```

13. PHP 코드 수정하기 
```php
<?php
$conn = mysqli_connect(
  'localhost',
  'root',
  '111111',
  'opentutorials');
echo "<h1>single row</h1>";
$sql = "SELECT * FROM topic WHERE id = 19";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_array($result);
echo '<h2>'.$row['title'].'</h2>';
echo $row['description'];
echo "<h1>multi row</h1>";
$sql = "SELECT * FROM topic";
$result = mysqli_query($conn, $sql);
while($row = mysqli_fetch_array($result)) {
  echo '<h2>'.$row['title'].'</h2>';
  echo $row['description'];
}```


1. Azure 기본 사항<br>
[https://docs.microsoft.com/ko-kr/learn/paths/azure-fundamentals/ ](https://docs.microsoft.com/ko-kr/learn/paths/azure-fundamentals/ )

2. Azure Virtual Machine을 통한 웹 배포<br>
[https://docs.microsoft.com/ko-kr/learn/paths/deploy-a-website-with-azure-virtual-machines/ ](https://docs.microsoft.com/ko-kr/learn/paths/deploy-a-website-with-azure-virtual-machines/ )

3. Azure Web Service로 웹 사이트 배포<br>
[https://docs.microsoft.com/ko-kr/learn/paths/deploy-a-website-with-azure-app-service/ ](https://docs.microsoft.com/ko-kr/learn/paths/deploy-a-website-with-azure-app-service/ )

4. 서버 리스 응용 프로그램 만들기<br>
[https://docs.microsoft.com/ko-kr/learn/paths/create-serverless-applications/ ](https://docs.microsoft.com/ko-kr/learn/paths/create-serverless-applications/ )

5. 참고자료<br>
[https://github.com/KoreaEva/HOL/blob/master/Azure/20190108_Korea_University/microsoftazure-technicaloverview-170405213706.pdf](https://github.com/KoreaEva/HOL/blob/master/Azure/20190108_Korea_University/microsoftazure-technicaloverview-170405213706.pdf)

## Lunch time 

1. Azure에 데이터 저장<br>
[https://docs.microsoft.com/ko-kr/learn/paths/store-data-in-azure/](https://docs.microsoft.com/ko-kr/learn/paths/store-data-in-azure/)


2. Azure SQL Database를 프로비전하여 애플리케이션 데이터 저장<br>
[https://docs.microsoft.com/ko-kr/learn/modules/provision-azure-sql-db/](https://docs.microsoft.com/ko-kr/learn/modules/provision-azure-sql-db/)


3. Azure Cosmos DB의 NoSQL 데이터 작업<br>[https://docs.microsoft.com/ko-kr/learn/paths/work-with-nosql-data-in-azure-cosmos-db/](https://docs.microsoft.com/ko-kr/learn/paths/work-with-nosql-data-in-azure-cosmos-db/)

4. Azure Cosmos DB를 사용하여 전세계에 데이터 배포<br>
[https://docs.microsoft.com/ko-kr/learn/modules/distribute-data-globally-with-cosmos-db/](https://docs.microsoft.com/ko-kr/learn/modules/distribute-data-globally-with-cosmos-db/)

# iot-repo-2
IoT 프로젝트 2조 저장소. 농작물 수거 <br/>
(기간: 2024년 04월 17일 ~ 2024년 04월 25일)
***
## 프로젝트 소개
#### 상품 등급에 따른 정돈 및 작업자 추적 로봇 설계 및 제어 
### 프로젝트 목적
- 아두이노 보드를 활용한 임베디드 시스템 제어 및 PyQT5를 활용한 GUI 관리 구현
- RC카와 로봇팔 동작을 위한 모터와 센서들을 아두이노 보드 및 메인 PC에서 제어

### 주제 선정
- 유튜브 '스마트팜' 검색결과
<img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/845fadad-96e3-48fd-8963-db1be8e8abed" width="400">
<img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/429dbc3f-2d4e-4183-a963-437f1f7d14b3" width="400">
<img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/cc60aadf-6136-49f7-97d2-90ee53fe8c0a" width="400">
<img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/903e91d4-a9ba-4eb7-8492-546f1969e69b" width="400"><br><br>

- 저비용 및 고효율 형태의 IOT 기술을 농업 산업에 접목한 **스마트팜** 대한 관심 서서히 증대
- 국내 기업에서 자율주행 트렉터 등 **스마트 농기계** 개발 중인 현황
- IOT 수업 때 배운 아두이노 보드 및 PC 통한 센서 제어, GUI 구현 등을 활용하여 **간단한 양품/불량품 분류 목적의 농작업용 로봇 설계 목표**
  
### 기술스택

<div align=center> 
  
   |**Category**|**Details**|
  |:----------:|:----------:|
  |**개발환경**|<img src="https://img.shields.io/badge/Ubuntu22.04-E95420?style=for-the-badge&logo=Ubuntu22.04&logoColor=white"> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white"> |
  |**소프트웨어 프로그램**|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Arduino-00878F?style=for-the-badge&logo=Arduino&logoColor=white">|
  |**데이터베이스 관리 시스템**|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white">|
  |**GUI**|<img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=Qt&logoColor=white">|
  |**협업 툴**|<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white"> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"> <img src="https://img.shields.io/badge/Confluence-172B4D?style=for-the-badge&logo=Confluence&logoColor=white"> <br> <img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white"> <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"> <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=Figma&logoColor=white"> |
</div> 

### 팀원 역할
<div align=center> 
  
|**구분**|**이름**|**역할**|
|:------:|:------:|:-------|
|팀장|채희곤|<ul><li>'Login', 'Register', 'Home' 및 'Main' window GUI 코드 작성</li><li> 데이터베이스 관리 시스템 및 GitHub, JIRA 등 협업 툴 환경 설정 및 관리</li><li>PPT 문서 작업</li></ul>|
|팀원|현혜지|<ul><li>'Login', 'Register', 'Home' 및 'Main' window GUI 코드 작성</li><li> 메인 PC와 Arduino Board 간 통신 제어</li></ul>|
|팀원|홍권호|<ul><li>RC카 및 로봇 팔 등 하드웨어 설계</li><li> RC카 및 로봇 팔 등 Arduino IDE 코드 작성</li></ul>|
|팀원|이유민|<ul><li> RC카 및 로봇 팔 등 Arduino IDE 코드 작성</li><li> 메인 PC와 Arduino Board 간 통신 제어</li></ul>|
</div> 

***

## 프로젝트 설계
### 기능 리스트
- (1) 작업자 인식 기능
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/f7da4214-c5e5-4f90-bf23-47246ee25742" width="700">
  </div>
- (2) 인식한 작업자 따라 정상 이동 기능
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/5e9eec3b-b0df-4359-980c-7a7d33e879cb" width="700">
  </div>
- (3) 등급별 정돈 정상 작동 기능
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/25fdabcc-2479-4e83-bd11-b86f88dd4fd2" width="700">
  </div>

### 시스템 구성도
#### 1. 제품 설계도
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/6743c392-578d-4256-a159-502d5a2e1527" width="800">
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/e5494963-d99e-4a22-b963-779ffe5f6ab9" width="600">
  </div> 
  
- 제품 파트별 주요 기능 담당
  <div align=center> 
    
  |**주요 기능**|**역할 파트**|
  |:--------:|:------:|
  |현재 상품(Product) 보관 및 집기|Product Entrance, IR Sensor, Color Sensor, <br> CDS Sensor, Robot Arm, Basket|
  |작업자 따라 이동|Camera Sensor, DC Motor Driver, DC Motor x4|
  |작업자 인식|RFID Reader|
  |메인 PC 통신|Arduino Mega Board, Bluetooth Module|
  
  </div> 

#### 2. HW 설계도
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/17d6660c-9b57-4b0c-b681-5e0dc8fa3f23" width="800">
  </div> 
  
#### 3. SW 설계도
- SW 구성도
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/dbae9f79-c74f-41a3-b806-9fde058acdac" width="800">
  </div> 
  
- 명령어 흐름도
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/34cef795-b55a-41d5-b2f5-bcb173bb0ae1" width="1000">
  </div> 
  
- 블루투스 통신 프로토콜
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/6af1c3fa-3447-46ce-b785-5e84250cb4a3" width="400">
  </div> 
  
  ##### Arduino -> PC
  - 시리얼 통신 대상 센서들의 I/O 상태 플래그 PC로 전송
  - **OF**: 카메라 통한 작업자 추적 성공 여부(T/F)
  - **CS**: 컬러 센서 통한 현재 상품 RGB 값의 기준 RGB 값과 일치 여부(T/F)
  - **ID**: RFID 리더기 통해 읽은 TAG Data
  ##### PC -> Arduino
  - PC로부터 명령어 보드로 전송
  - **PF**: 전원인가 여부(T/F)
  - **EM**: 비상정지 여부(T/F)
  - **FN**: 작업완료 알람 여부(T/F)

### GUI

<div align=center>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/02c5e443-8844-4a24-974c-fe21710c53b1" width="400">
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/5d555d85-e1a2-43b8-bb7e-6d8ca1911894" width="400">
    <br>
  <div align=center> 
  (1) 로그인 화면&emsp;&emsp;&emsp;(2) 회원가입 화면
  </div>    
</div>
  <br>  <br>
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/9344330c-9697-4a7c-b918-735200868f6d" width="400">
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/e01d4e1d-9a2f-449c-8b7a-e7ed5e62a7b4" width="400">
    <br>
   <div align=center> 
  (3) 작업자 화면&emsp;&emsp;&emsp;(4) 관리자 화면
  </div>    
  </div>


### 시퀀스 다이어그램
#### 1-1. 미등록 작업자 등록 후 로그인 완료 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/8f78b038-9988-4ee2-b1e7-cd648871e7cd" width="600">
  </div>
  
#### 1-2. 목표작업량 달성 후 로그아웃 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/c2bbf856-7525-4ec3-bf29-c2cfb831fc2c" width="600">
  </div>
  
#### 2-1. 등급별 정돈(양품) 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/a20df8ae-efd0-4630-ba8c-d1dcf0bb5c77" width="600">
  </div>
  
#### 2-2. 등급별 정돈(불량품) 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/860ea7ce-d831-4ff2-a683-64a036aff4e4" width="600">
  </div>
  
#### 2-3. 등급별 정돈(작업 대상 부재) 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/d1ae2893-fe9c-423b-9caa-2252cbd1cf1b" width="600">
  </div>
  
#### 3-1. 작업자 따라 이동(정상) 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/a50b97ec-1439-47df-931e-ae43675cbaad" width="600">
  </div>
  
#### 3-2. 작업자 따라 이동(실패) 시나리오
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/31fb921c-a3fa-45d0-90fd-32556e103a4a" width="600">
  </div>
  
------------------
### 시연영상
- 단위: 5 FPS
- [동영상 압축](https://www.veed.io/tools/video-compressor?locale=ko-KR&source=%2Ftools%2Fvideo-compressor%2Fgif-compressor)
- [GIF 파일 변환](https://gifmaker.me/video-to-gif/)
  
#### 1-1. 미등록 작업자 등록 후 로그인 완료 시나리오 시연
- 작업요청 -> 작업자 ID 전송 -> 로그인 정보(PW) 입력 -> 로그인 시도
  - **DB에 등록된 로그인 정보(ID/PW) NO** -> 새로운 작업자 정보(**이름, ID, PW, 개별작업량**) DB 등록 -> 로그인 재시도
  - **DB에 등록된 로그인 정보(ID/PW) YES** -> 로그인 성공
    
  <div align=center> 
  <br/>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/a5a9b808-2642-4b22-af32-21575438498c" height ="400">
  </div>
  
#### 1-2. 목표작업량 달성 후 로그아웃 시나리오 시연
- 작업요청 -> 로그인 성공 -> **DB 출근 여부('AT_WORK') 열 업데이트(N -> Y)** & 로봇 전원 ON -> 작업시작
- 목표작업량 달성 -> 로그아웃 시도 성공 -> **DB 출근 여부('AT_WORK') 열 업데이트(Y -> N)** & 목표달성 신호 -> 작업종료
  <div align=center> 
  <br/>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/e8d7e63c-73d7-4666-8598-b95cf86a9f2f" height ="600">
  </div>
  
#### 2-1. 등급별 정돈(양품) 시나리오 시연
- 양품(🔴 공) 정돈 
  <div align=center> 
  <br/>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/9b683557-4136-4b34-99e5-6262ea75fee7" width="400">
  </div>
  
#### 2-2. 등급별 정돈(불량품) 시나리오 시연
- 불량품(🟢 공) 정돈 
  <div align=center> 
  <br/>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/9622de9b-a5d0-40e2-b972-f4f82bd16925" width="400">
  </div>
  
#### 2-3. 등급별 정돈(작업 대상 부재) 시나리오 시연
- 1차 로봇팔 집기 동작 -> 대기 상태 -> 인식 상태 -> 2차 로봇팔 집기 동작
  <div align=center> 
  <br/>
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/3d5b4c53-b2a8-4e37-ac24-63cf3014d26b" width="400">
  </div>
  
#### 3-1. 작업자 따라 이동(정상) 시나리오 시연
- 전진
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/4e87148d-480e-4ddf-882e-c0e9bc4e6712" width="400">
  </div>

- 우회전
  - Stop -> **Right** -> Forward
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/b17fe979-8239-4dde-aea0-10ae2f0fa378" width="400">
  </div>
  
- 좌회전
  - Stop -> **Left** -> Forward
  <div align=center> 
  <img src="https://github.com/addinedu-ros-5th/iot-repo-2/assets/113625699/456a4eeb-384d-49db-8471-1f9d03fdcd8a" width="400">
  </div>

  ------------------
  #### 협업 툴 링크
  - [컨플루언스 - 회의록](https://iotrepo2.atlassian.net/wiki/spaces/PM/pages/98675)
  - [JIRA - 칸반보드](https://iotrepo2.atlassian.net/jira/software/projects/IT/boards/1?atlOrigin=eyJpIjoiNDJjOGVjNWExMzMyNDgwYWJlYmU5ZTdmYTMzNTU4M2EiLCJwIjoiaiJ9)

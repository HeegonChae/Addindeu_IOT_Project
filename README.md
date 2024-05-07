# iot-repo-2
IoT 프로젝트 2조 저장소. 농작물 수거 

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

## 프로젝트 설계
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
  
### GUI

## 실행 방법

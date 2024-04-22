# iot-repo-2
IoT 프로젝트 2조 저장소. 농작물 수거 

***
## 실행 방법
### 보드 <-> PC 통신
#### Ubuntu 포트 찾기 명령어
```
sudo dmesg |  tail
```
#### 포트 목록 확인
```
ls /dev/tty* # 일반적인 시리얼 포트 리스트 확인 
ls /dev/rfcomm* # rfcomm 장치 리스트 확인
```
#### 권한 확인
- 예시 장치 파일(**/dev/rfcomm0**)
```
ls -l /dev/rfcomm0
```
#### 권한 부여
- 모든 사용자가 해당 장치 파일에 읽고 쓸 수 있도록 권한 설정
```
sudo chmod 666 /dev/rfcomm0
```
#### 통신 테스트
```
import serial
import time

# 시리얼 포트 설정 (아두이노 연결된 포트로 변경)
serial_port = '/dev/ttyACM0'  # 예시로 '/dev/ttyUSB0'를 사용하였습니다.
baud_rate = 9600              # 아두이노와 동일한 통신 속도로 설정

# 시리얼 포트 초기화
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # PC에서 아두이노로 데이터 전송
        ser.write(b'Hello from PC\n')
        print("Data sent to Arduino")

        # 아두이노로부터 데이터 수신 및 출력
        received_data = ser.readline().decode().strip()
        print("Received data from Arduino:", received_data)  
        time.sleep(1)          # 1초 대기
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()                # 시리얼 포트 닫기
```
#### 블루투스 연결
```
sudo apt install blueman
```
- GGYUL 연결 (비밀번호 1234)
- 연결 안 될 경우 bluetooth manager에서 Serial Port 클릭

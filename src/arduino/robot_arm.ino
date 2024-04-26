#include <Servo.h>
#include <SoftwareSerial.h>

#define S0 41
#define S1 42
#define S2 29
#define S3 30
#define sensorOut 31


//서보모터 구조체
struct ServoControl {
    Servo servo;
    int currentPosition; //현재 위치
    int targetPosition; //목표 위치
    unsigned long lastUpdate; //타이머 동작을 위한 변수
    int updateInterval; //타이머 주기
};
ServoControl servoControls[6];

const int LED =13;
int speedDelay = 20;

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
bool CS = false; //컬러센서 변수
int light;
int light2;
int light3 ;
int sensorValue = 0;

bool isPositionReached = false;



unsigned long previousMillis1 = 0; // 1번 타이머
unsigned long previousMillis2 = 0; // 2번 타이머

unsigned long time1 = 1500;
unsigned long time2 = 500;

//로봇팔 제어를 위한 flag
int flag =0;
int operating_flag =0;
int operate_flag =0;
int grip_flag =0;
int turn1_flag =0;
int turn2_flag =0;

//타켓 포지션 설정 후 해당위치로 이동
void updateServoPosition(ServoControl &servoControl, int targetPosition) 
{
    servoControl.targetPosition = targetPosition; // 목표 위치 설정
    moveServoToPosition(servoControl);
}

void moveServoToPosition(ServoControl &servoControl) {
    unsigned long Millis = millis();
    // 서보의 현재 위치와 목표 위치의 차이 계산
    int positionDifference = servoControl.targetPosition - servoControl.currentPosition;

    if (Millis - servoControl.lastUpdate >= servoControl.updateInterval) {
        if (positionDifference != 0) {
            // 현재 위치를 목표 위치에 가깝게 조정
            int moveStep = positionDifference > 0 ? 1 : -1;
            servoControl.currentPosition += moveStep;
            servoControl.servo.write(servoControl.currentPosition);
            servoControl.lastUpdate = Millis; // 마지막 업데이트 시간 갱신
        }
    }
}



//상품 정상, 불량 판별
void colorSensor() {
  //빨간색
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  redFrequency = pulseIn(sensorOut, LOW);
  
  //초록색
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  

  greenFrequency = pulseIn(sensorOut, LOW);
  
  //파란색
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  
  blueFrequency = pulseIn(sensorOut, LOW);

  if ((redFrequency > 40) && (redFrequency < 75) && (greenFrequency > 95) && (greenFrequency < 120) && (blueFrequency > 55) && (blueFrequency < 75))
  {
    CS = 1;
  }
  else 
  {
    CS = 0;
  }

  delay(10);
}

void setup() {
  Serial.begin(9600);
  servoControls[0].servo.attach(2);
  servoControls[1].servo.attach(3);
  servoControls[2].servo.attach(4);
  servoControls[3].servo.attach(5);
  servoControls[4].servo.attach(6);
  servoControls[5].servo.attach(7);
 

  int initialPositions[6] = {90, 140, 150, 8, 100, 165}; // 각 서보의 초기 위치 설정

  for (int i = 0; i < 6; i++) 
    {
        servoControls[i].currentPosition = initialPositions[i]; // 배열에서 초기 위치 가져오기
        servoControls[i].servo.write(initialPositions[i]); // 서보를 초기 위치로 설정
        servoControls[i].lastUpdate = millis(); // 마지막 업데이트 시간 초기화
        servoControls[i].updateInterval = 5; // 업데이트 간격 설정
    }

  
  pinMode(LED, OUTPUT);
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  digitalWrite(LED, HIGH);
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);

  delay(300);
  
   light = analogRead(A0) ;
   light2 = analogRead(A1) ;
   light3 = analogRead(A2) ;
}

void loop()
{    
  sensorValue = analogRead(A3);
  Serial.print("dis");
  Serial.println(sensorValue);
  unsigned long currentMillis = millis();

  if (sensorValue > 700 || operating_flag ==1)
  {
   
    operating_flag =1;

    //그립 동작 시작하지 않았을 경우
    if(grip_flag == 0)
    {
       colorSensor();
       previousMillis1 = currentMillis;

        
        if(operate_flag ==0)
        {
          
          updateServoPosition(servoControls[2], 162);
          Serial.println("servo03 1");
          updateServoPosition(servoControls[4], 133);
          Serial.println("servo05 1");
          updateServoPosition(servoControls[1], 100); 
          Serial.println("servo02 1");
          updateServoPosition(servoControls[5], 100);
          Serial.println("servo06 1");
          
          //모든 서보모터가 목표 위치에 도달했는지 확인
         if (servoControls[2].servo.read() != 162 || servoControls[4].servo.read() != 133 || servoControls[1].servo.read() != 100 || servoControls[5].servo.read() != 100) 
          {
             updateServoPosition(servoControls[2], 162);
            Serial.println("servo03 1");
            updateServoPosition(servoControls[4], 133);
            Serial.println("servo05 1");
            updateServoPosition(servoControls[1], 100); 
            Serial.println("servo02 1");
            updateServoPosition(servoControls[5], 100);
            Serial.println("servo06 1");
          }

          else 
          {
            operate_flag =1;
          }
        }


        else if (operate_flag ==1)
        {
          updateServoPosition(servoControls[1], 125);
          Serial.println("servo02 2");
          Serial.println(servoControls[1].servo.read());
          if (servoControls[1].servo.read() == 125)
          {
            Serial.println("All servos reached their target positions.");
            Serial.println("one stap done");
            
            currentMillis = millis();
            previousMillis1 = currentMillis;
            Serial.print("previous");
            Serial.println(previousMillis1);
            grip_flag =1;
          }
        } 
      } 
      

     
    //그립 동작 시작했을 경우
    if ((currentMillis - previousMillis1) >= time1 && grip_flag ==1)
    {
      previousMillis2 = currentMillis;
      
      light = analogRead(A0);
      light2 = analogRead(A1);
      light3 = analogRead(A2);


      if( flag ==0)
      {
        //정상품
        if (CS == 1)
        {
          Serial.println(flag);
          Serial.println("turn 2");

          Serial.println(light2);
          servoControls[0].servo.write(85);

          if(light2>65)
          {
            light2 = analogRead(A1);
            Serial.println(light2);
            servoControls[0].servo.write(90);
            turn1_flag = 1;
            flag=1;
          }
          
        }
        
      //불량품
      else
      {
        
        Serial.println(light3);
        servoControls[0].servo.write(85);
        if(light3>160)
        {
          light3 = analogRead(A2);
          Serial.println(light3);
          servoControls[0].servo.write(90);
          updateServoPosition(servoControls[4], 145);
          if(servoControls[4].servo.read() ==145)
          {
            flag=1;
            turn2_flag =1;
          }
        } 
        
      }

      }

      //turn1 또는 turn2가 활성화된 경우, 서보모터 위치 조정
      if(turn1_flag ==1 || turn2_flag ==1)
      {
       
        Serial.println(CS);

        if (servoControls[1].servo.read() !=90 && servoControls[5].servo.read() !=170)
          {
            updateServoPosition(servoControls[1], 90);
            Serial.println("servo02 3");
            updateServoPosition(servoControls[5], 170);
            Serial.println("servo06 2");
          }
        
        else 
         {
          updateServoPosition(servoControls[1], 130);
           Serial.println("servo02 4");
           Serial.println(servoControls[1].servo.read());

          if(servoControls[1].servo.read() ==130)
          {
            Serial.println("time 2 on");
            currentMillis = millis();
            previousMillis1 = currentMillis;
            previousMillis2 = currentMillis;
            
            
          }
        }
        
      }
  

    }

    //두번째 타이머 시간이 경과했을 때
    if (currentMillis - previousMillis2 >= time2)
    { 
   
      if (flag ==1)
      {
    
        Serial.println(flag);
        light = analogRead(A0);
        light2 = analogRead(A1);
        light3 = analogRead(A2);
        Serial.println("turn 1");
        servoControls[0].servo.write(100);
        if(light>870)
        {
          light = analogRead(A0);
          Serial.println(light);
          servoControls[0].servo.write(90);
          flag=0;
          grip_flag =0;
          turn1_flag =0;
          turn2_flag =0;
          currentMillis = millis();
          previousMillis1 = currentMillis;
          previousMillis2 = currentMillis;
          operating_flag =0;
        }

      }
    }

  }
    
    //센서 값이 조건을 만족하지 않았을 경우 기본 위치로 이동
    else 
    {
      
      delay(200);
    }

 
  }
 
  
  
  

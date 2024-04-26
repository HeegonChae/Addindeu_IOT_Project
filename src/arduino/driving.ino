#include "HUSKYLENS.h"
#include "SoftwareSerial.h"
HUSKYLENS huskylens;
SoftwareSerial mySerial(10, 11);

void printResult(HUSKYLENSResult result);
void setup() {
    Serial.begin(115200);
    mySerial.begin(9600);
    pinMode (32, OUTPUT);
    pinMode (33, OUTPUT);
    pinMode (34, OUTPUT);
    pinMode (37, OUTPUT);
    pinMode (35, OUTPUT);
    pinMode (36, OUTPUT);
    //허스키렌즈가 성공적으로 시작될 때까지 반복
    while (!huskylens.begin(mySerial))
    {
        Serial.println(F("Begin failed!"));
        Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS (General Settings>>Protocol Type>>Serial 9600)"));
        Serial.println(F("2.Please recheck the connection."));
        delay(100);
    }
}
void loop()
{
    if (!huskylens.request())
    Serial.println(F("Fail to request data from HUSKYLENS, recheck the connection!")); //데이터 요청 실패
    else if(!huskylens.isLearned())
    Serial.println(F("Nothing learned, press learn button on HUSKYLENS to learn one!")); //학습 데이터 없음
    else if(!huskylens.available())
    {
      Serial.println(F("No block or arrow appears on the screen!")); //화면에 객체 없음
      stop();

    }

    else
    {
        Serial.println(F("###########"));
        while (huskylens.available())
        {
            HUSKYLENSResult result = huskylens.read();
            printResult(result);
            driveBot(result);
        }
    }
}
//결과 데이터를 시리얼 모니터에 출력
void printResult(HUSKYLENSResult result){
    if (result.command == COMMAND_RETURN_BLOCK){
        Serial.println(String()+F("Block:xCenter=")+result.xCenter+F(",yCenter=")+result.yCenter+F(",width=")+result.width+F(",height=")+result.height+F(",ID=")+result.ID);
    }
    else if (result.command == COMMAND_RETURN_ARROW){
        Serial.println(String()+F("Arrow:xOrigin=")+result.xOrigin+F(",yOrigin=")+result.yOrigin+F(",xTarget=")+result.xTarget+F(",yTarget=")+result.yTarget+F(",ID=")+result.ID);
    }
    else{
        Serial.println("Object unknown!");
    }
}
//로봇 구동 로직 처리
void driveBot(HUSKYLENSResult result)
{
  if(result.xCenter<=70)
  {
    left();
    
  }
  else if(result.xCenter>=270)
  {
    right();
    
  }
    else if((result.xCenter>=70)&&(result.xCenter<=270))
  {
    if(result.width<=30)
    {
      forward();
    }
    else
    {
      stop();
    }
  }
}
void stop()
{
digitalWrite(32, LOW);
digitalWrite(33, LOW);
digitalWrite(37, LOW);
digitalWrite(34, LOW);
Serial.println("Stop");
}
void left()
{
digitalWrite(32, HIGH);
digitalWrite(33, LOW);
digitalWrite(37, LOW);
digitalWrite(34, HIGH);

analogWrite(35, 130);
analogWrite(36, 200);
Serial.println(" Rotate Left");
}
void right()
{
digitalWrite(32, LOW);
digitalWrite(33, HIGH);
digitalWrite(37, HIGH);
digitalWrite(34, LOW);

analogWrite(35, 130);
analogWrite(36, 200);
Serial.println(" Rotate Right");
}
void forward()
{
digitalWrite(32, LOW);
digitalWrite(33, HIGH);
digitalWrite(37, LOW);
digitalWrite(34, HIGH);
analogWrite(35, 130);
analogWrite(36, 200);
Serial.println("Forward");
}
void backward()
{
digitalWrite(32, HIGH);
digitalWrite(33, LOW);
digitalWrite(37, HIGH);
digitalWrite(34, LOW);
Serial.println("Forward");
}

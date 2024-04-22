#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_PIN          10         // Configurable, see typical pin layout above

SoftwareSerial BTSerial(3, 2); //Tx_PIN, Rx_PIN

MFRC522 rc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
MFRC522::MIFARE_Key key;



void setup() {
	Serial.begin(9600);		// Initialize serial communications with the PC
	BTSerial.begin(9600);
  SPI.begin();
  rc522.PCD_Init();
  for (int i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF;
  }
}

void loop() {
	// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( ! rc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards
	if ( ! rc522.PICC_ReadCardSerial()) {
		return;
	}

  MFRC522::StatusCode status;
  status = rc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 60, &key, &(rc522.uid));
  if (status != MFRC522::STATUS_OK)
  {
    return;
  }

	// Dump debug info about the card; PICC_HaltA() is automatically called

  String uidString = "";
  for (byte i = 0; i < rc522.uid.size; i++)
  {
    uidString += (rc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    uidString += String(rc522.uid.uidByte[i], HEX);
  }

  uidString.toUpperCase();

  
  BTSerial.println(String("ID") + uidString);
  Serial.println(String("ID") + uidString);
  
  rc522.PICC_HaltA();
  rc522.PCD_Init();

  delay(1000);

}

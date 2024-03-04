#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          
#define SS_PIN          10         
MFRC522 mfrc522(SS_PIN, RST_PIN);

const byte bambooshootUID[] = {0xA3, 0xD8, 0x56, 0x17};
const byte shrimpUID[] = {0xE4, 0x60, 0x0B, 0x1E};
const byte steamUID[] = {0x93, 0x28, 0x93, 0x24};

bool card1Scanned = false;
bool card2Scanned = false;
bool card3Scanned = false;

void setup() {
    Serial.begin(9600);
    while (!Serial);
    SPI.begin();
    mfrc522.PCD_Init();
    delay(4);
    // mfrc522.PCD_DumpVersionToSerial();
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    if (isCardUIDMatch(mfrc522.uid.uidByte, bambooshootUID, mfrc522.uid.size)) {
        if (!card1Scanned) {
            Serial.println(F("bambooshoot"));
            card1Scanned = true;
        }
    } else if (isCardUIDMatch(mfrc522.uid.uidByte, shrimpUID, mfrc522.uid.size)) {
        if (!card2Scanned) {
            Serial.println(F("shrimp"));
            card2Scanned = true;
        }
    } else if (isCardUIDMatch(mfrc522.uid.uidByte, steamUID, mfrc522.uid.size)) {
        if (!card3Scanned) {
            Serial.println(F("steam"));
            card3Scanned = true;
        }

    if (card1Scanned && card2Scanned && card3Scanned) {
        // Serial.println(F("You cooked Har Gow!"));
        card1Scanned = false;
        card2Scanned = false;
        card3Scanned = false;
    }

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1(); 
}}

bool isCardUIDMatch(byte *cardUID, const byte *knownUID, byte size) {
    for (byte i = 0; i < size; i++) {
        if (cardUID[i] != knownUID[i]) {
            return false;
        }
    }
    return true;
}

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          
#define SS_PIN          10         
MFRC522 mfrc522(SS_PIN, RST_PIN);

const byte card1UID[] = {0xA3, 0xD8, 0x56, 0x17};
const byte card2UID[] = {0xE4, 0x60, 0x0B, 0x1E};

bool card1Scanned = false;
bool card2Scanned = false;

void setup() {
    Serial.begin(9600);
    while (!Serial);
    SPI.begin();
    mfrc522.PCD_Init();
    delay(4);
    mfrc522.PCD_DumpVersionToSerial();
    Serial.println(F("Mix the ingredients now!"));
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    if (isCardUIDMatch(mfrc522.uid.uidByte, card1UID, mfrc522.uid.size)) {
        if (!card1Scanned) {
            Serial.println(F("Added Tapioca Starch!"));
            card1Scanned = true;
        }
    } else if (isCardUIDMatch(mfrc522.uid.uidByte, card2UID, mfrc522.uid.size)) {
        if (!card2Scanned) {
            Serial.println(F("Added Shrimp!"));
            card2Scanned = true;
        }
    }

    if (card1Scanned && card2Scanned) {
        Serial.println(F("You cooked Har Gow!"));
        card1Scanned = false;
        card2Scanned = false;
    }

    mfrc522.PICC_HaltA(); // Halt PICC
    mfrc522.PCD_StopCrypto1(); // Stop encryption on PCD
}

bool isCardUIDMatch(byte *cardUID, const byte *knownUID, byte size) {
    for (byte i = 0; i < size; i++) {
        if (cardUID[i] != knownUID[i]) {
            return false;
        }
    }
    return true;
}

#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    Serial.println("{\"status\":\"boot\",\"device\":\"open-potentiostat-esp32\",\"fw\":\"0.1.0\"}");
}

void loop() {
    while (Serial.available()) {
        String line = Serial.readStringUntil('\n');
        line.trim();
        if (line == "{\"cmd\":\"ping\"}") {
            Serial.println("{\"status\":\"ok\",\"device\":\"open-potentiostat-esp32\",\"fw\":\"0.1.0\"}");
        }
    }
}

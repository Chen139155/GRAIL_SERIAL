#include <ArduinoJson.h>
#include <Wire.h>

#define MCP4725_1 0x60  // 第一片 DAC
#define MCP4725_2 0x61  // 第二片 DAC
#define MCP4725_3 0x62  // 第三片 DAC（如果支持）
#define MCP4725_4 0x63  // 第四片 DAC（如果支持）
// 本接口实现仅支持两片

float dac_voltages[4] = { 0, 0, 0, 0 };  // 存储 4 个 DAC 的电压

void setup() {
  Serial.begin(2000000);
  Wire.begin();
  // pinMode(3, OUTPUT);  // PWM 通道
  pinMode(A0, INPUT);   // ADC 读取通道
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(62, OUTPUT);
  pinMode(63, OUTPUT);
  pinMode(64, OUTPUT);
  pinMode(65, OUTPUT);
  pinMode(66, OUTPUT);
  pinMode(67, OUTPUT);
  pinMode(68, OUTPUT);
  pinMode(69, OUTPUT);
  DDRA = 0xFF;         // 设置 PORTA（D22-D29）为 8 位数字输出
  DDRK = 0xFF;
  DDRC = 0x00;
  DDRL = 0x00; 
  PORTC = 0xFF;
  PORTL = 0xFF;
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    StaticJsonDocument<200> doc;

    DeserializationError error = deserializeJson(doc, input);
    if (error) return;  // 解析失败则跳过

    int ch = doc["ch"];
    String mode = doc["mode"];
    String chtype = doc["chtype"];

    if (mode == "write") {
      if (chtype == "digital") {
        int value = doc["value"];
        digitalWrite(ch, value);
      } else if (chtype == "analog") {
        float value = doc["value"];
        if (ch >= 0 && ch < 4 && value >= 0.0 && value <= 5.0) {
            dac_voltages[ch] = value;
            updateDAC(getAddress(ch), value, false);
        }
      } else if (chtype == "digital_8bit") {
        int value = doc["value"];
        if (ch == 0){
          PORTA = value & 0xFF;
        } else if (ch == 1){
          PORTK = value & 0xFF;
        }
      }
    } else if (mode == "read") {
      StaticJsonDocument<200> response;
      response["ch"] = ch;
      response["chtype"] = chtype;

      if (chtype == "digital") {
        response["value"] = digitalRead(ch);
      } else if (chtype == "analog") {
        response["value"] = analogRead(ch+54); // ch0-3表示54-57号引脚
      } else if (chtype == "digital_8bit") {
        if (ch == 0){
          response["value"] = PINC;  // 读取 PORTB
        } else if (ch == 1){
          response["value"] = PINL;  // 读取 PORTC
        }
        
      }

      String jsonResponse;
      serializeJson(response, jsonResponse);
      Serial.println(jsonResponse);
    }
  }
}

void updateDAC(uint8_t address, float voltage, bool writeEEPROM) {
  uint16_t dac_value = (uint16_t)(voltage / 5.0 * 4095);

  Wire.beginTransmission(address);
  Wire.write(writeEEPROM ? 96 : 64);  // 0x60 = EEPROM, 0x40 = RAM
  Wire.write(dac_value >> 4);
  Wire.write((dac_value & 15) << 4);
  Wire.endTransmission();
}

uint8_t getAddress(int channel) {
    switch (channel) {
        case 0: return MCP4725_1;
        case 1: return MCP4725_2;
        case 2: return MCP4725_3;
        case 3: return MCP4725_4;
        default: return MCP4725_1;
    }
}
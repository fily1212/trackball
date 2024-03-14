#include <ArduinoJson.h>
#include <string.h>

StaticJsonDocument<200> docSend;
int bl=2;
int rl=3;
int gl=4;
int v=0;
char a;
void setup() {
  
  Serial.begin(9600);
  pinMode(bl,OUTPUT);
  pinMode(rl,OUTPUT);
  pinMode(gl,OUTPUT);
  digitalWrite(bl,LOW);
  digitalWrite(rl,LOW);
  digitalWrite(gl,LOW);

  bon();
  delay(100); // Aspetta per 100 millisecondi
  boff();

  ron();
  delay(100); // Aspetta per 100 millisecondi
  roff();

  gon();
  delay(100); // Aspetta per 100 millisecondi
  goff();
  
  docSend["flinesensor"]= false;  //forward line sensor
  docSend["blinesensor"]= false;  //backward line sensor
}


void boff(){
  digitalWrite(bl,0);
  //Serial.println("Off");
  delay(100);
}


void bon(){
  digitalWrite(bl,1);
  //Serial.println("On");
  delay(100);
}
void roff(){
  digitalWrite(rl,0);
  //Serial.println("Off");
  delay(100);
}


void ron(){
  digitalWrite(rl,1);
  //Serial.println("On");
  delay(100);
}
void goff(){
  digitalWrite(gl,0);
  //Serial.println("Off");
  delay(100);
}


void gon(){
  digitalWrite(gl,1);
  //Serial.println("On");
  delay(100);
}



void loop() {

      delay(300);
      serializeJson(docSend,Serial);
      Serial.println();
      if(Serial.available()>0){
        StaticJsonDocument<500> docReceive;
        DeserializationError error=deserializeJson(docReceive,Serial);

        if(error){
         
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.c_str());
        return;
          return;
        }
        const char* cmd =docReceive["cmd"];

        if (strcmp(cmd, "forward") == 0) {
            goff();
            boff();
            ron();
        } else if (strcmp(cmd, "back") == 0) {
            roff();
            bon();
            gon();
        } else if (strcmp(cmd, "right") == 0) {
            roff();
            boff();
            gon();
        } else if (strcmp(cmd, "left") == 0) {
            roff();
            goff();
            bon();
        } else {
            boff();
            roff();
            goff();
        }

      }
 
}
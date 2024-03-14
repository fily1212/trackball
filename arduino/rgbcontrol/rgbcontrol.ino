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
}


void boff(){
  digitalWrite(bl,0);
  Serial.println("Off");
  delay(100);
}


void bon(){
  digitalWrite(bl,1);
  Serial.println("On");
  delay(100);
}
void roff(){
  digitalWrite(rl,0);
  Serial.println("Off");
  delay(100);
}


void ron(){
  digitalWrite(rl,1);
  Serial.println("On");
  delay(100);
}
void goff(){
  digitalWrite(gl,0);
  Serial.println("Off");
  delay(100);
}


void gon(){
  digitalWrite(gl,1);
  Serial.println("On");
  delay(100);
}



void loop() {

  
  
if (Serial.available()>0){
  a=Serial.read();
  
  if(a=='b'){
    if(digitalRead(bl)==LOW){
    Serial.println("was off, now on");
    bon();
    }else{
      Serial.println("was on,now off");
      boff();
    }
  }else if(a=='r'){
     if(digitalRead(rl)==LOW){
    Serial.println("was off, now on");
    ron();
    }else{
      Serial.println("was on,now off");
      roff();
  }
  }else if(a=='g'){
    if(digitalRead(gl)==LOW){
    Serial.println("was off, now on");
    gon();
    }else{
      Serial.println("was on,now off");
      goff();
  }
  }
}
}



int LED1 = 13;
int incomingData;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as output.
  pinMode(LED1, OUTPUT);
  // begin serial comm, with 9600 baud rate
  Serial.begin(9600);
}

void dot(int dur)
{
  digitalWrite(LED1, HIGH);
  delay(dur);
  digitalWrite(LED1, LOW);
  delay(dur);
}
// the loop function runs over and over again forever
void loop() {
  // if hardware serial comms available (i.e bluetooth)
  if (Serial.available() > 0) {

    // read data from bluetooth reciver
    incomingData = Serial.read();

    if (incomingData == 'B') {
      // HIGH voltage = turn on
      digitalWrite(LED1, HIGH);
      delay(1000);
      digitalWrite(LED1, LOW);
      delay(1000);
    }

    if (incomingData == 'H') {
      digitalWrite(LED1, HIGH);
    }

    if (incomingData == 'L') {
      digitalWrite(LED1, LOW);
    }

    if (incomingData == 'S') {
      for(int i = 0; i < 100; i++)
      {
        dot(100);
        dot(100);
        dot(100);
        delay(500);
        dot(300);
        dot(300);
        dot(300);
        delay(500);
        dot(100);
        dot(100);
        dot(100);

        delay(1000);
      }
      
    }
}
}

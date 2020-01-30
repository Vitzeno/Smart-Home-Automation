int LED1 = 13;
int incomingData;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as output.
  pinMode(LED1, OUTPUT);
  // begin serial comm, with 9600 baud rate
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  // if hardware serial comms available (i.e bluetooth)
  if (Serial.available() > 0) {

    // read data from bluetooth reciver
    incomingData = Serial.read();
    if (incomingData == 'b') {
      // HIGH voltage = turn on
      digitalWrite(LED1, HIGH);
      delay(1000);
      digitalWrite(LED1, LOW);
      delay(1000);
    }

    if (incomingData == '1') {
      digitalWrite(LED1, HIGH);
    }

    if (incomingData == '0') {
      digitalWrite(LED1, HIGH);
    }

  }
}

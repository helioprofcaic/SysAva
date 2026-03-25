// C++ code
//
int pinoOito = 0;

int pinoSete = 0;

void setup()
{
  pinMode(8, INPUT);
  pinMode(7, OUTPUT);

  pinoOito = digitalRead(8);
  pinoSete = 0;
  digitalWrite(7, LOW);
}

void loop()
{
  delay(1000); // Wait for 1000 millisecond(s)
  if (digitalRead(8) < 1) {
    digitalWrite(7, HIGH);
  }
}
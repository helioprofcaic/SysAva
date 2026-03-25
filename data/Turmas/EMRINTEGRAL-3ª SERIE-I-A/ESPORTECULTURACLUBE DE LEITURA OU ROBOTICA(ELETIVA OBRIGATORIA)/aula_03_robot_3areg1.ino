// C++ code
//
void setup()
{
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(8, LOW);
  digitalWrite(7, LOW);
}

void loop()
{
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(8, HIGH);
  digitalWrite(7, LOW);
  delay(5000); // Wait for 5000 millisecond(s)
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(8, LOW);
  digitalWrite(7, HIGH);
  delay(5000); // Wait for 5000 millisecond(s)
}
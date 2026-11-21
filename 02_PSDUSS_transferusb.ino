void setup() {
  // Initialize serial communication at 9600 baud
  Serial.begin(115200);
}

void loop() {
  // Read analog values from A0 and A1
  int valueA0 = analogRead(A0);
  int valueA1 = analogRead(A1);
  
  // Send values as a comma-separated string
  Serial.print(valueA0);
  Serial.print(",");
  Serial.println(valueA1);
  
  // Small delay to prevent flooding the serial port
  delay(100); 
}
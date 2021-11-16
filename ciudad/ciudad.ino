/*========================= SANXOFON ==========================//
 Genera un número aleatorio de 21 cifras y lo escribe en serial
//========================= SANXOFON ==========================*/


long randNumber;         // the variable which is supposed to hold the random number
String cadena = String(0); // 21 caracteres
void setup()
{
  // initialize the serial port
  Serial.begin(9600);
  // initialize the pseudo-random number generator
  randomSeed(analogRead(0));
}

void loop()
{
  if (random(0, 30)==0) {
    for (int i = 0; i < 21; ++i) {
      if(i==0){
        cadena = String(random(0, 9));
      } else {
        cadena = cadena + random(0, 9); // generate a random number adn add to string
      }                                 
    }
    Serial.println(cadena);
  } //else {
    //if (random(0, 9)==0) {
      //Serial.println(cadena);
    //}
  //}                                               // send the random number to the serial port
  delay(300);
}
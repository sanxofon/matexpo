/*========================= SANXOFON ==========================//
 Genera un número aleatorio de 21 cifras y lo escribe en serial
//========================= SANXOFON ==========================*/


String cadena; // 21 caracteres
int ii=0;
void setup()
{
  // initialize the serial port
  Serial.begin(9600);
  // initialize the pseudo-random number generator
  randomSeed(analogRead(0));
}

void loop()
{
      if (ii==0) {
        cadena = String(random(0, 9));
      } else {
        cadena = cadena + random(0, 9); // generate a random number adn add to string
      }
      ii++;                  
    String cadenout=String(cadena);
    if(cadenout.length()<21){
      for (int i = ii; i < 21; ++i) {
        cadenout = cadenout + '0';
      }
    }
    Serial.println(cadenout);
    if(ii>=21) {
      ii=0;
      delay(100);
    } else {
      delay(100);
    }
}

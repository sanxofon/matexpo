// CARRIL 3 Esclavo. 
// Envia por serial 3 la informacion de su estado

//#include <Arduino.h>
static const uint8_t analog_pin [] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13};

// lectura sensor
int valH [14]   = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int r_valH [14] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};
// lectura calibracion cero
int z_valH [14] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};

// Codificacion primos
//int P [3][3] = {{1,2,3},{5,7,11},{13,17,19}};
int P [3][3] = {{0,1,2},{3,4,5},{6,7,8}};
byte Pb [3][3] = {{48,49,50},{51,52,53},{54,55,56}};

//Codifica primo en bytes
byte primo( int z, int d){
  int reso = 5;
  int tz=0;
  int td=0;

  if (abs(z) < reso) {tz = 0;}
  if (z > reso) {tz = 1;}
  if (z < -reso) {tz = 2;}

  if (abs(d) < reso) {td = 0;}
  if (d > reso) {td = 1;}
  if (d < -reso) {td = 2;}

  return Pb[tz][td];
}

//Codifica primo en bytes
int int_primo( int z, int d){
  int reso = 5;
  int tz=0;
  int td=0;

  if (abs(z) < reso) {tz = 0;}
  if (z > reso) {tz = 1;}
  if (z < -reso) {tz = 2;}

  if (abs(d) < reso) {td = 0;}
  if (d > reso) {td = 1;}
  if (d < -reso) {td = 2;}

  return P[tz][td];
}


// Calibra los sensores
void calibra(){
  for (int ii=0; ii<3; ii++){
    // Calibra lo sensores
    for (int i =0; i<14; i++){
      z_valH[i] = analogRead(analog_pin[i]);  
      // Solo para checar los valores inicales
      //Serial.print(z_valH[i]);
      //Serial.print(" ");
    }
    //Serial.println();
   delay(50);
  }
  // Si quieres que avise que termino de calibrar descomenta la siguiente 
  //Serial.println("OK!");
}


// edificio correspondiente
byte edificio [8] = {255,1,1,1,1,1,1,1};



class Piso {
  private:
    int n;
  public:
    Piso(int n) {
    this->n=n;
    }
  byte valor() {
    int val_A = analogRead(analog_pin[2*n ] ) - z_valH[2*n  ];  
    int val_B = analogRead(analog_pin[2*n+1]) - z_valH[2*n+1];  
    return primo(val_A,val_B);
  }
};

Piso piso1 = Piso(0);
Piso piso2 = Piso(1);
Piso piso3 = Piso(2);
Piso piso4 = Piso(3);
Piso piso5 = Piso(4);
Piso piso6 = Piso(5);
Piso piso7 = Piso(6);

void setup () {
  Serial.begin(9600);
  Serial3.begin(9600);
  delay(50);
  calibra();
  delay(50);
}

void loop(){
  Serial.println("Voy");
  delay(1000);
  
  edificio[1] = piso1.valor(); 
  edificio[2] = piso2.valor(); 
  edificio[3] = piso3.valor(); 
  edificio[4] = piso4.valor(); 
  edificio[5] = piso5.valor(); 
  edificio[6] = piso6.valor(); 
  edificio[7] = piso7.valor(); 

  
  for (int i=0; i<8; i++){
    Serial3.write( edificio[i] );
  }
  delay(300);


}

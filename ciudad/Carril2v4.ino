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

class Puerto {
  private:
    int puerto_serial;
    bool hay_mensaje;
    byte mensaje [8];
    String texto;
  public:
    Puerto (int puerto_serial) {
    this->puerto_serial = puerto_serial;
    }
  bool lectura () {
    HardwareSerial *serio;
    if (this->puerto_serial==2) {
      serio = &Serial2;
    } else {
      serio = &Serial3;
    }
    if (serio.available()){
        for (int i=0;i<8;i++) {
          mensaje[i] = serio.read();
//          Serial.print("A0 escucha: ");
//          Serial.print(mensaje[i]);
//          Serial.println();
        }
          hay_mensaje = 1;
        } 
      else {
//        Serial.println("A0:no hay serial.3");
        hay_mensaje = 0;
        }
      if (mensaje[0] != 255){
        hay_mensaje = 0;
        }
  return hay_mensaje;
  }
  String edificio (){
    texto = "";
    for (int i=1; i<8;i++){
      texto += (char) mensaje[i];
      }
    return texto;
  }
};


// Crea los puertos de los dos arduinos
Puerto3 puertoA = Puerto(3);
Puerto2 puertoB = Puerto(2);


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

String estado = "000000000000000000000";
String nuevo_estado = "";
String vecino_izquierda = "0000000";
String vecino_derecha =   "0000000";

void setup () {
  Serial.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  delay(100);
  calibra();
  delay(150);
  estado = "000000000000000000000";
  Serial.println(estado);
}

void loop(){
  delay(10);
  edificio[1] = piso1.valor(); 
  edificio[2] = piso2.valor(); 
  edificio[3] = piso3.valor(); 
  edificio[4] = piso4.valor(); 
  edificio[5] = piso5.valor(); 
  edificio[6] = piso6.valor(); 
  edificio[7] = piso7.valor(); 

//  Serial.print(" Mi edificio es: ");
  String miedificio = "";
  for (int i=1; i<8; i++){
    miedificio += (char)edificio[i];
    }
//    Serial.println(miedificio);
  delay(500);

  
  
  if(puertoA.lectura()>0){
//    Serial.print("Mi vecino de la derecha es:");
    vecino_derecha = puertoA.edificio();
    nuevo_estado = vecino_izquierda + miedificio + vecino_derecha;
//    Serial.println(vecino_derecha);
    }
  
  if(puertoB.lectura()>0){
//    Serial.print("Mi vecino de la izquierda es:");
    vecino_izquierda = puertoB.edificio();
    nuevo_estado = vecino_izquierda + miedificio + vecino_derecha;
//    Serial.println(vecino_izquierda);
    }

  if (nuevo_estado != estado) {
    for (int i=0; i<3;i++){
    Serial.println(nuevo_estado);
    delay(10);
    }
    estado = nuevo_estado;
    }  
    


}

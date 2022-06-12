#include <SparkFun_ADXL345.h>  // https://github.com/sparkfun/SparkFun_ADXL345_Arduino_Library
ADXL345 adxl = ADXL345();    // I2C통신이므로 이렇게 수정해야합니다.
int x,y,z;                     // XYZ축을 설정합니다.
 void setup(){                  
  Serial.begin(9600);          
  adxl.powerOn();              // ADXL345을 켭니다.
   adxl.setRangeSetting(4);     // 2g는 가장높은 감도이고, 4g, 8g,16g는 낮은 감도입니다. 감도를 자유롭게 설정하세요.
}
void loop(){                   
  adxl.readAccel(&x, &y, &z);  //  x, y, z를 읽습니다.
  sendAccelToProcessing();     // processing으로 값을 보냅니다.
  delay(30);                   // 0.03초 정도의 딜레이가 있습니다.
}
 void sendAccelToProcessing(){  // 프로세싱에 보낼 값입니다.
  Serial.print("x");           
  Serial.print(x);            
  Serial.print("y");          
  Serial.print(y);             
  Serial.print("z");          
  Serial.print(z);             
}
[출처] [Bitelab] 아두이노 자이로센서(ADXL345) 이용하기|작성자 bitelab


#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h> 
#include <ESP8266HTTPClient.h>


const char * ssid = "Integra";
const char * password = "Integra2023";

String serverName = "http://192.168.0.101:5000/api/sensor";

const int trigPin = 12;
const int echoPin = 14;

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;

void setup() {
  Serial.begin(9600); // Starts the serial communication
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input


  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());


}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_VELOCITY/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance on the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);

  // Verifica se o esp está conectado
  if (WiFi.status() == WL_CONNECTED) {  
    WiFiClient client;
    HTTPClient http;
    
    http.begin(client, serverName);

  // Specify content-type header
    http.addHeader("Content-Type", "application/json");
    // Data to send with HTTP POST
    String httpRequestData = "{\"distancia\":" + String(distanceCm) + "}";       
    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);
    //fechando a conexão

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    http.end();
  }
  
  delay(3000);
}
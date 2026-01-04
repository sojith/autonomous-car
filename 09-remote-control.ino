// Load Wi-Fi library
#include <WiFi.h>

// Replace with your network credentials
const char *ssid = "";
const char *password = "";

WiFiServer server(80);        // Set web server port number to 80

String header;  // Variable to store the HTTP request
String action;
String period;


// Assign output variables to GPIO pins
//const int output12 = 12;
//const int output14 = 14;
const int front = 13;
const int back = 15;
const int left = 19;
const int right = 32;

unsigned long currentTime = millis(); // Current time

unsigned long previousTime = 0;       // Previous time

const long timeoutTime = 200;        // Define timeout time in milliseconds (example: 2000ms = 2s)

void setup() {
  Serial.begin(115200);
 
  pinMode(front, OUTPUT);           // Initialize the output variables as outputs
  pinMode(back, OUTPUT);
  pinMode(left, OUTPUT);
  pinMode(right, OUTPUT);
  
  digitalWrite(front, LOW);        // Set outputs to LOW
  digitalWrite(back, LOW);
  digitalWrite(left, LOW);
  digitalWrite(right, LOW);

  Serial.print("Connecting to ");      // Connect to Wi-Fi network with SSID and password
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {                             // If a new client connects,
    currentTime = millis();
    previousTime = currentTime;

    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client

    while (client.connected() && currentTime - previousTime <= timeoutTime) {  // loop while the client's connected
      currentTime = millis();
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then

        Serial.write(c);                    // print it out the serial monitor

        
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            //client.println();
            // turns the GPIOs on and off
            period = (header.substring(header.indexOf("time/")+5, header.indexOf("/end")));
            action = (header.substring(header.indexOf("action/")+7, header.indexOf("/time")));


            if (action == "front") {
              Serial.println("GPIO 13 ; front for " + period + " seconds");
              client.println("action: front " + period + "s");
              client.println();
              digitalWrite(front, HIGH);
              delay(period.toInt());
              digitalWrite(front, LOW);
            } else if (action == "back") {
              Serial.println("GPIO 32 ; back for " + period + " seconds");
              client.println("action: back " + period + "s");
              client.println();
              digitalWrite(back, HIGH);
              delay(period.toInt());
              digitalWrite(back, LOW);              
            } else if (action == "front-left") {
              Serial.println("GPIO 13 & 15 ; front & left for " + period + " seconds");
              client.println("action: front-left " + period + "s");
              client.println();
              digitalWrite(front, HIGH);
              digitalWrite(left, HIGH);
              delay(period.toInt());
              digitalWrite(front, LOW);
              digitalWrite(left, LOW);              
            } else if (action == "front-right") {
              Serial.println("GPIO 13 & 19 ; front & right for " + period + " seconds");
              client.println("action: front-right " + period + "s");
              client.println();
              digitalWrite(front, HIGH);
              digitalWrite(right, HIGH);
              delay(period.toInt());
              digitalWrite(front, LOW);
              digitalWrite(right, LOW); 
            } else if (action == "back-left") {
              Serial.println("GPIO 32 & 15 ; back & left for " + period + " seconds");
              client.println("action: back-left " + period + "s");
              client.println();
              digitalWrite(back, HIGH);
              digitalWrite(left, HIGH);
              delay(period.toInt());
              digitalWrite(back, LOW);
              digitalWrite(left, LOW); 
            } else if (action == "back-right") {
              Serial.println("GPIO 32 & 19 ; back & right for " + period + " seconds");
              client.println("action: back-right " + period + "s");
              client.println();
              digitalWrite(back, HIGH);
              digitalWrite(right, HIGH);
              delay(period.toInt());
              digitalWrite(back, LOW);
              digitalWrite(right, LOW); 
            }
            else{
              Serial.println("No Action");
              client.println("action: none");              
              client.println();
            }

            client.println("<head><link rel=\"icon\" href=\"data:,\"></head>");

            //client.println("<h1>Sojith the great</h1>");
            client.println(); //signifies the end of html content, if any
            
            break;            // Break out of the while loop
          } else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

      }
    }

    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}

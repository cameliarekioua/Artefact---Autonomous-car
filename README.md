**README**

---

# **Autonomous Car with Aruco Marker Detection**  

## **Project Overview**  
This project involves the development of an **autonomous vehicle** capable of detecting **Aruco markers** and navigating a predefined grid. The system is built using a **Raspberry Pi** as the main processing unit and utilizes **computer vision** for marker detection. The car is controlled via a web interface or a direct terminal command.  

## **Hardware Used**  
- **Raspberry Pi (SBC)**
- **Battery and Power Supply**
- **Webcam** (for vision and marker detection)
- **Two DC motors** with rotation sensors  
- **Motor controller** (connected via the I2C bus on the Raspberry Pi)  
- **WiFi Router** (for remote access and web interface)  
- **FabLab resources**: laser-cut wooden parts for chassis  

## **Software & Technologies Used**  
- **Raspberry Pi OS** (Operating system setup)  
- **SSH Configuration** (for remote access and control)  
- **Motor Control & Calibration**  
- **Camera Calibration** (for accurate marker detection)  
- **OpenCV** (for computer vision and Aruco marker detection)  
- **Python Flask** (to host the web server)  
- **HTML, CSS, JavaScript** (for the web interface)  
- **I2C Communication** (for motor control)  

## **Setup & Installation**  
1. **Install Raspberry Pi OS** and set up SSH access.  
2. **Calibrate the motors** and configure the motor controller.  
3. **Set up the camera** and calibrate it for Aruco marker detection.  
4. **Run the web server** to control the vehicle remotely.  
5. **Prepare laser-cut parts** by generating and sending an **SVG file** to the laser cutter.  

## **How to Run the Program**  
You can launch the program in two ways:  
- **From the web interface**  
- **From the terminal**:  
  ```bash
  python3 serveur.py
  ```


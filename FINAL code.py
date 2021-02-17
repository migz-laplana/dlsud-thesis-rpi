import serial
import time
import requests
import json


logindeets = {
    'txtUsername': 'A0001',
    'txtPassword': 'password'
    }
                

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
      
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if "byebye" in line:   #when a passenger has left
                print()
                print("Sending transaction details to TripleMPay...")
                info = line[6:]
                print(info)
                lt1, lng1, lt2, lng2, rfid, driverid = info.split("#")
                
                #14.321683    #DLSUD G1
                #120.963655
                secondtap = {}
                driverid = driverid
                rfid = rfid
                lat1 = lt1
                long1 = lng1
                lat2 = lt2
                long2 = lng2
                

                for variable in ["driverid", "rfid", "lat1", "long1", "lat2", "long2"]:
                    secondtap[variable] = eval(variable)
                print(secondtap)
                #print(secondtap)
                with requests.Session() as s:
                    p = s.post('https://triplempay.herokuapp.com/db_login.php', data=logindeets)
                    if p.status_code == 200:   #checking for successful conn
                        print("   Admin login successful!")
                    else:
                        print("   Error, check connection")

                    f = s.post('https://triplempay.herokuapp.com/fromRPI.php', data=secondtap)
                    if f.status_code == 200:   #checking for successful conn
                        print("   Data has been sent and recorded.")
                    else:
                        print("   Error, check connection")
            
            if "boarded" in line:    #when a passenger has just boarded
                print("Now connecting to TripleMPay for balance checking...")
                card = line[:11]
                #print(card)

                firsttap = {}
                rfid = card                     

                for variable in ["rfid"]:
                    firsttap[variable] = eval(variable)
                #print(firsttap)
                
                
                with requests.Session() as s:
                    p = s.post('https://triplempay.herokuapp.com/db_login.php', data=logindeets)
                    if p.status_code == 200:
                        print("   Admin login successful!")
                    else:
                        print("   Error, check connection")
                    r = s.get('https://triplempay.herokuapp.com/fromRPI.php', params=firsttap)
                    if r.status_code == 200:   #checking for successful conn
                        print("   Verifying card balance...")
                    else:
                        print("   Error, check connection")
                    answer = json.loads(r.content)
                    if "No" in answer:
                        ser.write(b"Card does not have sufficient balance! PLEASE GET OFF\n")
                        #reply = ser.readline().decode('utf-8').rstrip()
                        #print(reply)
                    if "Yes" in answer:
                        ser.write(b"Card has sufficient balance, allowed to board.\n")
                        #reply = ser.readline().decode('utf-8').rstrip()
                        #print(reply)
                    if "invalid" in answer:
                        ser.write(b"Card is unregistered. GET OFF.\n")
                        #reply = ser.readline().decode('utf-8').rstrip()
                        #print(reply)
                print()
                    

            if "dvr" in line:    #when a driver attempts to sign in
                print("Now connecting to TripleMPay for driverid checking...")
                driver = line[3:]
                #print(card)

                drivertap = {}
                rfid = driver                     

                for variable in ["rfid"]:
                    drivertap[variable] = eval(variable)
                print(drivertap)
                
                
                with requests.Session() as s:
                    p = s.post('https://triplempay.herokuapp.com/db_login.php', data=logindeets)
                    if p.status_code == 200:
                        print("   Admin login successful!")
                    else:
                        print("   Error, check connection")
                    r = s.get('https://triplempay.herokuapp.com/driverCheck.php', params=drivertap)
                    if r.status_code == 200:   #checking for successful conn
                        print("   Looking up driverid in database...")
                    else:
                        print("   Error, check connection")
                    answer = json.loads(r.content)
                    print(answer)
                    if "invalid" in answer:
                        ser.write(b"DriverId INVALID\n")
                        #reply = ser.readline().decode('utf-8').rstrip()
                        #print(reply)
                    if "Yes" in answer:
                        ser.write(b"DriverId Accepted\n")
                        #reply = ser.readline().decode('utf-8').rstrip()
                        #print(reply)

                print()
                
                
                
   
                


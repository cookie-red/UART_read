import serial
import socket
import time

def catchClearData(data):
    #print('catch clear data')
    if (data.find('$') != -1): 
        data = data[data.find('$'):] # 移除\r\n
        # print('ClearData',data)
	#print('length',len(data))
        # createJsonFile(data)
        return data
    elif (data.find('&') != -1): 
        data = data[data.find('&'):]
        # createJsonFile(data)
        return False
    else:
        return False

def decode_data(clear_data):
    clear_data = clear_data[:38] + clear_data[42:72]
    packet = clear_data
    return packet

def hex2Dec(packet):
    hex = str(packet)
    string = ''
    i = 0
    while i < len(hex):
        string = string + str(int(hex[i:i+2],16))
        i += 2
    return string

# 血壓、步數、里程、卡路里需要用以hex2Dec_2來解碼(須對調:7104 -> 0471)
def hex2Dec_2(packet):
    string = packet[2:4] + packet[0:2]
    dec = int(string,16)
    return dec

def decode(data):
    mileage = str(int(hex2Dec_2(data[0:4]))/1000) # 里程 (若收到的值須對掉 ex:7104 -> 0471)
    calories = str(int(hex2Dec_2(data[4:8]))) # 卡路里 (若收到的值須對掉 ex:7104 -> 0471)
    # power = hex2Dec(data[8:10]) # 電力
    hr = str(int(hex2Dec(data[10:12]))) # 心率
    temp = hex2Dec(data[12:16])
    TEMP = str(float(temp[0:2]+'.'+temp[2:4])) # 體溫

    physical = {'Mileage':mileage,  
                'Calories':calories,
                # 'Power':power,
                'HR':hr,
                'Temp':TEMP
                }
    print(physical)


if __name__ == '__main__':

    i = 0
    ser = serial.Serial("COM5", 115200)
    print (ser.port)
    while True:
        sline = ser.readline().decode()
        if sline[3:15] == '4003EE7F99DB': #先篩選測試手錶資料
            clear_data = catchClearData(sline)
            packet = decode_data(clear_data)
            data = packet[38:54] 
            decode(data)
            nowTime = time.strftime('%H:%M:%S',time.localtime())
            print(nowTime) # 查看接收數據的時間延遲
           

            

      
# mode macaddress  time longitude  latitude        thing          hopping     
#  3       12        4     10          9             16             14
# $05 79A4CFC90EC2 E800 121.5300FF 25.0400B3 B3000B005B000000 91599125620703
#                                            38~

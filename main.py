import numpy as np  # 匯入 NumPy 模組，用於科學計算
import time  # 匯入 time 模組，用於計時
import cv2  # 匯入 OpenCV 模組，用於影像處理
import PoseModule as pm  # 自定義模組，用於姿勢偵測
import math  # 匯入 math 模組，用於數學運算
from PIL import ImageGrab, Image
import os
import pyodbc
import base64
import threading
import datetime

# 更改對象處

# 初始化攝影機，這裡是使用預設的攝影機
cap = cv2.VideoCapture(0)

# 初始化姿勢偵測器
detector = pm.poseDetector()

# 初始化計數器、方向、上一個時間
count = 0
dir = 0
pTime = 0

# 初始化成功狀態、i、bs、ratio、height_all、baseH
success = True
i = 0
bs = 0
ratio = 0
height_all = 0
baseH = 0
# 確定跌倒次數提醒次數
Falldown_1 = 0
img_count = 0
id=0
file_count=0
ending = 0
#日期戳記
lastday = 0
def cleanData():
    # 更改對象處
    folder_path = 'C:/Users/ASUS/Desktop/Topic_code/image/'
    # folder_path = 'D:/Topic_code/img/'  # 黃的設置文件夾路徑
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

    # 更改對象處
    # conn = pyodbc.connect(driver="SQL Server Native Client 11.0",
    #                       host="DESKTOP-ERIHSRT\SQLEXPRESS02", database="fall_img",
    #                       uid="sa", pwd="top159357")  # 資料庫連線
    # conn = pyodbc.connect(driver="SQL Server Native Client 11.0",
    #                host="DESKTOP-7C2H478", database="Basic_Information",
    #                uid="sa", pwd="jkl0979229277")  # 黃的資料庫連線
    conn = pyodbc.connect(driver="SQL Server Native Client 11.0", server="123.195.132.32,1433",
                          database="Basic_Information",
                          uid="sa", pwd="jkl0979229277")
    cursor = conn.cursor()
    # sql = "TRUNCATE TABLE test9;"
    sql = "TRUNCATE TABLE jkl_7777;"

    cursor.execute(sql)
    conn.commit()  # 更新資料庫
    conn.close()
    print("清除資料庫")

def repeat_timer(): #每五秒就+1 可以當成時間間距
    global img_count,file_count
    # 更改對象處
    folder_path = 'C:/Users/ASUS/Desktop/Topic_code/image/' #徐的設置文件夾路徑
    # folder_path = 'D:/Topic_code/img/'  # 黃的設置文件夾路徑
    # 更改對象處
    # conn = pyodbc.connect(driver="SQL Server Native Client 11.0",
    #                       host="DESKTOP-ERIHSRT\SQLEXPRESS02", database="fall_img",
    #                       uid="sa", pwd="top159357") # 徐的的資料庫連線
    # conn = pyodbc.connect(driver="SQL Server Native Client 11.0",
    #                host="DESKTOP-7C2H478", database="Basic_Information",
    #                uid="sa", pwd="jkl0979229277")  # 黃的資料庫連線
    conn = pyodbc.connect(driver="SQL Server Native Client 11.0", server="123.195.132.32,1433",
                          database="Basic_Information",
                          uid="sa", pwd="jkl0979229277")

    cursor = conn.cursor()
    file_list = os.listdir(folder_path)  # 取得目標資料夾下的所有檔案
    # 更改對象處
    # sql = "SELECT COUNT(*) FROM test9"   #這裡需要改table名稱
    sql = "SELECT COUNT(*) FROM jkl_7777"  #黃的sql資料數量
    cursor.execute(sql)
    num_records = cursor.fetchone()[0]  #取得sql資料數量
    if len(file_list) != num_records: #資料夾檔案數與sql資料數去做比較
        img_count += 1
        with open(folder_path + file_list[file_count], 'rb') as f:
            img_data = f.read()
        encodestring = base64.b64encode(img_data)  # jpg檔轉至base64
        cursor = conn.cursor()
        # 更改對象處
        # sql_save = "INSERT INTO test9(timer, img) values (?,?)" #徐的插入sql
        sql_save = "INSERT INTO jkl_7777 (timer, img) values (?,?)"   #黃的sql
        cursor.execute(sql_save, (file_list[file_count] , encodestring))
        file_count+=1

        conn.commit()  # 更新資料庫
        conn.close()
    if success :
        threading.Timer(5.0, repeat_timer).start()
    else:
        threading.Timer(5.0, repeat_timer).cancel()

cleanData()
repeat_timer()

while success:
    pointlist = []
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (640, 480))  # 調整圖像大小
        imgCanvas = np.zeros((480, 640, 3), np.uint8)  # 創建黑色畫布
        imgCanvas = detector.findPose(img, imgCanvas)  # 在圖像上檢測姿勢
        lmList, bbox = detector.findPosition(img,True)  # 檢測身體部位位置
        if len(lmList) != 0:
            i = i + 1
            # 两肩中点
            if bs == 0:
                if i == 1:
                    point_one = detector.midpoint(11, 12)
                elif i == 10:
                    # 計算肩膀中心點、腳尖中心點、脊椎垂直距離、身高總距離、身高比率
                    point_ten = detector.midpoint(11, 12)
                    point_foot = detector.midpoint(29, 30)
                    spineV = int(math.hypot(point_ten['x'] - point_one['x'], point_ten['y'] - point_one['y']))
                    height_all = int(math.hypot(point_foot['x'] - point_one['x'], point_foot['y'] - point_one['y']))
                    ratio = spineV / height_all
                    if ratio > 0.25:
                        bs = 1
                    else:
                        i = 0

                    # print(length)
            # if bs==1:
            if True:
                # 两髋中心点
                point_kuan = detector.midpoint(23, 24)
                point_foot = detector.midpoint(29, 30)
                # 两脚中点

                baseH = (point_kuan['y'] - point_foot['y'])
                if baseH > -40 and i < 30:
                    bs = 2
                elif baseH < -40:
                    bs = 0
                    i = 0

            if bs == 2:  # &&計時有剛好在秒數上
                Falldown_1 += 1
                lmList, bbox = detector.findPosition(img,False)
                repeat_timer()
                #更改對象處
                # folder_path = 'D:/Topic_code/img/'  # 黃的設置文件夾路徑
                folder_path = 'C:/Users/ASUS/Desktop/Topic_code/image/'  # 設置文件夾路徑

                if Falldown_1%5 ==0:#可以直接避免大量的照片存入 可以有時間差距
                    try:
                        imageName = str(time.strftime('%Y.%m.%d %H-%M-%S', time.localtime(time.time()))) + ".jpg"
                        screenshot = cv2.imwrite(folder_path+imageName, img)
                    except OSError:
                        print(folder_path+imageName + ' is not a valid image file.')

        else:
            bs = 0
            i = 0
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

        cv2.imshow("Fall_Src", img)

        if cv2.waitKey(113) == ord("q"):
            cleanData() #取消後刪除sql資料
            success = 0

            break

cap.release()
cv2.destroyAllWindows()
# 关闭连接


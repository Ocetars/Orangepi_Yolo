import cv2
import time
from rknnpool import rknnPoolExecutor
from func import myFunc

cap = cv2.VideoCapture("./VID_20230712_172958.mp4")
# cap = cv2.VideoCapture("./REC_for_testing.mp4")
# cap = cv2.VideoCapture(0)

# 模型路径
modelPath = "./rknnModel/2022S_RK3588_i8.rknn"
# CLASSES = ("TakeOff", "Car", "Concentric", "W", "Centre")
CLASSES = ('RT', 'RR', 'RC', 'BT', 'BR', 'BC', 'A', 'X')
# 线程数
TPEs = 3
# 初始化rknn池
pool = rknnPoolExecutor(rknnModel=modelPath, TPEs=TPEs, myFunc=myFunc)

# 初始化异步所需要的帧
if cap.isOpened():
    for i in range(TPEs + 1):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            del pool
            exit(-1)
        pool.put(frame)

frames, loopTime, initTime = 0, time.time(), time.time()
while cap.isOpened():
    frames += 1
    ret, frame = cap.read()
    if not ret:
        break
    pool.put(frame)
    # 下一行中，result是myFunc函数的返回值（列表），flag是pool.get的判断标志(True or False）
    result, flag = pool.get()
    if flag == False:
        break
    # 输出结果，result是列表，内容详见myFunc函数
    if result is not None:
        outpic = result[0]
        centers = result[1]
        boxes = result[2]
        scores = result[3]
        classes = result[4]
        
        cv2.imshow("outpic", outpic)
        if classes is not None:
            for cl in classes:
                # if CLASSES[cl] == "W" and scores[cl] > 0.5:
                    if centers:
                        # centers是一个列表，里面第[0]个元素是一个元组，元组中是中心点的坐标
                        center_x = centers[0][0]
                        center_y = centers[0][1]
                        print("center:\t",center_x,center_y)
                        print("class:\t", CLASSES[cl])
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    # if frames % 30 == 0:
    #     print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")
    #     loopTime = time.time()

print("总平均帧率\t", frames / (time.time() - initTime))

cap.release()
cv2.destroyAllWindows()
pool.release()

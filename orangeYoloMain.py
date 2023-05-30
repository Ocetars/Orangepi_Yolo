import cv2
import time
from rknnpool import rknnPoolExecutor
from func import myFunc

cap = cv2.VideoCapture("./REC_for_testing.mp4")
# cap = cv2.VideoCapture(0)

# 模型路径
modelPath = "./rknnModel/GXv5s_RK3588_i8.rknn"
# 线程数
TPEs = 3
# 初始化rknn池
pool = rknnPoolExecutor(rknnModel=modelPath, TPEs=TPEs, func=myFunc)

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
    # 下一行中，result是myFunc函数的返回值（列表），flag是(True or False）
    result, flag = pool.get()
    if flag == False:
        break
    # 输出结果
    cv2.imshow("test", result[0])
    print("centers:\t", result[1])
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if frames % 30 == 0:
        print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")
        loopTime = time.time()

print("总平均帧率\t", frames / (time.time() - initTime))

cap.release()
cv2.destroyAllWindows()
pool.release()

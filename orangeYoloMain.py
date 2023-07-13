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

def draw(image, boxes, scores, classes, label="A", threshold=0.6):
    centers = []
    for box, score, cl in zip(boxes, scores, classes):
        # 加入筛选条件，确定需要检测的目标
        if CLASSES[cl] == label and score > threshold:
            top, left, right, bottom = box
            # print('class: {}, score: {}'.format(CLASSES[cl], score))
            # print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(top, left, right, bottom))
            top = int(top)  # 左上x1
            left = int(left)  # 左上y1
            right = int(right)  # 右下x2
            bottom = int(bottom)  # 右下y2
            x1 = top
            y1 = left
            x2 = right
            y2 = bottom
            # 在图像上绘制目标框
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # 计算目标框的中心坐标
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            centers.append((center_x, center_y))

            # 在图像上绘制目标中心
            cv2.circle(image, (int(center_x), int(center_y)), 2, (0, 255, 0), -1)
            # 在图像上绘制物体类别及置信度
            cv2.putText(
                image,
                "{0} {1:.2f}".format(CLASSES[cl], score),
                (x1, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )
    return centers, score

frames, loopTime, initTime = 0, time.time(), time.time()

# 主函数
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
        boxes = result[1]
        scores = result[2]
        classes = result[3]
    
        if classes is not None:
            # 从draw函数中引入返回值
            centers, score = draw(outpic, boxes, scores, classes)

            print(  "class:\t", 'A',
                    "\tcenters:\t", centers, 
                    "\tscore:\t", score  )
            
            cv2.imshow("outpic", outpic)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    # if frames % 30 == 0:
    #     print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")
    #     loopTime = time.time()

print("总平均帧率\t", frames / (time.time() - initTime))

cap.release()
cv2.destroyAllWindows()
pool.release()

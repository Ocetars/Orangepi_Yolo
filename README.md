# 多线程模型帧率测试
* 使用performance.sh进行CPU/NPU定频尽量减少误差
* airockchip提供的已量化模型[下载](https://eyun.baidu.com/enterprise/share/link?cid=8272257679089781337&uk=2751701137&sid=202211118572878233)（密码rknn）
* 无人机场地测试视频：REC_for_testing.mp4

|  模型\线程数   | 1    |  2   | 3  |  4  | 5  | 6  |
|  ----  | ----    | ----  |  ----  | ----  | ----  | ----  |
| yolov5s  | 27.4491 | 49.0747 | 65.3673  | 63.3204 | 71.8407 | 72.0590 |

# Acknowledgements
* https://github.com/ultralytics/yolov5
* https://github.com/rockchip-linux/rknn-toolkit2
* https://github.com/airockchip/rknn_model_zoo

# Contributors
本仓库主要内容基于 [leafqycc](https://github.com/leafqycc)

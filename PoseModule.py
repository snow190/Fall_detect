import mediapipe as mp
import cv2

class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.85, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpDraw_styles = mp.solutions.drawing_styles
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, False, self.detectionCon, self.trackCon)

    # findPose 方法用於在圖像中檢測人體姿勢。
    def findPose(self, img, imgCanvas,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(imgCanvas, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
                                            #landmark_drawing_spec=self.mpDraw_styles.get_default_pose_landmarks_style())
        return imgCanvas

    # findPosition 方法用於查找姿勢關鍵點的位置。
    def findPosition(self, img, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                xList.append(cx)
                yList.append(cy)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 0, 255), 2)
        return self.lmList, bbox

    # midpoint 方法用於查找兩個關鍵點之間的中點。
    def midpoint(self, p1, p2):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3 = int((x1 + x2) / 2)
        y3 = int((y1 + y2) / 2)
        point = {"x": x3, "y": y3}
        return point

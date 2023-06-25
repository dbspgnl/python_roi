import cv2
import numpy as np
import keyboard

isDragging = False                         # 마우스 드래그 상태 저장
x0,y0,w,h = -1,-1,-1,-1                    # 영역 선택 좌표 저장
blue,red = (255,0,0),(0,0,255)              # 색상 값
positions = []


def onMouse(event, x, y, flags, param):     # 마우스 이벤트 핸들 함수
    global isDragging, x0, y0, img          # 전역 변수 참조

    if event == cv2.EVENT_LBUTTONDOWN:      # 왼쪽 마우스 버튼 다운, 드래그 시작
        isDragging = True
        x0 = x
        y0 = y
        if flags & cv2.EVENT_FLAG_SHIFTKEY: # 마우스 좌클릭 후 시프트
            print("시프트 누른 후 좌버튼")
            positions.append((x,y))
            
    elif event == cv2.EVENT_LBUTTONUP: # 왼쪽 마우스 버튼 업 (행동 종료) 
        isDragging = False
        print(positions)
        if len(positions) == 2: # 좌표가 두 개면 직선
            print("직선")
            img_draw = img.copy() 
            cv2.line(img_draw, positions[0], positions[1], red, 2)
            cv2.imshow('img', img_draw)
        elif len(positions) >= 3: # 다각형 
            print("삼각형")
            img_draw = img.copy() 
            pts3 = np.array(positions, dtype=np.int32)
            cv2.polylines(img_draw, [pts3], True, (0,0,255), 2)
            cv2.imshow('img', img_draw)
     
        
    elif event == cv2.EVENT_MOUSEMOVE:      # 마우스 움직임
        if isDragging:                       # 드래그 진행 중
            img_draw = img.copy()            # 사각형 그림 표현을 위한 이미지 복제 (매번 같은 이미지에 그려지면 이미지가 더러워짐)
            cv2.rectangle(img_draw, (x0,y0), (x,y), blue, 2)  # 드래그 진행 영역 표시
            cv2.imshow('img', img_draw)       # 사각형으로 표시된 그림 화면 출력
            

img = cv2.imread('./intersection.png') # 이미지 로드
while True: 
    cv2.imshow('img', img)
    cv2.setMouseCallback('img', onMouse) # 마우스 이벤트 등록
    key = cv2.waitKey()
    if  key == ord('q') :
        cv2.destroyAllWindows()
        break
    elif key == ord('1') :
        print("1 클릭")
        
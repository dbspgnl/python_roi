import cv2
import numpy as np

isDragging = False                         # 마우스 드래그 상태 저장
x0,y0,w,h = -1,-1,-1,-1                    # 영역 선택 좌표 저장
blue,red = (255,0,0),(0,0,255)              # 색상 값

def onMouse(event, x, y, flags, param):     # 마우스 이벤트 핸들 함수
    global isDragging, x0, y0, img          # 전역 변수 참조
    if event == cv2.EVENT_LBUTTONDOWN:      # 왼쪽 마우스 버튼 다운, 드래그 시작
        isDragging = True
        x0 = x
        y0 = y
        
    elif event == cv2.EVENT_MOUSEMOVE:      # 마우스 움직임
        if isDragging:                       # 드래그 진행 중
            img_draw = img.copy()            # 사각형 그림 표현을 위한 이미지 복제 (매번 같은 이미지에 그려지면 이미지가 더러워짐)
            cv2.rectangle(img_draw, (x0,y0), (x,y), blue, 2)  # 드래그 진행 영역 표시
            cv2.imshow('img', img_draw)       # 사각형으로 표시된 그림 화면 출력
            
    elif event == cv2.EVENT_LBUTTONUP:       # 왼쪽 마우스 버튼 업
        if isDragging:                        # 드래그 중지
            isDragging = False               
            w= x - x0                         # 드래그 영역 폭 계산
            h= y - y0                         # 드래그 영역 높이 계산
            print("x%d, y%d, w%d, h%d" % (x0, y0, w, h) )
            if w>0 and h>0:                  # 폭과 높이가 양수이면 드래그 방향이 옳음
                img_draw = img.copy()         # 선택 영역에 사각형 그림을 표시할 이미지 복제
                cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2) # 선택 영역에 빨간색 사각형 표시
                cv2.imshow('img', img_draw)         # 빨간색 사각형이 그려진 이미지 화면 출력
                roi = img[y0:y0+h, x0:x0+w]         # 원본 이미지에서 선택 영역만 ROI로 지정
                cv2.imshow('cropped', roi)          # ROI 지정 영역을 새 창으로 표시
                cv2.moveWindow('cropped', 0,0)     # 새 창을 화면 좌측 상단으로 이동
                cv2.imwrite('../CV2/img/cropped.jpg', roi)  # ROI 영역만 파일로 저장
                print('cropped.')
            
            else:
            # 드래그 방향이 잘못된 경우 사각형 그림이 없는 원본 이미지 출력
                cv2.imshow('img', img)
                print('좌측 상단에서 우측 하단으로 영역을 드래그하세요.')

img = cv2.imread('./intersection.png')
cv2.imshow('img', img)
cv2.setMouseCallback('img', onMouse) # 마우스 이벤트 등록
cv2.waitKey()
cv2.destroyAllWindows()
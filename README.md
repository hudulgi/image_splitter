# Image Splitter (이미지 분리기)

하나의 파일에 두 개의 이미지가 좌, 우측에 들어가 있다면 분리하는 코드이다. 하나의 이미지로 스캔된 하프사이즈 사진 두 장을 분리하는 목적으로 만들어졌다.

![Image](https://github.com/user-attachments/assets/05d8aa58-ef1b-4603-b7c3-8789db5bb833)

가로2, 세로3의 비율을 사용하기 때문에 원본 이미지의 세로 크기를 이용하여 좌우 이미지의 가로 폭을 계산하여 사용한다. 

원본 이미지의 좌, 우측 경계면을 기준으로 특정 픽셀 간격으로 offset 되어 이미지가 추출되고, offset량은 코드 상에서 지정 한다. (변수명 tol)
3035X2031 크기인 샘플 이미지는 40을 사용했다.

output_overlay 폴더에 좌우 이미지 영역을 오버레이한 이미지가 출력되므로 분리되는 영역의 확인이 가능하다.

![Image](https://github.com/user-attachments/assets/08842947-c96e-4532-b70a-535f99b17476)

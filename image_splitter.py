import cv2
import os
from pathlib import Path


def image_seperator(_image_path):
    # 원본 이미지를 불러오고, 원본은 별도로 보존
    original_img = cv2.imread(_image_path)
    if original_img is None:
        print("이미지를 불러올 수 없습니다.")
        exit(1)
    img = original_img.copy()  # 작업용 이미지

    # 전체 이미지 크기
    height, width = img.shape[:2]

    # 좌우 영역 설정
    # 이미지의 수직 크기를 1.5로 나눈 값이 분리 영역의 폭 (가로2:세로3 비율)
    crop_width = height / 1.5
    crop_width_half = crop_width / 2.0

    left_center = tol + crop_width_half  # 좌측 사진 중앙
    right_center = width - ( tol + crop_width_half)  # 우측 사진 중앙

    # 정수형 좌표 계산
    left_center_int = int(round(left_center))
    right_center_int = int(round(right_center))
    center_int = int(round(width / 2.0))
    crop_width_int = int(round(crop_width))

    # 기준 선 그리기
    # 빨간 선: 좌측 및 우측 이미지의 중앙
    cv2.line(img, (left_center_int, 0), (left_center_int, height - 1), (0, 0, 255), 2)
    cv2.line(img, (right_center_int, 0), (right_center_int, height - 1), (0, 0, 255), 2)
    # 파란 선: 전체 중앙선 (검은 구분선의 평균 중앙점)
    cv2.line(img, (center_int, 0), (center_int, height - 1), (255, 0, 0), 2)

    # 좌측 영역: 중심은 left_center
    left_crop_x_start = tol
    left_crop_x_end = tol + crop_width_int

    # 우측 영역: 중심은 right_center
    right_crop_x_start = width - ( tol + crop_width_int)
    right_crop_x_end = width - tol

    # 노란색 반투명 사각형으로 영역 표시 (전체 높이 사용)
    overlay = img.copy()
    yellow = (0, 255, 255)  # BGR: 노란색
    alpha = 0.2  # 투명도 계수

    cv2.rectangle(overlay, (left_crop_x_start, 0), (left_crop_x_end, height), yellow, -1)
    cv2.rectangle(overlay, (right_crop_x_start, 0), (right_crop_x_end, height), yellow, -1)

    # overlay와 원본 이미지 합성
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # 결과(오버레이 포함) 이미지 저장
    _name, _ext = os.path.splitext(os.path.basename(_image_path))
    os.makedirs(overlay_output_path, exist_ok=True)  # 폴더가 없으면 생성 (이미 존재하면 오류 발생하지 않음)

    cv2.imwrite(os.path.join(overlay_output_path, f'{_name}_overlay.{_ext}'), img)
    print(f"overlay 이미지가 {overlay_output_path}에 저장되었습니다.")

    # 좌측과 우측 영역을 원본 이미지에서 잘라서 별도의 파일로 저장
    left_region = original_img[0:height, left_crop_x_start:left_crop_x_end]
    right_region = original_img[0:height, right_crop_x_start:right_crop_x_end]
    os.makedirs(split_output_path, exist_ok=True)  # 폴더가 없으면 생성 (이미 존재하면 오류 발생하지 않음)

    cv2.imwrite(os.path.join(split_output_path, f'{_name}_l.{_ext}'), left_region, [cv2.IMWRITE_JPEG_QUALITY, 100])
    print(f"좌측 영역 이미지가 {split_output_path}에 저장되었습니다.")
    cv2.imwrite(os.path.join(split_output_path, f'{_name}_r.{_ext}'), right_region, [cv2.IMWRITE_JPEG_QUALITY, 100])
    print(f"우측 영역 이미지가 {split_output_path}에 저장되었습니다.")


if __name__ == '__main__':
    image_path = './input'  # 원본 이미지 파일 경로
    overlay_output_path = './output_overlay'  # 결과(오버레이 포함) 이미지 저장 경로
    split_output_path = './output'

    # 좌/우측 offset량 설정 (px)
    tol = 40

    folder = Path(image_path)  # 검색할 폴더 경로
    # 폴더 내의 파일들 중 확장자가 .jpg (대소문자 상관없이) 인 파일 선택
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == '.jpg']
    files = sorted(files)

    print(files)
    for file in files:
        print(file)
        image_seperator(file)

import cv2
from ultralytics import YOLO
import os
import sys

try:
    model_path = "best.pt"
    model = YOLO(model_path, task='detect')
    print(f"Đã tải mô hình thành công từ: {model_path}")
except Exception as e:
    print(f"LỖI TẢI MÔ HÌNH: Không tìm thấy tệp {model_path}. Vui lòng kiểm tra lại vị trí của best.pt.")
    print(f"Chi tiết lỗi: {e}")
    sys.exit(1)

img_path = 'bienbao1.jpg'

if not os.path.exists(img_path):
    print(f"LỖI ĐẦU VÀO: Không tìm thấy tệp ảnh {img_path}.")
    print("Vui lòng đảm bảo tệp ảnh nằm đúng vị trí hoặc sửa lại đường dẫn trong code.")
    sys.exit(1)
    
img = cv2.imread(img_path)

if img is None:
    print(f"LỖI ĐỌC ẢNH: Tệp '{img_path}' tồn tại nhưng không thể đọc được (có thể bị hỏng).")
    sys.exit(1)

results = model(img, conf=0.25)

result = results[0] 

for box in result.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    conf = box.conf.item()
    class_id = int(box.cls.item())
    label = model.names[class_id]
    
    print(f"Phát hiện: {label} (Conf: {conf:.2f}) tại [{x1}, {y1}, {x2}, {y2}]")
    
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

try:
    cv2.imshow("Ket Qua Nhận Dien Bien Bao", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    cv2.imwrite("output.jpg", img)
    print("Đã lưu ảnh kết quả thành: output.jpg")

except Exception as e:
    print(f"LỖI HIỂN THỊ: Không thể hiển thị ảnh. Lỗi: {e}")
    print("Bạn có thể thiếu thư viện giao diện đồ họa (GUI) cho OpenCV hoặc đang chạy trong môi trường không có màn hình.")
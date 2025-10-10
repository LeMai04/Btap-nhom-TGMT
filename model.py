import random

# Danh sách giả lập các biển báo
classes = ["Cấm rẽ trái", "Cấm rẽ phải", "Cấm đi thẳng", "Giới hạn tốc độ", "Dừng"]

def predict_sign(image_path):
    """
    Hàm test: nhận vào đường dẫn ảnh, trả về biển báo giả ngẫu nhiên
    """
    class_name = random.choice(classes)
    confidence = random.uniform(80, 100)  # giả lập confidence 80-100%
    return f"{class_name} ({confidence:.2f}%)"

import os
from PIL import Image

def trim_transparent_images(input_folder, output_folder):
    # Tạo thư mục đầu ra nếu chưa có
    os.makedirs(output_folder, exist_ok=True)

    # Duyệt tất cả file trong thư mục input
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Mở và chuyển sang định dạng RGBA để đảm bảo có kênh alpha
                img = Image.open(input_path).convert("RGBA")

                # Lấy vùng không trong suốt
                bbox = img.getbbox()

                if bbox:
                    # Cắt ảnh
                    trimmed = img.crop(bbox)
                    trimmed.save(output_path)
                    print(f"Đã xử lý: {filename}")
                else:
                    print(f"Bỏ qua (ảnh hoàn toàn trong suốt): {filename}")
            except Exception as e:
                print(f"Lỗi xử lý {filename}: {e}")

trim_transparent_images("assets\\jinn", "assets\\jinn_trim")

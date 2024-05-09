import os

# Giả sử cấu hình BASE_DIR của bạn được đặt như sau, thay đổi nếu khác
BASE_DIR = '/Users/hoangdieu/PycharmProjects/EcomRecomendation'

# Đường dẫn đến thư mục chứa model
MODEL_DIR = os.path.join(BASE_DIR, 'static', 'model')

# Đường dẫn đến file model cụ thể
model_path = os.path.join(MODEL_DIR, 'kmeans_model.joblib')

# In đường dẫn để kiểm tra
all_items = os.listdir(MODEL_DIR)
files = [item for item in all_items if os.path.isfile(os.path.join(MODEL_DIR, item))]

    # Kiểm tra nếu không có file nào
if not files:
	print("not Found")
else:
        # In ra tên các file
	for file in files:
		print(file)


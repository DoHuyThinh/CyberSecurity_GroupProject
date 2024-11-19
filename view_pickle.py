import pickle

# Thay đổi đường dẫn đến file .pkl của bạn
file_path = 'new_intrusion_model.pkl'

# Mở và đọc file pickle
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# In dữ liệu để kiểm tra
print(data)

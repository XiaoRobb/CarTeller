from scipy import io as mat_io

car_mat_file = "../data_processing/datasets/cars_metas/cars_meta"
labels_meta = mat_io.loadmat(car_mat_file)
class_names = [name[0] for name in labels_meta['class_names'][0]]
# print("**************************************************")
#
# car_mat_file2 = "../data_processing/datasets/cars_metas/cars_train_annos"
# labels_meta2 = mat_io.loadmat(car_mat_file2)
# print(labels_meta2["annotations"][0])
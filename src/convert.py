# https://www.kaggle.com/datasets/thtuan/btad-beantech-anomaly-detection

import glob
import os

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dotenv import load_dotenv
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
from tqdm import tqdm

import src.settings as s


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    # project_name = "BTAD"
    dataset_path = "/home/grokhi/rawdata/btad/BTech_Dataset_transformed"
    batch_size = 30
    batch_size = 30
    masks_folder_name = "ground_truth"


    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        subfolder = image_path.split("/")[-2]
        if subfolder == "ok":
            tag = sly.Tag(ok)
        else:
            tag = sly.Tag(ko)

        class_index = image_path.split("/")[-4]
        obj_class = index_to_class[class_index]

        if ds_name == "test" and subfolder == "ko":
            masks_path = os.path.join(image_path.split(ds_name)[0], masks_folder_name)
            mask_name = get_file_name(image_path) + ".png"
            if image_path.split("/")[-4] == "03":
                mask_name = get_file_name(image_path) + ".bmp"
            mask_path = os.path.join(masks_path, subfolder, mask_name)
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]

            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                if curr_bitmap.area > 50:
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])


    product_1 = sly.ObjClass("product_1", sly.Bitmap)
    product_2 = sly.ObjClass("product_2", sly.Bitmap)
    product_3 = sly.ObjClass("product_3", sly.Bitmap)

    index_to_class = {"01": product_1, "02": product_2, "03": product_3}

    ok = sly.TagMeta("ok", sly.TagValueType.NONE)
    ko = sly.TagMeta("ko", sly.TagValueType.NONE)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[product_1, product_2, product_3], tag_metas=[ok, ko])
    api.project.update_meta(project.id, meta.to_json())

    train_images_pathes = glob.glob(dataset_path + "/*/train/*/*.bmp") + glob.glob(
        dataset_path + "/*/train/*/*.png"
    )
    test_images_pathes = glob.glob(dataset_path + "/*/test/*/*.bmp") + glob.glob(
        dataset_path + "/*/test/*/*.png"
    )

    ds_name_to_data = {"test": test_images_pathes, "train": train_images_pathes}

    for ds_name, images_pathes in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            img_names_batch = [
                im_path.split("/")[-4]
                + "_"
                + im_path.split("/")[-2]
                + "_"
                + get_file_name_with_ext(im_path)
                for im_path in img_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))
    return project



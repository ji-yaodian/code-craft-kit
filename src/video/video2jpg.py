

def video2jpg(video_file, output_dir):
    """
    mp4按帧转成jpg图片，去掉相同的图片
    :param video_file:
    :param output_dir:
    :return:
    """
    import cv2
    import os
    import hashlib
    cap = cv2.VideoCapture(video_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame_count = 0
    last_hash = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 100 == 0:
            print(f"frame_count: {frame_count}")
        frame = cv2.resize(frame, (224, 224))
        hash_str = hashlib.md5(frame).hexdigest()
        if hash_str == last_hash:
            continue
        last_hash = hash_str
        cv2.imwrite(os.path.join(output_dir, f"{frame_count}.jpg"), frame)
    cap.release()
    cv2.destroyAllWindows()
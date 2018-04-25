

def objectDetectionCap():  
    import cv2
    import numpy as np 
    import os
    import six.moves.urllib as urllib
    import sys
    import tarfile
    import tensorflow as tf
    import zipfile
    
    from collections import defaultdict
    from io import StringIO
    from matplotlib import pyplot as plt
    from PIL import Image
    

    # This is needed since the notebook is stored in the object_detection folder.
    cwd = os.getcwd()
    os.chdir(cwd)
    sys.path.append("../lib")
    from object_detection.utils import ops as utils_ops
    
    if tf.__version__ < '1.4.0':
      raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
    
    
    # ## Env setup
    
    
    # This is needed to display the images.
    get_ipython().magic('matplotlib inline')
    
    
    # ## Object detection imports
    # Here are the imports from the object detection module.
    
    
    from utils import label_map_util
    
    from utils import visualization_utils as vis_util
    
    
    # # Model preparation 
    
    # ## Variables
    # 
    # Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
    # 
    # By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
    
    
    # What model to download.
    MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
    MODEL_FILE = MODEL_NAME + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
    
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    
    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    
    NUM_CLASSES = 90
    
   
    # ## Download Model
    
#    opener = urllib.request.URLopener()
#    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#    tar_file = tarfile.open(MODEL_FILE)
#    for file in tar_file.getmembers():
#      file_name = os.path.basename(file.name)
#      if 'frozen_inference_graph.pb' in file_name:
#        tar_file.extract(file, os.getcwd())
   
    
    # ## Load a (frozen) Tensorflow model into memory.
    
    
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    
    
    # ## Loading label map
    # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
    
    
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    
    cap = cv2.VideoCapture(0)
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
       ret = True
       while (ret):
          ret,image_np = cap.read()
          image_np_expanded = np.expand_dims(image_np, axis=0)
          image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
          boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
          scores = detection_graph.get_tensor_by_name('detection_scores:0')
          classes = detection_graph.get_tensor_by_name('detection_classes:0')
          num_detections = detection_graph.get_tensor_by_name('num_detections:0')
          (boxes, scores, classes, num_detections) = sess.run(
                  [boxes, scores, classes, num_detections],
                  feed_dict={image_tensor: image_np_expanded})
          vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              use_normalized_coordinates=True,
              line_thickness=8)
          cv2.imshow('image', cv2.resize(image_np,(1280,800)))
          if cv2.waitKey(25) & 0xFF == ord('q'):
              cv2.destroyAllWindows()
              cap.release()
              break
    
    
    

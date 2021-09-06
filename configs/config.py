"""CNN - LSTM config system
This file specifies default config options for the model used.
"""

# DEFINE THE DIFFERENT PATH WHERE THE TREE MODEL WILL SAVE THE RESULT

from configs.collections import AttrDict

__C = AttrDict()

# Users can get the configuration by:
#   from config.config import cfg
cfg = __C

# ####################################################################################################################################
__C.SAVE_WEIGHT_PATH = {'single': "/home/aivdepth/saved_models/single_frame/"}
__C.SAVE_RESULTS_PATH = {'single': "/home/aivdepth/test_results/single_frame/"}
# __C.SAVE_VIDEO_PATH = {"/home/aivdepth/Video_dataset/"} #todo immagine con traiettorie finale e originale
__C.TENSORBOARD_PATH = {'single': "/home/aivdepth/tensorboard_runs/single_frame/"}
__C.DATASET_PATH = "/home/aivdepth/datasets/images_dataset/"
# __C.DATASET_PATH = {'processed': "/home/aivdepth/datasets/images_dataset_processed/",  # ne metterei uno e basta
#                     'original': "/home/aivdepth/datasets/images_dataset/"}
__C.SVO_DATASET_PATH = "/home/aivdepth/datasets/video_dataset/svo/"
__C.CSV_DATASET_PATH = "/home/aivdepth/datasets/csv_dataset/"
__C.JSON_DATASET_PATH = "/home/aivdepth/datasets/json_dataset/"
# ####################################################################################################################################
#
# TRAINING PARAMETERS
#
# ####################################################################################################################################

__C.TRAIN = AttrDict()

# ####################################################################################################################################
#
# DEFINE THE DIMENSION
#
# ####################################################################################################################################

#
# Define the hidden and cell state dimension for the tree models and LSTM layers
#

__C.IN_CHANNELS = {'single': 3}
__C.DIMENSION = {'single': 128}
__C.LAYERS = 2

# ####################################################################################################################################
#
# DEFINE THE MODELS' COMMON PARAMETERS
#
# ####################################################################################################################################

#
# Define gradient clipping, batch size, learning rate and decrement period
# Decrement period: number of epochs after that we decrement the learning rate
# Gradient clipping: manca definizione
#
__C.TRAIN.GRADIENT_CLIP = 5
__C.TRAIN.BATCH_SIZE = 20
__C.TRAIN.LEARNING_RATE = 0.1
__C.TRAIN.DEC_PERIOD = 20

#
# Define some information of the dataset
# Len_sequence : define the lenght of the sequence to predict
# Shuffle: indicates if the images have to be shuffle
#
__C.TRAIN.LEN_SEQUENCES = 10  # 30
__C.TRAIN.SHUFFLE_T = True
__C.TRAIN.SHUFFLE_V = False

#
# Define loss function, the optimizer and the alpha and momentum optimizer parameters
# Define also the gamma parameter for the scheduler
# SGD:
# Alpha:
# Momentum:
# Gamma: define how much we decrease the learning rate
#
__C.TRAIN.ALPHA = 0.90
__C.TRAIN.MOMENTUM = 0.9
__C.TRAIN.GAMMA = 0.1
__C.TRAIN.OPTIMIZER = 'SGD'
__C.TRAIN.LOSS = 'MSE'

# ####################################################################################################################################
#
# TEST PARAMETERS
#
# ####################################################################################################################################


__C.TEST = AttrDict()

# ####################################################################################################################################
#
# DEFINE THE HIDDEN DIMENSION
#
# ####################################################################################################################################

# __C.TEST.HIDDEN_DIMENSION_DEPTH = 256
# __C.TEST.HIDDEN_DIMENSION_MULTIFRAME = 768
__C.TEST.HIDDEN_DIMENSION_SINGLEFRAME = 128

# ####################################################################################################################################
#
# DEFINE THE MODELS' COMMON PARAMETERS
#
# ####################################################################################################################################

#
# Define learning rate, batch size and loss
#

__C.TEST.LEARNING_RATE = 0.1
__C.TEST.BATCH_SIZE = 1
__C.TEST.LOSS = 'MSE'

#
# Define dataset descriptors
# Len_sequence : define the lenght of the sequence to predict
# Shuffle: indicates if the images have to be shuffle
#
__C.TEST.LEN_SEQUENCES = 10
__C.TEST.SHUFFLE = False

# #####################################################################################################################################

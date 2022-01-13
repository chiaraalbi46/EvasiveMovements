![GitHub contributors](https://img.shields.io/github/contributors/chiaraalbi46/EvasiveMovements?color=blue) ![GitHub repo size](https://img.shields.io/github/repo-size/chiaraalbi46/EvasiveMovements) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) ![ZED](https://img.shields.io/badge/ZED-3.5.0-blue) 

# Trajectory prediction: Evasive maneuvers

This repo contains the work made for the project of ***Image and Video Analysis*** course, at the **University of Florence**. Part of the code has been recovered from [this repository](https://github.com/giuliobz/AutonomousDriving).

The **goal** of the project is training a neural network (NN) to predict the future trajectories of a radio controlled car. The NN is fed with the frames of the videos recorded during some driving sessions, with a ZED camera mounted on the car. 

<p align="center">
  <img src="./Immagine1.JPG" />
</p>


## Environment and packages

In the following paragraph we explain some steps to recreate a usable environment. Conda package manager and Python 3.8 have been used. A GPU, with a memory > 2GB (at least for the version of ZED SDK we have used) is needed, in order to interact with ZED camera.

- First of all **ZED SDK** and **zed-python-api** have to be installed. Please follow the explanations to this [link](https://github.com/stereolabs/zed-python-api), for the correct setup. In this project ZED SDK version 3.5.0 has been used. We have to specify that for Windows OS, NVIDIA CUDA Development version 11.0 has to be installed (other versions doesn't match at the moment of the configuration).

- A usable conda environment can be directly created from the requirements.txt file, using the command:
    
    ``` git conda create --name <env> --file requirements.txt ```

    The requirements.txt file has been exported from an environment on Windows OS, so probably some packages don't correctly fit with different OS. A new conda environment can of course be created, with these commands:

    ```
    conda create --name EvasiveMovements python=3.8
    conda activate EvasiveMovements
    conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
    conda install -c conda-forge tensorboardx
    conda install -c anaconda -c conda-forge -c comet_ml comet_ml 
    ```
    Pytorch have been used as the machine learning framework. We suggest to look to this [link](https://pytorch.org/get-started/locally/) for different settings. Tensorboard support is present, but we prefer to work with [Comet.ml](https://www.comet.ml/site/), to monitor the training metrics. A registration is needed (you can use the Github account). There are [many ways](https://www.comet.ml/docs/python-sdk/advanced/#python-configuration) to integrate comet support in a project, but we suggest to save the API key generated, as described [here](https://www.comet.ml/docs/quick-start/), in a .comet.config file and to copy the following lines in your script:
    ```
    import comet_ml
    experiment = comet_ml.Experiment()
    ```
    The .comet.config file has to be placed in the folder, where the script is located. In the repo a blank .comet.config file is provided.


## Recommended Directory Structure for Training and Evaluation
You might have the same dataset structure for data. 
```
dataset                                    
│
├── images_dataset
│   ├── dx_stop_dx
│   ├── dx_stop_sx
│   ├── dx_walk_dx
│   ├── dx_back_sx
│   ├── normal
│   ├── sx_stop_sx
│   └── ...
│ 
├── csv_dataset
│   ├── train 
│   ├── validation
│   └── test
│
├── json_dataset
│   └── config
└──  
```

## File comments

- **./configs/config.py**: In this file there are all the settings, path and configurations. Please read all sections to make sure all work correctly.

- Create json and csv files
    - **create_video_json.py**: Save the coordinates of a video trajectory (Es. video220_traj.json). Files are saved in the used video folder './dataset/images_dataset/dx_stop_dx/video220/'.
    - **trajectories_json.py**: Create the trajectories' file from a json file of a video sequence. Files are saved in the folder './dataset/images_dataset/dx_stop_dx/video220/'.
    - **net_utilities.py**: Split dataset in train, test and validation and save data in json file in the folder './dataset/json_dataset/config/'   
    - **create_csv_file.py**: Create the CSV file from video sequences. File is saved in the folder  './dataset/csv_dataset/train/' (train_config_10_sequence.csv).

- Preprocessing 
    - **augmentation.py**: Flipping the images vertically (data augmentation). 
    - **preprocess.py**: Preprocessing of the left frames.  
    
- Video creation
    - **plot_image.py**: Transform coordinates in the image plane.
    
- Training and Testing
    - **main_comet.py**: Train and test the CNN and LSTM model.


## Arguments to run main_comet.py
```
python main_comet.py --train_path = path of the train csv file
                     --valid_path = path of the validation csv file
                     --test_path = path of the test csv file
                     --epochs = number of epochs
                     --device = choose GPU
                     --proj_exp = define comet ml project folder
                     --name_exp = define comet ml experiment
                     --plot_step = number of graphics during train on comet
                     --shuffle_train = shuffle data of train
                     --len_seq = number of future points predicted (sequence length)
                     --lr = learning rate train
                     --opt = Optimizar
```



## Working example

The following lines describe the generical sequence of commands to run, in order to make some experiments. We assumed the data organization described above. In the example the frames are sampled with a rate of 10, the distance between two consecutive origins is 4 (origin_distance) and the future points to predict are 10 (future_points).

- **Coordinates and angles extraction:** 

    ```python create_video_json.py --video .../svo_cut/ --dest .../datasets/images_dataset/ --step 10 ```

- **Real trajectory creation:** 

    ```python trajectories_json.py --video_json_path .../datasets/images_dataset/ --point_future 10 --origin_distance 4 ```

- **Data augmentation:** ```python augmentation.py --folder_path .../datasets/images_dataset/ --od 4 --fp 10 ```

- **Preprocessing:** ```python preprocess.py --folder .../datasets/images_dataset/ ``` 

    Add ```--flip 1``` to preprocess the augmented frames.

- **Dataset split:** 
    
    ```python net_utilities.py --train_p 60 --test_p 20 --conf config0 ```

- **CSV creation:**

    ```python create_csv_file.py --config_f config0 --type train --len_seq 10 --od 4 --fp 10 --project od4_fp10```

    Change ```--type validation``` or ```--type test``` for validation and test set. Add ```--flip 1``` to also take into account the augmented frames.

- **Train:**

    ```python main_comet.py --train_path .../datasets/csv_dataset/od4_fp10/train/train_config0_10_sequence.csv --valid_path .../datasets/csv_dataset/od4_fp10/validation/validation_config0_10_sequence.csv --epochs 600 --name_exp od4_fp10 --proj_exp evasion --plot_step 1 --shuffle_train True ```

- **Test:** 

    ```python main_comet.py --test_path .../datasets/csv_dataset/od4_fp10/test/test_config0_10_sequence.csv --model_path .../saved_models/single_frame/od4_fp10/weight_600_lenseq_10_.../weight_....pth --name_exp od4_fp10 --proj_exp evasion``` 

    We use the weights at the epoch in which the global validation loss reaches its minimum. This value can be found through Comet.ml interface. 


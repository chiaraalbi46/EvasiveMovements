from datetime import datetime
from comet_ml import Experiment
import argparse
import os
import torch
from torch.utils.data import TensorDataset, DataLoader
from configs.config import cfg
from initialize_model import initialize_model
from load_dataset import load_data_singleframe
from test import test
from train_comet import train


# todo fare config con path locali
########################################################################################################################
# STARTING THE RAINING OF THE NET
########################################################################################################################


def main():
    parser = argparse.ArgumentParser(description="Train the CNN and LSTM model")
    parser.add_argument("--train_path", dest="train", default=None, help="path of the train csv file")
    parser.add_argument("--valid_path", dest="valid", default=None, help="path of the validation csv file")
    parser.add_argument("--test_path", dest="test", default=None, help="path of the test csv file")
    parser.add_argument("--model_path", dest="model", default=None, help="path of the model weight")
    parser.add_argument("--epochs", dest="epochs", default=200, help="number of epochs")
    parser.add_argument("--val_period", dest="period", default=1, help="choose when use the validation")
    parser.add_argument("--device", dest="device", default='0', help="choose GPU")
    parser.add_argument("--model_type", dest="model_type", default='single',
                        help="define the model to use: sigle-frame, multi-frame or depth")
    parser.add_argument("--proj_exp", dest="name_proj", default='evasive',
                        help="define comet ml project folder")
    parser.add_argument("--name_exp", dest="name_exp", default=None,
                        help="define comet ml experiment")
    parser.add_argument("--plot_step", dest="plot_step", default=2,
                        help="number of graphics during train on comet")
    parser.add_argument("--shuffle_train", dest="shuffle_train", default=None,  # False
                        help="number of graphics during train on comet")
    parser.add_argument("--len_seq", dest="len_seq", default=10,
                        help="number of future points predicted (sequence lenght)")  # per train, validation e test
    # TODO:rivedere ...
    # prenderebbe i valori del config ma per ora passiamolo perchè dobbiamo fare prove con 10/30

    args = parser.parse_args()

    print("SHUFFLE TRAIN: ", bool(args.shuffle_train))
    len_seq = int(args.len_seq)
    project = args.name_exp
    experiment = Experiment(project_name=args.name_proj)
    experiment.set_name(args.name_exp)

    if args.train is None and args.test is None:
        print("you have to decide : do train or test")
        exit()

    ####################################################################################################################
    # TRAIN PHASE
    ####################################################################################################################
    if args.test is None:

        if args.valid is None:
            print("please insert valid")
            exit()
        else:

            # current date and time
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            # dir_name = os.path.dirname(os.path.abspath(__file__))  # path a EvaisveM.

            # save_weight_path = dir_name + cfg.SAVE_WEIGHT_PATH[
            #     args.model_type] + 'weight_' + args.epochs + '_lenseq_' + str(cfg.TRAIN.LEN_SEQUENCES) + '_' + str(
            # #     timestamp)
            # tensor_board_path = dir_name + cfg.TENSORBOARD_PATH[
            #     args.model_type] + "weight_" + args.epochs + '_lenseq_' + str(cfg.TRAIN.LEN_SEQUENCES) + '_' + str(
            #     timestamp)
            # todo aggiungere if se si fa in locale per path

            save_weight_path = cfg.SAVE_WEIGHT_PATH[args.model_type] + project + '/' + 'weight_' + args.epochs + \
                               '_lenseq_' + str(len_seq) + '_' + str(timestamp)

            tensor_board_path = cfg.TENSORBOARD_PATH[
                                    args.model_type] + project + '/' + "weight_" + args.epochs + '_lenseq_' + \
                                str(len_seq) + '_' + str(timestamp)

            if not os.path.exists(save_weight_path):
                os.makedirs(save_weight_path)

            if not os.path.exists(tensor_board_path):
                os.makedirs(tensor_board_path)

            print()
            print("SUMMARIZE : ")
            print()
            print("train data path: {}".format(args.train))
            print("valid data path: {}".format(args.valid))
            print("weight save path: {}".format(save_weight_path))
            print("epoch: {}".format(args.epochs))
            print("validation period: {}".format(args.period))
            print("batch size: {}".format(cfg.TRAIN.BATCH_SIZE))
            print("learning rate: {}".format(cfg.TRAIN.LEARNING_RATE))
            print("GPU device: {}".format(args.device))
            print("len_seq: {}".format(args.len_seq))  # cfg.TRAIN.LEN_SEQUENCES
            print("hidden_dimension: {}".format(cfg.DIMENSION[args.model_type]))
            print("Loss Function: {}".format(cfg.TRAIN.LOSS))
            print("Optimizer: {}".format(cfg.TRAIN.OPTIMIZER))
            print("Decrement period: {}".format(cfg.TRAIN.DEC_PERIOD))
            print("num_layers: {}".format(cfg.LAYERS))
            print("you are working with {} model".format(args.model_type))
            print("To use tensorboardX log this --logdir : " + tensor_board_path)
            print()

            hyper_params = {
                "num_layers": cfg.LAYERS,
                "batch_size": cfg.TRAIN.BATCH_SIZE,
                "num_epochs": args.epochs,
                "learning_rate": cfg.TRAIN.LEARNING_RATE
            }

            experiment.log_parameters(hyper_params)

            ##### todo

            train_images, train_coordinates, train_paths = load_data_singleframe(csv_path=args.train, len_sequence=len_seq)
            # cfg.TRAIN.LEN_SEQUENCES
            valid_images, valid_coordinates, val_paths = load_data_singleframe(csv_path=args.valid, len_sequence=len_seq)

            # model, criterion, optimizer = initialize_model(model_type=args.model_type, cfg=cfg, mode='train')
            model, criterion, optimizer = initialize_model(model_type=args.model_type, cfg=cfg, mode='train',
                                                           len_seq=len_seq)  # add len_seq

            experiment.set_model_graph(model)

            train_data = TensorDataset(torch.from_numpy(train_images), torch.from_numpy(train_coordinates))
            val_data = TensorDataset(torch.from_numpy(valid_images), torch.from_numpy(valid_coordinates))

            # train_loader = DataLoader(train_data, shuffle=cfg.TRAIN.SHUFFLE_T, batch_size=cfg.TRAIN.BATCH_SIZE,
            #                           drop_last=True)
            train_loader = DataLoader(train_data, shuffle=bool(args.shuffle_train), batch_size=cfg.TRAIN.BATCH_SIZE,
                                      drop_last=True)
            val_loader = DataLoader(val_data, shuffle=cfg.TRAIN.SHUFFLE_V, batch_size=cfg.TRAIN.BATCH_SIZE,
                                    drop_last=True)

            train(model=model, criterion=criterion, optimizer=optimizer, train_loader=train_loader,
                  val_loader=val_loader, epochs=int(args.epochs), val_period=int(args.period),
                  save_weights=save_weight_path, event_log_path=tensor_board_path, dev=args.device, cfg=cfg,
                  exp=experiment, train_p=train_paths, val_p=val_paths, plot_step=int(args.plot_step))

    ####################################################################################################################
    # TEST PHASE
    ####################################################################################################################

    if args.train is None:
        if args.model is None:
            print("please insert the path to load the model for the test")
            exit()
        else:

            print()
            print("SUMMARIZE : ")
            print()
            print("test data path: {}".format(args.test))
            print("model path: {}".format(args.model))
            print("batch size: {}".format(cfg.TEST.BATCH_SIZE))
            print("hidden dimension: {}".format(cfg.DIMENSION[args.model_type]))
            print("GPU device: {}".format(args.device))
            print("len_seq: {}".format(len_seq))  # cfg.TEST.LEN_SEQUENCES
            print("Loss Function: {}".format(cfg.TRAIN.LOSS))
            print("you are working with {} model".format(args.model_type))
            print()

            save_path = cfg.SAVE_RESULTS_PATH[args.model_type] + project + '/'
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            test_images, test_coordinates, image_path = load_data_singleframe(csv_path=args.test,
                                                                              len_sequence=len_seq)
            # cfg.TEST.LEN_SEQUENCES

            model, criterion = initialize_model(model_type=args.model_type, cfg=cfg, mode='teTRAIst')

            test_data = TensorDataset(torch.from_numpy(test_images), torch.from_numpy(test_coordinates))

            test_loader = DataLoader(test_data, shuffle=cfg.TEST.SHUFFLE, batch_size=cfg.TEST.BATCH_SIZE,
                                     drop_last=True)

            test(model=model, criterion=criterion, model_path=args.model, test_loader=test_loader,
                 paths=image_path, dev=args.device, save_path=save_path)  # exp=experiment


if __name__ == '__main__':
    main()

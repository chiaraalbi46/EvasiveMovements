import torch
import torch.nn as nn
from model import NET


def initialize_model(model_type, cfg, mode, len_seq):  # ho aggiunto il passaggio di len_seq ...rivedere
    if mode == 'train':
        batch_size = cfg.TRAIN.BATCH_SIZE
        # len_seq = cfg.TRAIN.LEN_SEQUENCES
    elif mode == 'test':
        batch_size = cfg.TEST.BATCH_SIZE
        # len_seq = cfg.TEST.LEN_SEQUENCES
    else:
        print('Error occurrent')
        exit()

    model = NET(len_seq=len_seq, batch_size=batch_size, hidden_dimension=cfg.DIMENSION[model_type],
                num_layers=cfg.LAYERS, in_channels=cfg.IN_CHANNELS[model_type])

    criterion = nn.MSELoss()

    if mode == 'train':

        if cfg.TRAIN.OPTIMIZER == 'Adam':
            optimizer = torch.optim.Adam(model.parameters(), lr=cfg.TRAIN.LEARNING_RATE)
        elif cfg.TRAIN.OPTIMIZER == 'SGD':
            optimizer = torch.optim.SGD(model.parameters(), lr=cfg.TRAIN.LEARNING_RATE, momentum=cfg.TRAIN.MOMENTUM)
        elif cfg.TRAIN.OPTIMIZER == 'RMS':
            optimizer = torch.optim.RMSprop(model.parameters(), lr=cfg.TRAIN.LEARNING_RATE, alpha=cfg.TRAIN.ALPHA,
                                            momentum=cfg.TRAIN.MOMENTUM)

        return model, criterion, optimizer

    else:

        return model, criterion

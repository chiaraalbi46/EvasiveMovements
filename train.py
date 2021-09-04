import sys, os, math, torch

sys.path.insert(1, '/home/biondibazzanti/AutonomousDriving/Pytorch/models')
#from utils.utilities import export_plot_from_tensorboard
from torch.optim.lr_scheduler import StepLR
from torch.utils.tensorboard import SummaryWriter
import torch.nn as nn
import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
from torchvision.utils import make_grid

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import matplotlib.pyplot as plt


def export_plot_from_tensorboard(event_path, save_path):
    event_acc = EventAccumulator(event_path)
    event_acc.Reload()
    for element in event_acc.Tags()['scalars']:
        _, step_nums, vals = zip(*event_acc.Scalars(element))
        plt.plot(list(step_nums), list(vals))
        tmp = element.split("/")
        plt.savefig(save_path + "/" + tmp[1] + '.png')
        plt.clf()


def train(model, criterion, optimizer, train_loader, val_loader, epochs, val_period, save_weights, event_log_path, dev,
          cfg):
    limit = 1e-07
    global_min_val_loss = np.Inf
    iteration = 1

    writer = SummaryWriter(event_log_path)
    val_losses = {}
    train_losses = {}

    device = torch.device('cuda:' + dev)

    torch.cuda.reset_max_memory_allocated(device)
    model.to(device)

    print()
    print("Starting training the model")

    for i in range(epochs):

        print('*' * 100)
        print("Epoch : {}".format(i + 1))
        model.train()
        scheduler = StepLR(optimizer, step_size=cfg.TRAIN.DEC_PERIOD, gamma=cfg.TRAIN.GAMMA)

        for image, labels in train_loader:
            optimizer.zero_grad()

            train_inputs = image.to(device).float()
            out = model(train_inputs, device)

            loss = criterion(out, labels.float())

            if i in train_losses:
                train_losses[i].append(loss.item())
            else:
                train_losses[i] = [loss.item()]

            # tensorboard utilities
            writer.add_scalar('Training/train_loss_value', loss.item(), iteration)
            iteration += 1

            # compute gradients and optimizer step
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), cfg.TRAIN.GRADIENT_CLIP)
            optimizer.step()

        writer.add_scalar('Training/train_global_loss', sum(train_losses[i]) / len(train_losses[i]), i + 1)
        print("Epoch: {}/{}".format(i + 1, epochs),
              "Loss : {}".format(sum(train_losses[i]) / len(train_losses[i])))

        #### Validation step

        if (i + 1) % val_period == 0:

            print()
            print("Starting valid test")
            model.eval()

            with torch.no_grad():

                for val_image, val_labels in val_loader:

                    val_image = val_image.to(device)
                    val_out = model(val_image.float(), device)

                    val_loss = criterion(val_out, val_labels.float())

                    if i in val_losses:
                        val_losses[i].append(val_loss.item())
                    else:
                        val_losses[i] = [val_loss.item()]

                    writer.add_scalar('Validation/valid_loss_value', val_loss.item(), iteration)

            writer.add_scalar('Validation/valid_global_loss', sum(val_losses[i]) / len(val_losses[i]), i + 1)

            print("End valid test")
            print("Train Loss: {:.3f} - ".format(sum(train_losses[i]) / len(train_losses[i])),
                  "Validation Loss: {:.3f}".format(sum(val_losses[i]) / len(val_losses[i])))

            torch.save(model.state_dict(),
                       save_weights + '/weight_' + str(sum(val_losses[i]) / len(val_losses[i])) + '_' + str(
                           i + 1) + '.pth')

        scheduler.step()

    writer.close()
    print()
    print("Save losses graphs")
    onlyfile = [f for f in listdir(event_log_path) if isfile(join(event_log_path, f))]
    export_plot_from_tensorboard(event_log_path + "/" + onlyfile[0], save_weights)
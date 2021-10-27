""" train with comet integration """


import torch
from torch.optim.lr_scheduler import StepLR
from torch.utils.tensorboard import SummaryWriter
import torch.nn as nn
import numpy as np
from os import listdir
from os.path import isfile, join
from trajectory_images import plot_data

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import matplotlib.pyplot as plt
#from metrics_eval import ADE, FDE


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
          cfg, exp, train_p, val_p, plot_step):
    print('boh', val_loader)
    limit = 1e-07
    global_min_val_loss = np.Inf
    iteration = 1

    writer = SummaryWriter(event_log_path)
    val_losses = {}
    train_losses = {}

    # ADE
    val_ades = {}
    train_ades = {}

    # FDE
    val_fdes = {}
    train_fdes = {}

    # device = torch.device('cuda:' + dev)
    device = torch.device('cuda')

    torch.cuda.reset_max_memory_allocated(device)
    model.to(device)

    print()
    print("Starting training the model")
    # with exp.train():
    for i in range(epochs):

        print('*' * 100)
        print("Epoch : {}".format(i + 1))

        # exp.set_epoch(i+1)

        model.train()
        scheduler = StepLR(optimizer, step_size=cfg.TRAIN.DEC_PERIOD, gamma=cfg.TRAIN.GAMMA)

        # per plot comet ml
        epoca = 'ep_' + str(i + 1) + '_'
        type_name = 'train_'

        # with exp.context_manager('epoca'):

        # Train
        with exp.context_manager('train'):
            current_path = 0
            for image, labels in train_loader:
                optimizer.zero_grad()

                train_inputs = image.to(device).float()
                out = model(train_inputs, device)

                loss = criterion(out, labels.float())
                #
                # # ADE
                # ade = ADE(out, labels.float())
                #
                # # ADE
                # fde = FDE(out, labels.float())

                if i in train_losses:
                    train_losses[i].append(loss.item())
                else:
                    train_losses[i] = [loss.item()]

                # if i in train_ades:
                #     train_ades[i].append(ade)
                # else:
                #     train_ades[i] = [ade]
                #
                # if i in train_fdes:
                #     train_fdes[i].append(fde)
                # else:
                #     train_fdes[i] = [fde]

                num_plots = int(epochs / plot_step)
                # if (i+1) % num_plots == 0:
                #     for k in range(len(out)):
                #         predicted = out[k].detach().numpy()
                #         real = labels[k].detach().numpy()
                         # if 'flip' in train_p[current_path]:
                            #   print('path', val_path)
                          #   path = train_p[current_path].replace("left_frames_flip_processed", "left_frames_flip")
                          #else:
                            # path = val_p[current_path].replace("left_frames_processed", "left_frames")
                #         #path = train_p[current_path].replace("left_frames_processed", "left_frames")
                #         # plot_data(real, predicted, exp, k, iteration, path, epoca, type_name)  # k, l, path
                #         plot_data(real, predicted, exp, k, (i + 1), path, iteration)  # step = epoca
                #         current_path += 1

                # tensorboard utilities
                writer.add_scalar('Training/train_loss_value', loss.item(), iteration)

                # comet ml
                exp.log_metric('train_loss_value', loss.item(), step=iteration)  # loss iteration (batch)

                # exp.log_metric('train_ade_value', ade, step=iteration)  # ade iteration (batch)
                # exp.log_metric('train_fde_value', fde, step=iteration)  #fde iteration (batch)

                iteration += 1

                # compute gradients and optimizer step
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), cfg.TRAIN.GRADIENT_CLIP)
                optimizer.step()

        writer.add_scalar('Training/train_global_loss', sum(train_losses[i]) / len(train_losses[i]), i + 1)

        # comet ml
        exp.log_metric('train_global_loss', sum(train_losses[i]) / len(train_losses[i]), step=i + 1)  # loss  epoca

        # exp.log_metric('train_global_ade', sum(train_ades[i]) / len(train_ades[i]), step=i + 1)  # ade epoca
        # exp.log_metric('train_global_fde', sum(train_fdes[i]) / len(train_fdes[i]), step=i + 1)  # fde epoca

        print("Epoch: {}/{}".format(i + 1, epochs),
              "Loss : {}".format(sum(train_losses[i]) / len(train_losses[i])))

        #### Validation step

        if (i + 1) % val_period == 0:

            print()
            print("Starting valid test")
            model.eval()

            type_name = 'val_'

            current_path = 0
            with torch.no_grad():
                with exp.context_manager('validation'):

                    for val_image, val_labels in val_loader:

                        val_image = val_image.to(device)

                        val_out = model(val_image.float(), device)

                        val_loss = criterion(val_out, val_labels.float())

                        # # ADE
                        # val_ade = ADE(val_out, val_labels.float())
                        #
                        # # FDE
                        # val_fde = FDE(val_out, val_labels.float())

                        if i in val_losses:
                            val_losses[i].append(val_loss.item())
                        else:
                            val_losses[i] = [val_loss.item()]

                        # if i in val_ades:
                        #     val_ades[i].append(val_ade)
                        # else:
                        #     val_ades[i] = [val_ade]
                        #
                        # if i in val_fdes:
                        #     val_fdes[i].append(val_fde)
                        # else:
                        #     val_fdes[i] = [val_fde]


                        if (i + 1) % num_plots == 0:
                            for k in range(len(val_out)):
                                val_predicted = val_out[k].detach().numpy()
                                val_real = val_labels[k].detach().numpy()
                                #print('predetti', val_predicted)
                                #print('real', val_real)
                                if 'flip' in val_p[current_path]:
                                 #   print('path', val_path)
                                    val_path = val_p[current_path].replace("left_frames_flip_processed", "left_frames_flip")
                                else:
                                    val_path = val_p[current_path].replace("left_frames_processed", "left_frames")
                                # plot_data(val_real, val_predicted, exp, k, iteration, val_path, epoca, type_name)
                                plot_data(val_real, val_predicted, exp, k, (i + 1), val_path, iteration)
                                current_path += 1

                        writer.add_scalar('Validation/valid_loss_value', val_loss.item(), iteration)

                        # comet ml
                        exp.log_metric('valid_loss_value', val_loss.item(), step=iteration)

                        # exp.log_metric('valid_ade_value', val_ade, step=iteration)
                        # exp.log_metric('valid_fde_value', val_fde, step=iteration)

            writer.add_scalar('Validation/valid_global_loss', sum(val_losses[i]) / len(val_losses[i]), i + 1)

            # comet ml
            exp.log_metric('valid_global_loss', sum(val_losses[i]) / len(val_losses[i]), step=i + 1)  # loss  epoca

            # exp.log_metric('valid_global_ade', sum(val_ades[i]) / len(val_ades[i]), step=i + 1)  # ade  epoca
            # exp.log_metric('valid_global_fde', sum(val_fdes[i]) / len(val_fdes[i]), step=i + 1)  # fde  epoca

            print("End valid test")
            print("Train Loss: {:.3f} - ".format(sum(train_losses[i]) / len(train_losses[i])),
                  "Validation Loss: {:.3f}".format(sum(val_losses[i]) / len(val_losses[i])))

            torch.save(model.state_dict(),
                       save_weights + '/weight_' + str(sum(val_losses[i]) / len(val_losses[i])) + '_' + str(
                           i + 1) + '.pth')
        # exp.log_epoch_end(i + 1)
        scheduler.step()

    writer.close()
    exp.end()
    print()
    print("Save losses graphs")
    onlyfile = [f for f in listdir(event_log_path) if isfile(join(event_log_path, f))]
    export_plot_from_tensorboard(event_log_path + "/" + onlyfile[0], save_weights)

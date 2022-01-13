import os
import csv
import torch
# from trajectory_images import save_video
from configs.config import cfg
import numpy as np
from metrics_eval import ADE, FDE
from net_utilities import write_json
import json


def test(model, criterion, model_path, test_loader, paths, dev, save_path):
    test_losses = []

    test_ades = []
    test_fdes = []

    # csv_file = cfg.SAVE_RESULTS_PATH[model_type] + project + '/' + "summarize_test.csv"
    csv_file = save_path + "summarize_test.csv"
    # video_name = dir_name + cfg.SAVE_VIDEO_PATH[model_type] + "summarize_video.avi"

    if os.path.exists(csv_file):
        os.remove(csv_file)

    model.load_state_dict(torch.load(model_path))

    # device = torch.device('cuda:' + str(dev))
    device = torch.device('cuda')
    model.to(device)
    model.eval()

    print("Starting testing the model")

    current_path = 0

    with open(csv_file, 'w') as result_file:
        with torch.no_grad():
            filewriter = csv.writer(result_file)
            for inputs, labels in test_loader:

                image = inputs.to(device)
                output = model(image.float(), device)

                test_loss = criterion(output, labels.float())

                # ADE
                test_ade = ADE(output, labels.float())

                # FDE
                test_fde = FDE(output, labels.float())

                test_losses.append(test_loss.item())

                test_ades.append(test_ade)
                test_fdes.append(test_fde)

                for i in range(len(output)):
                    predicted = output[i].detach().numpy()
                    real = labels[i].detach().numpy()
                    path = paths[current_path].replace("left_frames_processed", "left_frames")
                    lines = [path, predicted.tolist(), real.tolist()]
                    filewriter.writerow(lines)
                    current_path += 1


    print()
    print("saved resume csv file in " + csv_file)
    print()
    print("Test loss: {:.3f}".format(np.mean(test_losses)))
    print('*' * 100)
    print()
    print("Test ADE: {:.3f}".format(np.mean(test_ades)))
    print('*' * 100)
    print()
    print("Test FDE: {:.3f}".format(np.mean(test_fdes)))
    print('*' * 100)
    result = {'Loss': np.mean(test_losses), 'ADE': np.mean(test_ades), 'FDE:': np.mean(test_fdes)}
    write_json(str(result), save_path +  '/test_result.json')
    # print('Starting Video Creation')
    #
    # save_video(video_name=video_name, csv_path=csv_file, len_seq=cfg.TEST.LEN_SEQUENCES, model_type=model_type)

import os
import csv
import torch
# from trajectory_images import save_video
from configs.config import cfg
import numpy as np


def test(model, criterion, model_path, test_loader, paths, dev, model_type):
    num_correct = 0
    test_losses = []
    distances = []

    csv_file = cfg.SAVE_RESULTS_PATH[model_type] + "summarize_test.csv"
    # video_name = dir_name + cfg.SAVE_VIDEO_PATH[model_type] + "summarize_video.avi"

    if os.path.exists(csv_file):
        os.remove(csv_file)

    model.load_state_dict(torch.load(model_path))

    # device = torch.device('cuda:' + str(dev))
    device = torch.device('cuda')
    model.to(device)
    model.eval()

    print("starting testig the model")

    current_path = 0

    with open(csv_file, 'w') as result_file:
        with torch.no_grad():
            filewriter = csv.writer(result_file)
            for inputs, labels in test_loader:

                image = inputs.to(device)
                output = model(image.float(), device)

                test_loss = criterion(output, labels.float())

                test_losses.append(test_loss.item())

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
    # print('Starting Video Creation')
    #
    # save_video(video_name=video_name, csv_path=csv_file, len_seq=cfg.TEST.LEN_SEQUENCES, model_type=model_type)



####
# def test(test_loader, paths, dev, model_type):
# array_json = []
# for inputs, labels in test_loader:
#     print("INPUTS: ", inputs)
#     print("LABELS: ", labels)
#     for i in range(len(inputs)):
#         real = (labels[i].detach().numpy()).tolist()
#         path = paths[current_path].replace("left_frames_processed", "left_frames")
#
#         # lines = [path, predicted.tolist(), real.tolist()]
#         # filewriter.writerow(lines)
#         dict_frame = {'path': path, 'real': real, }
#         print("DICT: ", dict_frame)
#         array_json.append(dict_frame)
#         current_path += 1
#
# write_json(array_json, '/home/aivdepth/PROVA_OUTPUT_TEST1.json')
'''
L'obiettivo qui sarebbe quello di capire quali sono le matrici delle trasformazioni che portano la camera da un frame all'altro / da un frame rispetto al frame di riferimento.
Una volta capita la trasformazione potremmo applicarla a tutti i punti (un certo dato come parametro) che vogliamo riportare nel sistema di riferimento del frame desiderato.
Per adesso ci sono dei tentativi per capire come cambia camera_pose da un frame all'altro (estraiamo il vettore di traslazione e la matrice di rotazione ... o almeno pensiamo di farlo)
e la funzione transform_pose è presa da https://www.stereolabs.com/docs/positional-tracking/coordinate-frames/
'''

import sys
import pyzed.sl as sl


def transform_pose(pose, tx):
    transform_ = sl.Transform()
    transform_.set_identity()
    print("T0: ", transform_)

    # Translate the tracking frame by tx along the X axis
    transform_[0, 3] = tx
    # transform_[0][3] = tx
    print("T1: ", transform_)

    # Pose(new reference frame) = M.inverse() * pose (camera frame) * M, where M is the transform between the two frames
    transform_inv = sl.Transform()
    transform_inv.init_matrix(transform_)
    transform_inv.inverse()
    print("TINV: ", transform_inv)

    pose = transform_inv * pose * transform_

    return pose


if __name__ == '__main__':

    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                                    coordinate_units=sl.UNIT.METER,
                                    coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)

    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        spl = filepath.split('/')
        vid_name = spl[len(spl) - 1]
        spl1 = vid_name.split('.')
        vname = spl1[0]
        print(vname)
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)
        # print(init_params)
    else:
        print("svo no read")

    zed = sl.Camera()
    status = zed.open(init_params)

    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    tracking_params = sl.PositionalTrackingParameters()
    zed.enable_positional_tracking(tracking_params)

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()  # zed_pose
    # print("Pose prima tracking: ", camera_pose.pose_data(sl.Transform()))

    camera_info = zed.get_camera_information()

    py_translation = sl.Translation()
    pose_data = sl.Transform()
    nf = zed.get_svo_number_of_frames()
    print(nf)

    step = 100
    i = 0  # importante
    # grab parte comunque dall'inizio del video - se mettiamo dei valori diversi per i (>0) non partiamo dal numero di frame corrispondente al valore di i

    while i < nf:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:  # frame

           # quale dei due ? ci sono delle differenze negli output però chi è più giusto ? (per me REFERENCE_FRAME.WORLD ma bo)
           # tracking_state = zed.get_position(camera_pose)
            tracking_state = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)

            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                # print("FRAME: ", i)
                # print("Pose:  ", i, " tracking ", camera_pose.pose_data(sl.Transform()))
                # print("Traslation matrix: ", camera_pose.get_translation(py_translation).get())
                # print("Rotation matrix: ", camera_pose.get_rotation_matrix())

                # Rotation
                # rotation = camera_pose.get_rotation_vector()
                # text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))

                # Display the translation and timestamp
                # translation = sl.Translation()
                if i % step == 0:
                    print("FRAME: ", i)
                    # print("Traslation matrix: ", camera_pose.get_translation(py_translation).get())
                    print("Rotation matrix: ", camera_pose.get_rotation_matrix())
                    rotation = camera_pose.get_rotation_vector()
                    text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))
                    print("Rotation vector: ", text_rotation)
                    translation = py_translation
                    tx = round(camera_pose.get_translation(translation).get()[0], 3)
                    ty = round(camera_pose.get_translation(translation).get()[1], 3)
                    tz = round(camera_pose.get_translation(translation).get()[2], 3)
                    text_translation = str(
                        (round(translation.get()[0], 2), round(translation.get()[1], 2), round(translation.get()[2], 2)))
                    print("Translation: Tx: {0}, Ty: {1}, Tz {2}\n".format(tx, ty, tz))

                # pose_data = camera_pose.pose_data(sl.Transform)  # se lo mettiamo sembra fermarsi dopo la stampa di un solo frame

            i += 1

    # # Get the distance between the center of the camera and the left eye
    # translation_left_to_center = zed.get_camera_information().calibration_parameters.T[0]
    # print("translantion_ltc: ", translation_left_to_center)
    # print(type(translation_left_to_center))
    #
    # # Retrieve and transform the pose data into a new frame located at the center of the camera
    # print("Pose prima tracking: ", camera_pose.pose_data(sl.Transform()))
    # print("Pose data: ", camera_pose.pose_data())
    #
    # tracking_state = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)
    # # tracking_state = zed.get_position(camera_pose)
    # print("Pose dop tracking: ", camera_pose.pose_data(sl.Transform()))
    #
    # translation = sl.Translation()
    # tx = round(camera_pose.get_translation(translation).get()[0], 3)
    # ty = round(camera_pose.get_translation(translation).get()[1], 3)
    # tz = round(camera_pose.get_translation(translation).get()[2], 3)
    # print("Translation: Tx: {0}, Ty: {1}, Tz {2}\n".format(tx, ty, tz))
    # print("Camera pose type: ", type(camera_pose))
    #
    # # Traslazione lungo asse x
    # txt = 2.0
    # # tracking_state1 = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)
    # # tracking_state1 = zed.get_position(camera_pose)
    #
    # new_pose = transform_pose(camera_pose.pose_data(sl.Transform()), 200)
    # new_pose = sl.Pose(new_pose)
    # tracking_state1 = zed.get_position(new_pose, sl.REFERENCE_FRAME.WORLD)
    # print("New pose: ", new_pose)
    #
    #
    # translation1 = sl.Translation()
    # tx1 = round(new_pose.get_translation(translation1).get()[0], 3)
    # ty1 = round(new_pose.get_translation(translation1).get()[1], 3)
    # tz1 = round(new_pose.get_translation(translation1).get()[2], 3)
    #
    # print("Translation: Tx: {0}, Ty: {1}, Tz {2}\n".format(tx1, ty1, tz1))

    # Disable positional tracking and close the camera
    zed.disable_positional_tracking()
    zed.close()
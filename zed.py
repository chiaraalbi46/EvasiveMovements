'''
Corrisponde a quanto contenuto in https://github.com/stereolabs/zed-examples/blob/master/tutorials/tutorial%204%20-%20positional%20tracking/python/positional_tracking.py
'''

import pyzed.sl as sl
import sys
import ogl_viewer.tracking_viewer as gl

if __name__ == "__main__":

    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                                    coordinate_units=sl.UNIT.METER,
                                    coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)

    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    print(sys.argv)
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)
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

    camera_info = zed.get_camera_information()
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(camera_info.camera_model)

    py_translation = sl.Translation()
    pose_data = sl.Transform()

    text_translation = ""
    text_rotation = ""

    while viewer.is_available():
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                rotation = camera_pose.get_rotation_vector()
                translation = camera_pose.get_translation(py_translation)
                text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))
                text_translation = str(
                    (round(translation.get()[0], 2), round(translation.get()[1], 2), round(translation.get()[2], 2)))
                print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(translation.get()[0], translation.get()[1], translation.get()[2],
                                                                                       camera_pose.timestamp.get_milliseconds()))
                pose_data = camera_pose.pose_data(sl.Transform())
            viewer.updateData(pose_data, text_translation, text_rotation, tracking_state)

    viewer.exit()
    zed.close()
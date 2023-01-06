import logging
from pathlib import Path

import pandas as pd

from freemocap.configuration.paths_and_files_names import (
    MEDIAPIPE_BODY_3D_DATAFRAME_CSV_FILE_NAME,
    RAW_DATA_FOLDER_NAME,
)
from freemocap.core_processes.capture_volume_calibration.anipose_camera_calibration import (
    freemocap_anipose,
)
from freemocap.core_processes.capture_volume_calibration.anipose_camera_calibration.get_anipose_calibration_object import (
    load_anipose_calibration_toml_from_path,
)
from freemocap.core_processes.capture_volume_calibration.triangulate_3d_data import (
    triangulate_3d_data,
)
from freemocap.core_processes.detecting_things_in_2d_images.mediapipe_stuff.convert_mediapipe_npy_to_csv import (
    convert_mediapipe_npy_to_csv,
)
from freemocap.core_processes.detecting_things_in_2d_images.mediapipe_stuff.mediapipe_skeleton_detector import (
    MediaPipeSkeletonDetector,
)
from freemocap.core_processes.post_process_skeleton_data.estimate_skeleton_segment_lengths import (
    estimate_skeleton_segment_lengths,
    mediapipe_skeleton_segment_definitions,
    save_skeleton_segment_lengths_to_json,
)
from freemocap.core_processes.post_process_skeleton_data.gap_fill_filter_and_origin_align_skeleton_data import (
    gap_fill_filter_origin_align_3d_data_and_then_calculate_center_of_mass,
)
from freemocap.core_processes.session_processing_parameter_models.session_processing_parameter_models import (
    SessionProcessingParameterModel,
)
from freemocap.tests.test_mediapipe_2d_data_shape import (
    test_mediapipe_2d_data_shape,
)
from freemocap.tests.test_mediapipe_3d_data_shape import test_mediapipe_3d_data_shape

logger = logging.getLogger(__name__)


def process_session_folder(
    session_processing_parameter_model: SessionProcessingParameterModel,
):
    """
    Process a single session folder.

    Parameters
    ----------
    session_processing_parameter_model : SessionProcessingParameterModel
        SessionProcessingParameterModel object (contains all the paths and parameters necessary to process a session folder

    """

    s = session_processing_parameter_model  # make it smol

    if not Path(s.session_info.path_to_folder_of_synchronized_videos).exists():
        raise FileNotFoundError(
            f"Could not find synchronized_videos folder at {s.session_info.path_to_folder_of_synchronized_videos}"
        )

    logger.info("Detecting 2d skeletons...")
    # 2d skeleton detection
    mediapipe_skeleton_detector = MediaPipeSkeletonDetector(
        parameter_model=s.mediapipe_parameters,
    )

    mediapipe_2d_data = mediapipe_skeleton_detector.process_folder_full_of_videos(
        s.session_info.path_to_folder_of_synchronized_videos,
        Path(s.session_info.path_to_output_data_folder) / RAW_DATA_FOLDER_NAME,
    )

    assert test_mediapipe_2d_data_shape(
        s.session_info.path_to_folder_of_synchronized_videos,
        Path(s.session_info.path_to_output_data_folder) / RAW_DATA_FOLDER_NAME,
        mediapipe_2d_data,
    )

    logger.info("Triangulating 3d skeletons...")

    anipose_calibration_object = load_anipose_calibration_toml_from_path(
        camera_calibration_data_toml_path=s.session_info.path_to_calibration_toml_file,
        save_copy_of_calibration_to_this_path=s.session_info.path_to_session_folder,
    )
    (
        raw_skel3d_frame_marker_xyz,
        skeleton_reprojection_error_fr_mar,
    ) = triangulate_3d_data(
        anipose_calibration_object=anipose_calibration_object,
        mediapipe_2d_data=mediapipe_2d_data,
        output_data_folder_path=Path(s.session_info.path_to_output_data_folder)
        / RAW_DATA_FOLDER_NAME,
        mediapipe_confidence_cutoff_threshold=s.anipose_triangulate_3d_parameters.confidence_threshold_cutoff,
        use_triangulate_ransac=s.anipose_triangulate_3d_parameters.use_triangulate_ransac_method,
    )

    assert test_mediapipe_3d_data_shape(
        s.session_info.path_to_folder_of_synchronized_videos,
        Path(s.session_info.path_to_output_data_folder) / RAW_DATA_FOLDER_NAME,
        raw_skel3d_frame_marker_xyz,
        skeleton_reprojection_error_fr_mar,
    )

    logger.info(
        "Gap-filling, butterworth filtering, origin aligning 3d skeletons, then calculating center of mass ..."
    )

    skel3d_frame_marker_xyz = gap_fill_filter_origin_align_3d_data_and_then_calculate_center_of_mass(
        skel3d_frame_marker_xyz=raw_skel3d_frame_marker_xyz,
        skeleton_reprojection_error_fr_mar=skeleton_reprojection_error_fr_mar,
        path_to_folder_where_we_will_save_this_data=s.session_info.path_to_output_data_folder,
        sampling_rate=s.post_processing_parameters.framerate,
        cut_off=s.post_processing_parameters.butterworth_filter_parameters.cutoff_frequency,
        order=s.post_processing_parameters.butterworth_filter_parameters.order,
        reference_frame_number=None,
    )

    logger.info("Breaking up big `npy` into smaller bits and converting to `csv`...")
    # break up big NPY and save out csv's
    convert_mediapipe_npy_to_csv(
        mediapipe_3d_frame_trackedPoint_xyz=skel3d_frame_marker_xyz,
        output_data_folder_path=s.session_info.path_to_output_data_folder,
    )

    path_to_skeleton_body_csv = (
        Path(s.session_info.path_to_output_data_folder)
        / MEDIAPIPE_BODY_3D_DATAFRAME_CSV_FILE_NAME
    )
    skeleton_dataframe = pd.read_csv(path_to_skeleton_body_csv)

    logger.info("Estimating skeleton segment lengths...")
    skeleton_segment_lengths_dict = estimate_skeleton_segment_lengths(
        skeleton_dataframe=skeleton_dataframe,
        skeleton_segment_definitions=mediapipe_skeleton_segment_definitions,
    )

    save_skeleton_segment_lengths_to_json(
        s.session_info.path_to_output_data_folder, skeleton_segment_lengths_dict
    )


if __name__ == "__main__":

    from rich.pretty import pprint

    session_folder_path = Path(
        r"H:\My Drive\Biol2299_Fall2022\com_vs_bos_posture_data\sesh_2022-09-28_15_52_24_bbbbbb"
    )

    path_to_camera_calibration_toml = Path(
        r"H:\My Drive\Biol2299_Fall2022\calibration_recordings\sesh_2022-09-28_15_39_31_calibration\sesh_2022-09-28_15_39_31_calibration.toml"
    )

    path_to_blender_executable = Path(
        r"C:\Program Files\Blender Foundation\Blender 3.2\blender.exe"
    )

    anipose_calibration_object = freemocap_anipose.CameraGroup.load(
        str(path_to_camera_calibration_toml)
    )

    if Path(
        session_folder_path / "synchronized_videos"
    ).exists():  # freemocap version > v0.0.54 (aka `alpha`)
        synchronized_videos_folder_in = (
            Path(session_folder_path) / "synchronized_videos"
        )
    elif Path(
        session_folder_path / "SyncedVideos"
    ).exists():  # freemocap version <= v0.0.54 (aka `pre-alpha`)
        synchronized_videos_folder_in = Path(session_folder_path) / "SyncedVideos"
    else:
        print(f"No folder full of synchronized videos found for {session_folder_path}")
        raise FileNotFoundError

    output_data_folder = Path(session_folder_path) / "output_data"
    output_data_folder.mkdir(exist_ok=True, parents=True)

    session_processing_parameter_model = SessionProcessingParameterModel(
        path_to_session_folder=session_folder_path,
        path_to_output_data_folder=output_data_folder,
        path_to_folder_of_synchronized_videos=synchronized_videos_folder_in,
        anipose_calibration_object=anipose_calibration_object,
        path_to_blender_executable=path_to_blender_executable,
    )

    session_processing_parameter_model.anipose_triangulate_3d_parameters.use_triangulate_ransac_method = (
        False
    )

    session_processing_parameter_model.start_processing_at_stage = 2

    pprint(session_processing_parameter_model.dict(), expand_all=True)

    process_session_folder(session_processing_parameter_model)

    print("Done!")
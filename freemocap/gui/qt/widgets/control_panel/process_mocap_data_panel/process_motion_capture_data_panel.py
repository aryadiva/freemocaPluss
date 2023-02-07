import logging
import threading
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QGroupBox
from pyqtgraph.parametertree import Parameter, ParameterTree

from freemocap.gui.qt.widgets.control_panel.calibration_control_panel import CalibrationControlPanel
from freemocap.gui.qt.widgets.control_panel.process_mocap_data_panel.parameter_groups.create_3d_triangulation_parameter_group import (
    create_3d_triangulation_prarameter_group,
)
from freemocap.gui.qt.widgets.control_panel.process_mocap_data_panel.parameter_groups.create_mediapipe_parameter_group import (
    create_mediapipe_parameter_group,
)
from freemocap.gui.qt.widgets.control_panel.process_mocap_data_panel.parameter_groups.create_post_processing_parameter_group import (
    create_post_processing_parameter_group,
)
from freemocap.gui.qt.workers.process_motion_capture_data_thread_worker import (
    ProcessMotionCaptureDataThreadWorker,
)
from freemocap.parameter_info_models.recording_processing_parameter_models import (
    RecordingProcessingParameterModel,
)

logger = logging.getLogger(__name__)


class ProcessMotionCaptureDataPanel(QWidget):
    processing_finished_signal = pyqtSignal()

    def __init__(
        self,
        recording_processing_parameters: RecordingProcessingParameterModel,
        get_active_recording_info: Callable,
        kill_thread_event: threading.Event,
        parent=None,
    ):
        super().__init__(parent=parent)

        self._kill_thread_event = kill_thread_event
        self._get_active_recording_info = get_active_recording_info
        self._recording_processing_parameter_model = recording_processing_parameters
        self._recording_processing_parameter_model.recording_info_model = self._get_active_recording_info()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        vbox = QVBoxLayout()
        self._layout.addLayout(vbox)

        self._calibration_control_panel = CalibrationControlPanel(
            get_active_recording_info_callable=self._get_active_recording_info,
            kill_thread_event=self._kill_thread_event,
            parent=self,
        )
        vbox.addWidget(self._calibration_control_panel)

        self._process_motion_capture_data_button = QPushButton(
            "Process Motion Capture Videos",
        )
        self._process_motion_capture_data_button.clicked.connect(self._launch_process_motion_capture_data_thread_worker)
        self._layout.addWidget(self._process_motion_capture_data_button)

        self._parameter_tree_widget = ParameterTree(parent=self, showHeader=False)
        self._layout.addWidget(self._parameter_tree_widget)

        self._add_parameters_to_parameter_tree_widget(
            self._parameter_tree_widget,
            session_processing_parameter_model=self._recording_processing_parameter_model,
        )

        self._process_motion_capture_data_thread_worker = None

    @property
    def process_motion_capture_data_button(self):
        return self._process_motion_capture_data_button

    def calibrate_from_active_recording(self, charuco_square_size_mm: float):
        self._calibration_control_panel.calibrate_from_active_recording(charuco_square_size_mm=charuco_square_size_mm)

    def kill_running_threads(self):
        self._calibration_control_panel.kill_running_threads()
        if self._process_motion_capture_data_thread_worker is not None:
            self._process_motion_capture_data_thread_worker.kill()

    def _add_parameters_to_parameter_tree_widget(
        self,
        parameter_tree_widget: ParameterTree,
        session_processing_parameter_model: RecordingProcessingParameterModel,
    ):
        parameter_group = self._convert_session_processing_parameter_model_to_parameter_group(
            session_processing_parameter_model
        )
        parameter_tree_widget.setParameters(parameter_group, showTop=False)

        return parameter_group

    def _convert_session_processing_parameter_model_to_parameter_group(
        self,
        session_processing_parameter_model: RecordingProcessingParameterModel,
    ):

        return Parameter.create(
            name="Processing Parameters",
            type="group",
            children=[
                dict(
                    name="2d Image Trackers",
                    type="group",
                    children=[
                        self._create_new_skip_this_step_parameter(),
                        create_mediapipe_parameter_group(session_processing_parameter_model.mediapipe_parameters_model),
                    ],
                    tip="Methods for tracking 2d points in images (e.g. mediapipe, deeplabcut(TODO), openpose(TODO), etc ...)",
                ),
                dict(
                    name="3d triangulation methods",
                    type="group",
                    children=[
                        self._create_new_skip_this_step_parameter(),
                        create_3d_triangulation_prarameter_group(
                            session_processing_parameter_model.anipose_triangulate_3d_parameters_model
                        ),
                    ],
                    tip="Methods for triangulating 3d points from 2d points (using epipolar geometry and the 'camera_calibration' data).",
                ),
                dict(
                    name="Post Processing (data cleaning)",
                    type="group",
                    children=[
                        self._create_new_skip_this_step_parameter(),
                        create_post_processing_parameter_group(
                            session_processing_parameter_model.post_processing_parameters_model
                        ),
                    ],
                    tip="Methods for cleaning up the data (e.g. filtering/smoothing, gap filling, etc ...)"
                    "TODO - Add/expose more post processing methods here (e.g. gap filling, outlier removal, etc ...)",
                ),
            ],
        )

    def _extract_session_parameter_model_from_parameter_tree(
        self,
    ) -> RecordingProcessingParameterModel:
        session_processing_parameter_model = self._recording_processing_parameter_model

        logger.debug(
            "TODO - extract the parameter values from the parameter tree and populate the session_parameter_model. Just using defaults for now."
        )
        return session_processing_parameter_model

    def _create_new_skip_this_step_parameter(self):
        parameter = Parameter.create(
            name="Skip this step?",
            type="bool",
            value=False,
            tip="If you have already run this step, you can skip it." "re-running it will overwrite the existing data.",
        )
        parameter.sigValueChanged.connect(self.disable_this_parameter_group)

        return parameter

    def disable_this_parameter_group(self, parameter, changes):
        logger.debug(f"TODO - disable parameter group when 'skip this step?' is checked")
        pass
        # skip_this_step_bool = parameter.value()
        # parameter_group = parameter.parent()
        # for child in parameter_group.children():
        #     if child.name() != "Skip this step?":
        #         logger.debug(f"Disabling {child.name()}")
        #         child.setOpts(enabled=not skip_this_step_bool)

    def _launch_process_motion_capture_data_thread_worker(self):
        logger.debug("Launching process motion capture data process")
        session_parameter_model = self._extract_session_parameter_model_from_parameter_tree()
        session_parameter_model.recording_info_model = self._get_active_recording_info()

        if session_parameter_model.recording_info_model is None:
            logger.error("No active recording selected.")
            return
        if not Path(session_parameter_model.recording_info_model.path).exists():
            logger.error(f"Recording path does not exist: {session_parameter_model.recording_info_model.path}.")
            return

        self._process_motion_capture_data_thread_worker = ProcessMotionCaptureDataThreadWorker(session_parameter_model)
        self._process_motion_capture_data_thread_worker.start()

        self._process_motion_capture_data_thread_worker.finished.connect(self._handle_finished_signal)

    @pyqtSlot()
    def _handle_finished_signal(self):
        logger.debug("Process motion capture data process finished.")
        self.processing_finished_signal.emit()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ProcessMotionCaptureDataPanel()
    window.show()
    app.exec()
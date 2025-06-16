import sys
import os
import subprocess
import sounddevice as sd
import soundfile as sf
import matplotlib
matplotlib.use("QtAgg")
from PySide6.QtWidgets import (
    QSizePolicy,
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit,
    QTabWidget, QMessageBox, QTextEdit, QCheckBox, QSlider, QDialog
)
from PySide6.QtGui import QShortcut, QKeySequence
from constants import FORMAT_PRESETS, SPEAKER_NAMES
import datetime

class ImpulciferGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Impulcifer GUI")
        self.resize(700, 700)

        self.channel_mappings = {}
        
        # Default speaker layout
        self.selected_layout_name = next(iter(FORMAT_PRESETS))
        self.selected_layout = [SPEAKER_NAMES[i] for i in FORMAT_PRESETS[self.selected_layout_name]]


        self.tabs = QTabWidget()
        self.tab_order = []
        self.setCentralWidget(self.tabs)

                # self.create_headphone_eq_tab() called only once
        # Temporarily defer Setup tab creation
        # self.create_measurement_setup_tab()
        self.create_processing_options_tab()
        self.create_compensation_tab()
        self.create_room_response_tab()
        self.create_headphone_eq_tab()
        self.create_execution_tab()
        self.create_visualization_tab()
        self.create_measurement_setup_tab()  # Add Setup tab last
        self.setup_shortcuts()

    def create_measurement_setup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(QLabel("""
        In this tab, configure the test signal, measurement directory, and select
        playback and recording devices used for capturing impulse responses.
        """))
                                                                
        
        
        
        
        
        
        
        
        

        self.test_signal_path_var = QLineEdit()
        self.test_signal_path_var.setMaximumWidth(300)
        
        self.test_signal_path_var.setPlaceholderText("e.g., /path/to/test_signal.wav")
        browse_test = QPushButton("Browse")
        browse_test.setMaximumWidth(100)
        
        browse_test.clicked.connect(self.browse_test_signal)
        layout.addLayout(self.labeled_row("Select Test Signal File:", self.test_signal_path_var, browse_test))

        self.measurement_dir_var = QLineEdit()
        self.measurement_dir_var.setMaximumWidth(300)
        self.measurement_dir_var.setPlaceholderText("e.g., /path/to/measurements/")
        browse_dir = QPushButton("Browse")
        browse_dir.setMaximumWidth(100)
        browse_dir.clicked.connect(self.browse_measurement_dir)
        layout.addLayout(self.labeled_row("Select Measurement Directory:", self.measurement_dir_var, browse_dir))
        
        # Layout selection
        self.layout_var = QComboBox()
        self.layout_var.addItems(FORMAT_PRESETS.keys())
        self.layout_var.addItem("Custom...")
        self.layout_var.setCurrentText(self.selected_layout_name)
        self.layout_var.currentTextChanged.connect(self.handle_layout_change)
        layout.addLayout(self.labeled_row("Speaker Layout:", self.layout_var))

        self.playback_device_var = QComboBox()
        self.playback_device_var.setMaximumWidth(200)
        
        self.recording_device_var = QComboBox()
        self.recording_device_var.setMaximumWidth(200)
        self.load_device_options()

        layout.addLayout(self.labeled_row("Playback Device:", self.playback_device_var))
        layout.addLayout(self.labeled_row("Recording Device:", self.recording_device_var))

        map_btn = QPushButton("Map Channels")
        map_btn.clicked.connect(self.map_channels)
        layout.addWidget(map_btn)

                # Validation button
        self.test_signal_path_var.textChanged.connect(self.validate_measurement_setup)
        self.measurement_dir_var.textChanged.connect(self.validate_measurement_setup)

        self.tabs.addTab(tab, "Setup")

    def validate_measurement_setup(self):
        test_signal = self.test_signal_path_var.text()
        measurement_dir = self.measurement_dir_var.text()
        errors = []

        # Reset styles
        self.test_signal_path_var.setStyleSheet("")
        self.measurement_dir_var.setStyleSheet("")

        if not os.path.isfile(test_signal):
            self.test_signal_path_var.setStyleSheet("border: 2px solid red;")
            errors.append("Test signal file path is invalid or does not exist. ")
        else:
            self.test_signal_path_var.setStyleSheet("border: 2px solid green;")

        if not os.path.isdir(measurement_dir):
            self.measurement_dir_var.setStyleSheet("border: 2px solid red;")
            errors.append("Measurement directory path is invalid or does not exist.")
        else:
            self.measurement_dir_var.setStyleSheet("border: 2px solid green;")

        if errors:
            QMessageBox.critical(self, "Validation Failed", "".join(errors))
        else:
            QMessageBox.information(self, "Validation Passed", "All paths are valid.")

    def create_compensation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        summary = QLabel("""
        This tab allows you to configure compensation settings that correct headphone coloration
        and apply pre-measured or theoretical frequency response adjustments. Useful for ensuring
        consistent playback across different headphone types or compensation targets.
        """)
        summary.setWordWrap(True)
        summary.setSizePolicy(summary.sizePolicy().horizontalPolicy(), QSizePolicy.Minimum)
        layout.addWidget(summary)
        # Compensation Tab: Apply headphone and response compensation
        
        self.enable_compensation_var = QCheckBox("Enable Compensation")
        layout.addWidget(self.enable_compensation_var)

        self.compensation_type_var = QComboBox()
        self.compensation_type_var.addItems(["Diffuse-field", "Free-field", "Custom"])
        self.compensation_type_var.currentTextChanged.connect(self.update_compensation_file_state)
        layout.addLayout(self.labeled_row("Compensation Type:", self.compensation_type_var))

        self.compensation_file_path_var = QLineEdit()
        browse_comp = QPushButton("Browse")
        browse_comp.clicked.connect(self.browse_compensation_file)
        self.compensation_file_path_var = QLineEdit()
        self.compensation_custom_widget = QWidget()
        custom_layout = QHBoxLayout(self.compensation_custom_widget)
        custom_layout.addWidget(QLabel("Custom Compensation File:"))
        custom_layout.addWidget(self.compensation_file_path_var)
        custom_layout.addWidget(browse_comp)
        layout.addWidget(self.compensation_custom_widget)
        self.update_compensation_file_state()

        self.headphone_eq_toggle = QCheckBox("Enable Headphone EQ")
        layout.addWidget(self.headphone_eq_toggle)

        self.headphone_file_path_var = QLineEdit()
        self.headphone_file_path_var.setPlaceholderText("e.g., /path/to/headphones.wav")
        browse_hp = QPushButton("Browse")
        browse_hp.clicked.connect(self.browse_headphone_file)
        layout.addLayout(self.labeled_row("Headphone EQ File (headphones.wav):", self.headphone_file_path_var, browse_hp))

        self.tabs.addTab(tab, "Compensation")

    def create_room_response_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(QLabel("""
        Record a room response for use with room correction processing. This requires a calibrated microphone and the same test signal used for IR capture.
        """))

        steps = QLabel("""
        Steps:
        1. Position your calibrated microphone at the Main Listening Position.
        2. Ensure the test signal and measurement directory are set correctly.
        3. Click below to record the room response.
        """)
        steps.setWordWrap(True)
        layout.addWidget(steps)

        note = QLabel("""
        Note: If you have a microphone calibration file, it will be applied during the processing step,
        not during this recording. You can specify it in the Processing Options tab.
        """)
        note.setWordWrap(True)
        layout.addWidget(note)

        self.room_response_button = QPushButton("Record Room Response")
        self.room_response_button.setMaximumWidth(200)
        self.room_response_button.clicked.connect(self.launch_room_response_recorder)
        centered_button_layout = QHBoxLayout()
        centered_button_layout.addStretch()
        centered_button_layout.addWidget(self.room_response_button)
        centered_button_layout.addStretch()
        layout.addLayout(centered_button_layout)

        self.tabs.insertTab(1, tab, "Room Response")

    def create_headphone_eq_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(QLabel("""
        Headphone EQ allows you to capture the frequency response of your headphones
        using a binaural microphone setup. This is optional but recommended for
        more accurate BRIR processing.
        """))
        
        steps = QLabel("""
        Steps:
        1. Insert your binaural microphones.
        2. Wear your headphones.
        3. Play the test signal and record using the button below.
        """)
        steps.setWordWrap(True)
        layout.addWidget(steps)

        self.hp_recorder_button2 = QPushButton("Record Headphone EQ")
        self.hp_recorder_button2.setMaximumWidth(200)
        self.hp_recorder_button2.clicked.connect(self.launch_headphone_recorder)
        centered_button_layout = QHBoxLayout()
        centered_button_layout.addStretch()
        centered_button_layout.addWidget(self.hp_recorder_button2)
        centered_button_layout.addStretch()
        layout.addLayout(centered_button_layout)

        self.tabs.insertTab(0, tab, "Headphone EQ")

    def create_execution_tab(self):
        # Create Execution tab first and bring it to focus
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(QLabel("""
        Use this tab to launch the recorder or run the processing pipeline.
        Review logs, clear or save output, and troubleshoot from here.
        """))
        # Execution Tab: Run processing and launch recorders
        
        self.run_button = QPushButton("Run Processing")
        self.run_button.clicked.connect(self.run_processing)
        layout.addWidget(self.run_button)

        self.recorder_button = QPushButton("Launch Recorder")
        self.recorder_button.clicked.connect(self.launch_recorder)
        layout.addWidget(self.recorder_button)

        self.hp_recorder_button = QPushButton("Record Headphone EQ")
        self.hp_recorder_button.clicked.connect(self.launch_headphone_recorder)
        # Removed from Execution tab to move into Headphone EQ tab

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        log_controls = QHBoxLayout()
        clear_log_btn = QPushButton("Clear Log")
        save_log_btn = QPushButton("Save Log")
        clear_log_btn.clicked.connect(lambda: self.output_text.clear())
        save_log_btn.clicked.connect(self.save_log)
        log_controls.addWidget(clear_log_btn)
        log_controls.addWidget(save_log_btn)
        layout.addLayout(log_controls)
        layout.addWidget(self.output_text)

        self.tabs.addTab(tab, "Execution")
        self.tabs.setTabText(self.tabs.indexOf(tab), "★ Execution")
        self.tabs.setCurrentWidget(tab)

    def run_processing(self):
        if not os.path.isdir(self.measurement_dir_var.text()):
            QMessageBox.critical(self, "Error", "Please ensure the measurement directory is valid before processing.")
            return

        args = [
            sys.executable, "impulcifer.py",
            "--dir_path", self.measurement_dir_var.text()
        ]

        if self.test_signal_path_var.text():
            args.extend(["--input", self.test_signal_path_var.text()])
        if self.decay_time_var.text():
            args.extend(["--decay", self.decay_time_var.text()])
        if self.target_level_var.text():
            args.extend(["--target_level", self.target_level_var.text()])
        if self.channel_balance_toggle.isChecked():
            args.extend(["--channel_balance", self.channel_balance_var.currentData()])
        if self.specific_limit_toggle.isChecked() and self.specific_limit_var.text():
            args.extend(["--specific_limit", self.specific_limit_var.text()])
        if self.generic_limit_toggle.isChecked() and self.generic_limit_var.text():
            args.extend(["--generic_limit", self.generic_limit_var.text()])
        if self.fr_combination_toggle.isChecked():
            args.extend(["--fr_combination_method", self.fr_combination_var.currentText()])
        if self.room_correction_var.isChecked():
            args.extend(["--room_target", self.room_target_path_var.text()])
            mic_file = self.mic_calibration_path_var.text()
            if mic_file:
                if not os.path.isfile(mic_file):
                    QMessageBox.critical(self, "Error", "Mic calibration file does not exist or is unreadable.")
                    return
                args.extend(["--room_mic_calibration", mic_file])
                args.extend(["--room_mic_calibration", self.mic_calibration_path_var.text()])
        if self.enable_compensation_var.isChecked():
            args.append("--compensation")
            if self.headphone_eq_toggle.isChecked() and self.headphone_file_path_var.text():
                args.extend(["--headphones", self.headphone_file_path_var.text()])
            if not self.headphone_eq_toggle.isChecked():
                args.append("--no_headphone_compensation")
            if self.compensation_type_var.currentText().lower() == "custom":
                args.append(self.compensation_file_path_var.text())
            else:
                args.append(self.compensation_type_var.currentText().lower().replace("-field", ""))

        try:
            self.output_text.append(f"Running: {' '.join(args)}")
            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.output_text.append("<span style='color: green;'>" + result.stdout + "</span>")
            if result.stderr:
                self.output_text.append("<span style='color: red;'>" + result.stderr + "</span>")
            return
            
        except Exception as e:
            self.output_text.append(f"Error: {str(e)}")

    def launch_room_response_recorder(self):
        if not os.path.isfile(self.test_signal_path_var.text()) or not os.path.isdir(self.measurement_dir_var.text()):
            QMessageBox.critical(self, "Error", "Please ensure the test signal and measurement directory are valid before recording.")
            return
        try:
            output_channels = ','.join(map(str, self.channel_mappings.get("output_channels", [])))
            input_channels = ','.join(map(str, self.channel_mappings.get("input_channels", [])))
            playback_idx = self.playback_device_var.currentText().split(':')[0]
            record_idx = self.recording_device_var.currentText().split(':')[0]

            args = [
                sys.executable, "recorder.py",
                "--output_channels", output_channels,
                "--input_channels", input_channels,
                "--playback_device", playback_idx,
                "--recording_device", record_idx,
                "--output_dir", self.measurement_dir_var.text(),
                "--test_signal", self.test_signal_path_var.text(),
                "--output_file", os.path.join(self.measurement_dir_var.text(), "room.wav")
            ]

            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.output_text.append("<span style='color: green;'>" + result.stdout + "</span>")
            if result.stderr:
                self.output_text.append("<span style='color: red;'>" + result.stderr + "</span>")
        except Exception as e:
            QMessageBox.critical(self, "Room Response Recorder Error", str(e))


    def launch_headphone_recorder(self):
        if not os.path.isfile(self.test_signal_path_var.text()) or not os.path.isdir(self.measurement_dir_var.text()):
            QMessageBox.critical(self, "Error", "Please ensure the test signal and measurement directory are valid before recording.")
            return
        try:
            output_channels = ','.join(map(str, self.channel_mappings.get("output_channels", [])))
            input_channels = ','.join(map(str, self.channel_mappings.get("input_channels", [])))
            playback_idx = self.playback_device_var.currentText().split(':')[0]
            record_idx = self.recording_device_var.currentText().split(':')[0]

            args = [
                sys.executable, "recorder.py",
                "--output_channels", output_channels,
                "--input_channels", input_channels,
                "--playback_device", playback_idx,
                "--recording_device", record_idx,
                "--output_dir", self.measurement_dir_var.text(),
                "--test_signal", self.test_signal_path_var.text(),
                "--output_file", os.path.join(self.measurement_dir_var.text(), "headphones.wav")
            ]

            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.output_text.append("<span style='color: green;'>" + result.stdout + "</span>")
            if result.stderr:
                self.output_text.append("<span style='color: red;'>" + result.stderr + "</span>")
        except Exception as e:
            QMessageBox.critical(self, "Headphone Recorder Error", str(e))


    def launch_recorder(self):
        if not os.path.isfile(self.test_signal_path_var.text()) or not os.path.isdir(self.measurement_dir_var.text()):
            QMessageBox.critical(self, "Error", "Please ensure the test signal and measurement directory are valid before recording.")
            return
        try:
            output_channels = ','.join(map(str, self.channel_mappings.get("output_channels", [])))
            input_channels = ','.join(map(str, self.channel_mappings.get("input_channels", [])))
            playback_idx = self.playback_device_var.currentText().split(':')[0]
            record_idx = self.recording_device_var.currentText().split(':')[0]

            args = [
                sys.executable, "recorder.py",
                "--output_channels", output_channels,
                "--input_channels", input_channels,
                "--playback_device", playback_idx,
                "--recording_device", record_idx,
                "--output_dir", self.measurement_dir_var.text(),
                "--test_signal", self.test_signal_path_var.text()
            ]

            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.output_text.append("<span style='color: green;'>" + result.stdout + "</span>")
            if result.stderr:
                self.output_text.append("<span style='color: red;'>" + result.stderr + "</span>")
            
        except Exception as e:
            QMessageBox.critical(self, "Recorder Error", str(e))

    def update_compensation_file_state(self):
        is_custom = self.compensation_type_var.currentText().lower() == "custom"
        self.compensation_custom_widget.setVisible(is_custom)
        self.compensation_file_path_var.setEnabled(is_custom)

    def browse_headphone_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Headphone EQ File", "", "Wave Files (*.wav);;All Files (*)")
        if file_path:
            self.headphone_file_path_var.setText(file_path)

    def browse_compensation_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Compensation File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.compensation_file_path_var.setText(file_path)


    def create_processing_options_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        summary = QLabel("""
        This tab lets you control how the impulse responses are interpreted and shaped,
        including decay filtering, loudness matching, balance, and room correction parameters.
        """)
        summary.setWordWrap(True)
        summary.setSizePolicy(summary.sizePolicy().horizontalPolicy(), QSizePolicy.Minimum)
        layout.addWidget(summary)
        # Processing Options Tab: Fine-tune BRIR processing parameters
        
        self.decay_time_var = QLineEdit()
        self.decay_time_var.setPlaceholderText("Recommended: 0.2")
        self.decay_time_toggle = QCheckBox("Enable")
        self.decay_time_toggle.setChecked(False)
        self.decay_time_var.setPlaceholderText("e.g., 0.2")
        self.decay_time_var.clear()
        layout.addLayout(self.labeled_row("Decay Time (seconds):", self.decay_time_var, self.decay_time_toggle))

        self.target_level_var = QLineEdit()
        self.target_level_var.setPlaceholderText("Recommended: -12.5")
        self.target_level_toggle = QCheckBox("Enable")
        self.target_level_toggle.setChecked(False)
        self.target_level_var.setPlaceholderText("e.g., -12.5")
        self.target_level_var.clear()
        layout.addLayout(self.labeled_row("Target Level (dB):", self.target_level_var, self.target_level_toggle))

        self.channel_balance_var = QComboBox()
        self.channel_balance_var.addItem("Off", "off")
        self.channel_balance_var.addItem("Left", "left")
        self.channel_balance_var.addItem("Right", "right")
        self.channel_balance_var.addItem("Average", "avg")
        self.channel_balance_var.addItem("Minimum", "min")
        self.channel_balance_var.addItem("Mids", "mids")
        self.channel_balance_var.addItem("Trend", "trend")
        # Default strategy
        idx = self.channel_balance_var.findData("trend")
        if idx != -1:
            self.channel_balance_var.setCurrentIndex(idx)
        self.channel_balance_toggle = QCheckBox("Enable")
        self.channel_balance_toggle.setChecked(False)
        balance_row = QHBoxLayout()
        balance_row.addWidget(QLabel("Channel Balance:"))
        balance_row.addWidget(self.channel_balance_var)
        balance_row.addWidget(self.channel_balance_toggle)
        self.channel_balance_preview = QPushButton("Preview…")
        self.channel_balance_preview.clicked.connect(self.open_channel_balance_preview)
        balance_row.addWidget(self.channel_balance_preview)
        layout.addLayout(balance_row)

        self.room_correction_var = QCheckBox("Enable Room Correction")
        self.room_correction_var.stateChanged.connect(self.update_room_correction_fields)
        layout.addWidget(self.room_correction_var)

        self.room_target_path_var = QLineEdit()
        self.room_target_path_row = QWidget()
        row_layout = QHBoxLayout(self.room_target_path_row)
        row_layout.addWidget(QLabel("Room Target File (optional):"))
        row_layout.addWidget(self.room_target_path_var)
        row_layout.addWidget(QPushButton("Browse", clicked=self.browse_room_target))
        layout.addWidget(self.room_target_path_row)
        browse_room_target = QPushButton("Browse")
        browse_room_target.clicked.connect(self.browse_room_target)
        

        self.specific_limit_var = QLineEdit()
        self.specific_limit_var.setPlaceholderText("e.g., 700")
        self.specific_limit_toggle = QCheckBox("Enable")
        

        self.generic_limit_var = QLineEdit()
        self.generic_limit_var.setPlaceholderText("e.g., 500")
        self.generic_limit_toggle = QCheckBox("Enable")
        

        self.fr_combination_var = QComboBox()
        self.fr_combination_var.addItems(["average", "conservative"])
        self.fr_combination_toggle = QCheckBox("Enable")
        

        self.specific_limit_row_widget = QWidget()
        self.specific_limit_row = self.labeled_row("Specific Limit (Hz):", self.specific_limit_var, self.specific_limit_toggle)
        self.specific_limit_row_widget.setLayout(self.specific_limit_row)
        self.generic_limit_row_widget = QWidget()
        self.generic_limit_row = self.labeled_row("Generic Limit (Hz):", self.generic_limit_var, self.generic_limit_toggle)
        self.generic_limit_row_widget.setLayout(self.generic_limit_row)
        self.fr_combination_row_widget = QWidget()

        self.mic_calibration_path_var = QLineEdit()
        self.mic_calibration_path_var.setPlaceholderText("Optional microphone calibration file")
        mic_calib_browse = QPushButton("Browse")
        mic_calib_browse.clicked.connect(self.browse_mic_calibration_file)
        layout.addLayout(self.labeled_row("Mic Calibration File:", self.mic_calibration_path_var, mic_calib_browse))
        self.fr_combination_row = self.labeled_row("FR Combination Method:", self.fr_combination_var, self.fr_combination_toggle)
        self.fr_combination_row_widget.setLayout(self.fr_combination_row)

        layout.addWidget(self.specific_limit_row_widget)
        layout.addWidget(self.generic_limit_row_widget)
        layout.addWidget(self.fr_combination_row_widget)

        self.update_room_correction_fields()
        self.tabs.addTab(tab, "Processing Options")

    def update_room_correction_fields(self):
        is_enabled = self.room_correction_var.isChecked()
        self.room_target_path_row.setVisible(is_enabled)
        self.specific_limit_row_widget.setVisible(is_enabled)
        self.generic_limit_row_widget.setVisible(is_enabled)
        self.fr_combination_row_widget.setVisible(is_enabled)

    def browse_mic_calibration_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Mic Calibration File", "", "Text Files (*.txt *.csv);;All Files (*)")
        if file_path:
            self.mic_calibration_path_var.setText(file_path)

    def browse_room_target(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Room Target File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.room_target_path_var.setText(file_path)

    def labeled_row(self, label_text, widget, extra_widget=None):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        row.addWidget(widget)
        if extra_widget:
            row.addWidget(extra_widget)
        return row

    def load_device_options(self):
        devices = sd.query_devices()
        self.playback_devices = [f"{i}: {d['name']}" for i, d in enumerate(devices) if d['max_output_channels'] > 0]
        self.recording_devices = [f"{i}: {d['name']}" for i, d in enumerate(devices) if d['max_input_channels'] > 0]

        self.playback_device_var.addItems(self.playback_devices)
        self.recording_device_var.addItems(self.recording_devices)

        if sd.default.device:
            if sd.default.device[1] < len(self.playback_devices):
                self.playback_device_var.setCurrentIndex(sd.default.device[1])
            if sd.default.device[0] < len(self.recording_devices):
                self.recording_device_var.setCurrentIndex(sd.default.device[0])

    def browse_test_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Test Signal File", "", "Wave Files (*.wav);;Pickle Files (*.pkl);;All Files (*)")
        if file_path:
            self.test_signal_path_var.setText(file_path)

    def browse_measurement_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Measurement Directory")
        if dir_path:
            self.measurement_dir_var.setText(dir_path)

    def handle_layout_change(self, text):
        if text == "Custom...":
            self.load_custom_layout()
            return
        self.selected_layout_name = text
        self.selected_layout = [SPEAKER_NAMES[i] for i in FORMAT_PRESETS[text]]

    def load_custom_layout(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Layout File", "", "Text or JSON (*.txt *.json);;All Files (*)")
        if not file_path:
            # Revert to previous selection
            self.layout_var.setCurrentText(self.selected_layout_name)
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            try:
                import json
                names = json.loads(content)
                if isinstance(names, dict):
                    names = names.get("speakers", [])
            except json.JSONDecodeError:
                names = [n.strip() for n in content.split(',') if n.strip()]
            if not names:
                raise ValueError("No speakers defined in layout file")
            self.selected_layout_name = os.path.basename(file_path)
            self.selected_layout = names
            if self.layout_var.findText(self.selected_layout_name) == -1:
                self.layout_var.addItem(self.selected_layout_name)
            self.layout_var.setCurrentText(self.selected_layout_name)
        except Exception as e:
            QMessageBox.critical(self, "Layout Load Error", str(e))
            self.layout_var.setCurrentText(self.selected_layout_name)

    def map_channels(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout

        dialog = QDialog(self)
        dialog.setWindowTitle("Channel Mapping")

        main_layout = QHBoxLayout()

        playback_idx = int(self.playback_device_var.currentText().split(':')[0])
        record_idx = int(self.recording_device_var.currentText().split(':')[0])

        playback_channels = sd.query_devices(playback_idx)['max_output_channels']
        record_channels = sd.query_devices(record_idx)['max_input_channels']

        speaker_labels = self.selected_layout
        mic_labels = ["Mic Left", "Mic Right"]

        self.speaker_channel_vars = []
        self.mic_channel_vars = []

        # Speaker layout
        speaker_layout = QFormLayout()
        speaker_layout.addRow(QLabel(f"Speaker Channels ({self.selected_layout_name})"))
        for i, label in enumerate(speaker_labels):
            box = QComboBox()
            box.addItems([str(x + 1) for x in range(playback_channels)])
            box.setCurrentIndex(i if i < playback_channels else 0)
            self.speaker_channel_vars.append(box)
            speaker_layout.addRow(label, box)

        # Mic layout
        mic_layout = QFormLayout()
        mic_layout.addRow(QLabel("Microphone Channels (Recording)"))
        for j, label in enumerate(mic_labels):
            box = QComboBox()
            box.addItems([str(x + 1) for x in range(record_channels)])
            box.setCurrentIndex(j if j < record_channels else 0)
            self.mic_channel_vars.append(box)
            mic_layout.addRow(label, box)

        main_layout.addLayout(speaker_layout)
        main_layout.addLayout(mic_layout)

        bottom_layout = QVBoxLayout()
        save_btn = QPushButton("Save Mappings")
        save_btn.clicked.connect(lambda: self.save_channel_mappings(dialog))
        bottom_layout.addLayout(main_layout)
        bottom_layout.addWidget(save_btn)

        dialog.setLayout(bottom_layout)
        dialog.exec()

    def create_visualization_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(QLabel("""
        View example plots or visualizations of processed frequency responses to
        help verify measurement accuracy and processing behavior.
        """))
        # Visualization Tab: View frequency response plots
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure

        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_button = QPushButton("Plot Example")
        self.plot_button.clicked.connect(self.plot_example)
        layout.addWidget(self.plot_button)

        self.tabs.addTab(tab, "Visualization")



        
    def save_log(self):
        try:
            content = self.output_text.toPlainText()
            default_name = f"impulcifer_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Log", default_name, "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(content)
                QMessageBox.information(self, "Log Saved", f"Log saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Log Error", str(e))

    def plot_example(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot([0, 1, 2, 3], [10, 1, 20, 3])
        ax.set_title("Example Plot")
        self.canvas.draw()



    def save_channel_mappings(self, dialog):
        speakers = [int(box.currentText()) - 1 for box in self.speaker_channel_vars]
        mics = [int(box.currentText()) - 1 for box in self.mic_channel_vars]
        self.channel_mappings = {
            "output_channels": speakers,
            "input_channels": mics
        }
        QMessageBox.information(self, "Channel Mappings", "Channel mappings saved successfully.")
        dialog.accept()

    def open_channel_balance_preview(self):
        from PySide6.QtCore import Qt

        dialog = QDialog(self)
        dialog.setWindowTitle("Channel Balance Preview")

        main_layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Audio File:"))
        file_var = QLineEdit()
        file_layout.addWidget(file_var)
        browse_btn = QPushButton("Browse")
        file_layout.addWidget(browse_btn)
        main_layout.addLayout(file_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Right Gain:"))
        slider = QSlider(Qt.Horizontal)
        slider.setRange(-100, 100)
        slider.setValue(0)
        slider_layout.addWidget(slider)
        gain_label = QLabel("0.0 dB")
        slider_layout.addWidget(gain_label)
        main_layout.addLayout(slider_layout)

        button_layout = QHBoxLayout()
        play_btn = QPushButton("Play")
        stop_btn = QPushButton("Stop")
        apply_btn = QPushButton("Apply")
        close_btn = QPushButton("Close")
        button_layout.addWidget(play_btn)
        button_layout.addWidget(stop_btn)
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        main_layout.addLayout(button_layout)

        def update_label(value):
            gain_label.setText(f"{value/10:.1f} dB")

        slider.valueChanged.connect(update_label)

        def browse_file():
            file_path, _ = QFileDialog.getOpenFileName(dialog, "Select Audio File", "", "Wave Files (*.wav);;All Files (*)")
            if file_path:
                file_var.setText(file_path)

        browse_btn.clicked.connect(browse_file)

        def play():
            if not os.path.isfile(file_var.text()):
                QMessageBox.critical(dialog, "Error", "Please select a valid audio file.")
                return
            data, fs = sf.read(file_var.text(), always_2d=True)
            if data.shape[1] < 2:
                QMessageBox.critical(dialog, "Error", "Audio file must be stereo.")
                return
            gain = 10 ** ((slider.value() / 10) / 20)
            data[:, 1] *= gain
            sd.stop()
            sd.play(data, fs)

        play_btn.clicked.connect(play)
        stop_btn.clicked.connect(sd.stop)

        def apply():
            gain_db = slider.value() / 10
            cli_val = f"{gain_db:.1f}"
            label = f"{cli_val} dB"
            # Find existing entry with same data
            index = self.channel_balance_var.findData(cli_val)
            if index == -1:
                self.channel_balance_var.addItem(label, cli_val)
                index = self.channel_balance_var.count() - 1
            self.channel_balance_var.setCurrentIndex(index)
            self.channel_balance_toggle.setChecked(True)
            sd.stop()
            dialog.accept()

        apply_btn.clicked.connect(apply)

        def close_dialog():
            sd.stop()
            dialog.close()

        close_btn.clicked.connect(close_dialog)

        dialog.setLayout(main_layout)
        dialog.exec()

    
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Meta+1"), self, activated=lambda: self.tabs.setCurrentIndex(
            self.tabs.indexOf(self.tabs.widget(0))  # Assumes Execution tab is at index 0
        ))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImpulciferGUI()
    window.show()
    sys.exit(app.exec())

#if canImport(SwiftUI)
import SwiftUI

struct EarprintApp: App {
    @State private var measurementDir: String = ""
    @State private var testSignal: String = ""
    @State private var channelBalance: String = ""
    @State private var targetLevel: String = ""
    @State private var selectedLayout: String = "7.1"
    @State private var playbackDevice: String = ""
    @State private var recordingDevice: String = ""
    @State private var channelMapping: [String: [Int]] = [:]
    @StateObject private var processingVM = ProcessingViewModel()

    var body: some Scene {
        WindowGroup {
            TabView {
                SetupView(viewModel: processingVM,
                          measurementDir: $measurementDir,
                          testSignal: $testSignal,
                          channelBalance: $channelBalance,
                          targetLevel: $targetLevel,
                          selectedLayout: $selectedLayout,
                          playbackDevice: $playbackDevice,
                          recordingDevice: $recording_device,
                          channelMapping: $channelMapping)
                    .tabItem { Text("Setup") }
                ExecutionView(viewModel: processingVM,
                              measurementDir: measurementDir,
                              testSignal: testSignal,
                              channelBalance: channelBalance,
                              targetLevel: targetLevel,
                              playbackDevice: playbackDevice,
                              recordingDevice: recordingDevice,
                              outputChannels: channelMapping["output_channels"] ?? [],
                              inputChannels: channelMapping["input_channels"] ?? [])
                              selectedLayout: selectedLayout)
                    .tabItem { Text("Execution") }
                HeadphoneEQView(viewModel: processingVM,
                                measurementDir: measurementDir,
                                testSignal: testSignal,
                                playbackDevice: playbackDevice,
                                recordingDevice: recordingDevice)
                    .tabItem { Text("Headphone EQ") }
                RoomResponseView(viewModel: processingVM,
                                 measurementDir: measurementDir,
                                 testSignal: testSignal,
                                 playbackDevice: playbackDevice,
                                 recordingDevice: recordingDevice)
                    .tabItem { Text("Room Response") }
                ProcessingOptionsView(channelBalance: $channelBalance,
                                     targetLevel: $targetLevel)
                    .tabItem { Text("Processing Options") }
                CompensationView(viewModel: processingVM)
                    .tabItem { Text("Compensation") }
                PresetView(viewModel: processingVM,
                           measurementDir: measurementDir)
                    .tabItem { Text("Presets") }
                ProfileView(viewModel: processingVM,
                            measurementDir: measurementDir)
                    .tabItem { Text("Profiles") }
                VisualizationView(measurementDir: measurementDir)
                    .tabItem { Text("Visualization") }
            }
            .frame(minWidth: 600, minHeight: 400)
        }
    }
}
#endif
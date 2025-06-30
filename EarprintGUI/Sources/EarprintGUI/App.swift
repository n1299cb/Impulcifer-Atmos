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
    @State private var enableCompensation: Bool = false
    @State private var headphoneEqEnabled: Bool = false
    @State private var headphoneFile: String = ""
    @State private var compensationType: String = "diffuse"
    @State private var customCompensationFile: String = ""
    @State private var diffuseField: Bool = false
    @State private var xCurveAction: String = "None"
    @State private var xCurveType: String = "minus3db_oct"
    @State private var xCurveInCapture: Bool = false
    @StateObject private var processingVM = ProcessingViewModel()
    @State private var selectedTab: Int = 0

    var body: some Scene {
        WindowGroup {
            TabView(selection: $selectedTab) {
                SetupView(viewModel: processingVM,
                          measurementDir: $measurementDir,
                          testSignal: $testSignal,
                          channelBalance: $channelBalance,
                          targetLevel: $targetLevel,
                          selectedLayout: $selectedLayout,
                          playbackDevice: $playbackDevice,
                          recordingDevice: $recordingDevice,
                          channelMapping: $channelMapping)
                    .tabItem { Text("Setup") }
                    .tag(0)
                ExecutionView(viewModel: processingVM,
                              measurementDir: measurementDir,
                              testSignal: testSignal,
                              channelBalance: channelBalance,
                              targetLevel: targetLevel,
                              playbackDevice: playbackDevice,
                              recordingDevice: recordingDevice,
                              outputChannels: channelMapping["output_channels"] ?? [],
                              inputChannels: channelMapping["input_channels"] ?? [],
                              selectedLayout: selectedLayout,
                              enableCompensation: $enableCompensation,
                              headphoneEqEnabled: $headphoneEqEnabled,
                              headphoneFile: $headphoneFile,
                              compensationType: $compensationType,
                              customCompensationFile: $customCompensationFile,
                              diffuseField: $diffuseField,
                              xCurveAction: $xCurveAction,
                              xCurveType: $xCurveType,
                              xCurveInCapture: $xCurveInCapture)
                    .tabItem { Text("Execution") }
                    .tag(1)
                HeadphoneEQView(viewModel: processingVM,
                                measurementDir: measurementDir,
                                testSignal: testSignal,
                                playbackDevice: playbackDevice,
                                recordingDevice: recordingDevice)
                    .tabItem { Text("Headphone EQ") }
                    .tag(2)
                RoomResponseView(viewModel: processingVM,
                                 measurementDir: measurementDir,
                                 testSignal: testSignal,
                                 playbackDevice: playbackDevice,
                                 recordingDevice: recordingDevice)
                    .tabItem { Text("Room Response") }
                    .tag(3)
                ProcessingOptionsView(channelBalance: $channelBalance,
                                     targetLevel: $targetLevel)
                    .tabItem { Text("Processing Options") }
                    .tag(4)
                CompensationView(viewModel: processingVM,
                                 enableCompensation: $enableCompensation,
                                 headphoneEqEnabled: $headphoneEqEnabled,
                                 headphoneFile: $headphoneFile,
                                 compensationType: $compensationType,
                                 customCompensationFile: $customCompensationFile,
                                 diffuseField: $diffuseField,
                                 xCurveAction: $xCurveAction,
                                 xCurveType: $xCurveType,
                                 xCurveInCapture: $xCurveInCapture)
                    .tabItem { Text("Compensation") }
                    .tag(5)
                PresetView(viewModel: processingVM,
                           measurementDir: measurementDir)
                    .tabItem { Text("Presets") }
                    .tag(6)
                ProfileView(viewModel: processingVM,
                            measurementDir: measurementDir)
                    .tabItem { Text("Profiles") }
                    .tag(7)
                VisualizationView(measurementDir: measurementDir)
                    .tabItem { Text("Visualization") }
                    .tag(8)
            }
            .frame(minWidth: 600, minHeight: 400)
        }
        .commands {
            CommandMenu("Navigate") {
                Button("Setup") { selectedTab = 0 }
                    .keyboardShortcut("1", modifiers: .command)
                Button("Execution") { selectedTab = 1 }
                    .keyboardShortcut("2", modifiers: .command)
            }
        }
    }
}
#endif
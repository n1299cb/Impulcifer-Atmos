#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct ExecutionView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    var testSignal: String
    var channelBalance: String
    var targetLevel: String
    var playbackDevice: String
    var recordingDevice: String
    var outputChannels: [Int]
    var inputChannels: [Int]
    var selectedLayout: String = ""
    @Binding var enableCompensation: Bool
    @Binding var headphoneEqEnabled: Bool
    @Binding var headphoneFile: String
    @Binding var compensationType: String
    @Binding var customCompensationFile: String
    @Binding var diffuseField: Bool
    @Binding var xCurveAction: String
    @Binding var xCurveType: String
    @Binding var xCurveInCapture: Bool

    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Button(action: {
                    viewModel.run(
                        measurementDir: measurementDir,
                        testSignal: testSignal,
                        channelBalance: channelBalance,
                        targetLevel: targetLevel,
                        playbackDevice: playbackDevice,
                        recordingDevice: recordingDevice,
                        outputChannels: outputChannels,
                        inputChannels: inputChannels,
                        enableCompensation: enableCompensation,
                        headphoneEqEnabled: headphoneEqEnabled,
                        headphoneFile: headphoneFile,
                        compensationType: compensationType == "custom" ? customCompensationFile : compensationType,
                        diffuseField: diffuseField,
                        xCurveAction: xCurveAction,
                        xCurveType: xCurveType,
                        xCurveInCapture: xCurveInCapture
                    )
                }) {
                    Text(viewModel.isRunning ? "Running..." : "Run Processing")
                }
                .disabled(viewModel.isRunning || measurementDir.isEmpty || testSignal.isEmpty)

                Button("Cancel") { viewModel.cancel() }
                    .disabled(!viewModel.isRunning)
            
                Button("Clear Log") { viewModel.clearLog() }
                    .disabled(viewModel.log.isEmpty)

                Button("Save Log") {
                    if let url = savePanel(startPath: measurementDir) {
                        try? viewModel.log.write(to: url, atomically: true, encoding: .utf8)
                    }
                }
                .disabled(viewModel.log.isEmpty)
            }

            if viewModel.isRunning {
                if let progress = viewModel.progress {
                    ProgressView(value: progress)
                        .frame(maxWidth: .infinity)
                } else {
                    ProgressView()
                        .progressViewStyle(.linear)
                        .frame(maxWidth: .infinity)
                }
            }
                Button("Launch Recorder") {
                    viewModel.record(measurementDir: measurementDir,
                                     testSignal: testSignal,
                                     playbackDevice: playbackDevice,
                                     recordingDevice: recordingDevice,
                                     outputFile: nil)
                }
                Button("Capture Wizard") {
                    viewModel.captureWizard(layout: selectedLayout, dir: measurementDir)
                }
                Button("Export Hesuvi") {
                    if let dest = savePanel(startPath: measurementDir) {
                        viewModel.exportHesuviPreset(measurementDir: measurementDir, destination: dest)
                    }
                }
            ScrollView {
                Text(viewModel.log)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding()
    }

    func savePanel(startPath: String) -> URL? {
        #if canImport(AppKit)
        let panel = NSSavePanel()
        panel.directoryURL = URL(fileURLWithPath: startPath)
        return panel.runModal() == .OK ? panel.url : nil
        #else
        return nil
        #endif
    }
}
#endif
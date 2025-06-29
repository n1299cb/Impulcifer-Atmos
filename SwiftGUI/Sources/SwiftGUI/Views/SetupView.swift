#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct SetupView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    @Binding var measurementDir: String
    @Binding var testSignal: String
    @Binding var channelBalance: String
    @Binding var targetLevel: String
    @Binding var selectedLayout: String

    private let layouts = ["1.0", "2.0", "5.1", "5.1.2", "5.1.4", "7.1", "7.1.2", "7.1.4", "7.1.6", "9.1.4", "9.1.6", "ambisonics"].sorted()

    var body: some View {
        Form {
            HStack {
                TextField("Measurement directory", text: $measurementDir)
                Button("Browse") {
                    if let path = openPanel(directory: true) {
                        measurementDir = path
                    }
                }
            }
            HStack {
                TextField("Test signal", text: $testSignal)
                Button("Browse") {
                    if let path = openPanel(directory: false) {
                        testSignal = path
                    }
                }
            }
            Picker("Layout", selection: $selectedLayout) {
                ForEach(layouts, id: \.self) { Text($0) }
            }
            TextField("Channel Balance", text: $channelBalance)
            TextField("Target Level", text: $targetLevel)
            HStack {
                Button("Layout Wizard") {
                    viewModel.layoutWizard(layout: selectedLayout, dir: measurementDir)
                }
                Button("Capture Wizard") {
                    viewModel.captureWizard(layout: selectedLayout, dir: measurementDir)
                }
            }
        }
        .padding()
    }

    func openPanel(directory: Bool) -> String? {
        let panel = NSOpenPanel()
        panel.canChooseFiles = !directory
        panel.canChooseDirectories = directory
        panel.allowsMultipleSelection = false
        return panel.runModal() == .OK ? panel.url?.path : nil
    }
}
#endif
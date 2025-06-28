import SwiftUI
import AppKit

struct SetupView: View {
    @Binding var measurementDir: String
    @Binding var testSignal: String

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
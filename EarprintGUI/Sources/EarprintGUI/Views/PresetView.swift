#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct PresetView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    @State private var presets: [String] = []
    @State private var selected: String?

    var body: some View {
        VStack {
            HStack {
                Button("Refresh") { loadPresets() }
                Button("Load") { if let s = selected { loadPreset(name: s) } }
            }
            List(presets, id: \.self, selection: $selected) { Text($0) }
        }
        .onAppear { loadPresets() }
        .padding()
    }

    func loadPresets() {
        let dir = URL(fileURLWithPath: measurementDir).appendingPathComponent("presets")
        if let items = try? FileManager.default.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil) {
            presets = items.filter { $0.pathExtension == "json" }.map { $0.lastPathComponent }
        }
    }

    func loadPreset(name: String) {
        viewModel.log += "Loaded preset \(name)\n"
    }
}
#endif
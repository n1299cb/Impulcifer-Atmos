#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct ProfileView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    @State private var profiles: [String] = []
    @State private var selected: String?

    var body: some View {
        VStack {
            HStack {
                Button("Refresh") { loadProfiles() }
                Button("Load") { if let s = selected { loadProfile(name: s) } }
                Button("Save") { if let s = selected { saveProfile(name: s) } }
                Button("Delete") { if let s = selected { deleteProfile(name: s) } }
                Button("Import…") { importProfile() }
            }
            List(profiles, id: \.self, selection: $selected) { Text($0) }
        }
        .onAppear { loadProfiles() }
        .padding()
    }

    func loadProfiles() {
        let dir = URL(fileURLWithPath: measurementDir).appendingPathComponent("profiles")
        if let items = try? FileManager.default.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil) {
            profiles = items.filter { $0.pathExtension == "json" }.map { $0.lastPathComponent }
        }
    }

    func loadProfile(name: String) {
        viewModel.log += "Loaded profile \(name)\n"
    }

    func saveProfile(name: String) {
        let dir = URL(fileURLWithPath: measurementDir).appendingPathComponent("profiles")
        let src = dir.appendingPathComponent(name)
        if let url = savePanel(start: dir.path, name: name) {
            try? FileManager.default.copyItem(at: src, to: url)
            loadProfiles()
        }
    }

    func deleteProfile(name: String) {
        let file = URL(fileURLWithPath: measurementDir).appendingPathComponent("profiles").appendingPathComponent(name)
        try? FileManager.default.removeItem(at: file)
        loadProfiles()
    }

    func importProfile() {
        let dir = URL(fileURLWithPath: measurementDir).appendingPathComponent("profiles")
        if let url = openPanel(start: dir.path) {
            let dest = dir.appendingPathComponent(url.lastPathComponent)
            try? FileManager.default.copyItem(at: url, to: dest)
            loadProfiles()
        }
    }

    func openPanel(start: String) -> URL? {
        #if canImport(AppKit)
        let panel = NSOpenPanel()
        panel.canChooseFiles = true
        panel.allowsMultipleSelection = false
        panel.directoryURL = URL(fileURLWithPath: start)
        return panel.runModal() == .OK ? panel.url : nil
        #else
        return nil
        #endif
    }

    func savePanel(start: String, name: String) -> URL? {
        #if canImport(AppKit)
        let panel = NSSavePanel()
        panel.nameFieldStringValue = name
        panel.directoryURL = URL(fileURLWithPath: start)
        return panel.runModal() == .OK ? panel.url : nil
        #else
        return nil
        #endif
    }
}
#endif
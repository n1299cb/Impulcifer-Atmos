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
}
#endif
import SwiftUI
import AppKit

struct VisualizationView: View {
    var measurementDir: String
    @State private var images: [String] = []
    @State private var selectedImage: String?

    var body: some View {
        HStack {
            VStack {
                Button("Refresh") { loadImages() }
                List(images, id: \.self, selection: $selectedImage) { item in
                    Text(URL(fileURLWithPath: item).lastPathComponent)
                }
            }
            if let image = selectedImage, let nsImage = NSImage(contentsOfFile: image) {
                Image(nsImage: nsImage)
                    .resizable()
                    .scaledToFit()
            } else {
                Text("No Image")
            }
        }
        .onAppear { loadImages() }
        .padding()
    }

    func loadImages() {
        guard !measurementDir.isEmpty else { images = []; return }
        let url = URL(fileURLWithPath: measurementDir)
        if let items = try? FileManager.default.contentsOfDirectory(at: url, includingPropertiesForKeys: nil) {
            images = items.filter { $0.pathExtension.lowercased() == "png" }.map { $0.path }
        }
    }
}
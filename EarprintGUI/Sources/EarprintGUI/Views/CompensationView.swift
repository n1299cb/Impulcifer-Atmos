#if canImport(SwiftUI)
import SwiftUI

struct CompensationView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    @State private var headphoneFile: String = ""

    var body: some View {
        Form {
            HStack {
                TextField("Headphone EQ File", text: $headphoneFile)
                Button("Browse") {
                    #if os(macOS)
                    let panel = NSOpenPanel()
                    panel.canChooseFiles = true
                    if panel.runModal() == .OK { headphoneFile = panel.url?.path ?? "" }
                    #endif
                }
            }
            Button("Record Headphone EQ") {
                viewModel.recordHeadphoneEQ(measurementDir: FileManager.default.currentDirectoryPath,
                                            testSignal: "",
                                            playbackDevice: "",
                                            recordingDevice: "")
            }
        }
        .padding()
    }
}
#endif
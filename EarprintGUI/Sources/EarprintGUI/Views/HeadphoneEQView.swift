#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct HeadphoneEQView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    var testSignal: String
    var playbackDevice: String
    var recordingDevice: String

    var body: some View {
        VStack(alignment: .leading) {
            Text("Record the frequency response of your headphones using binaural microphones.")
                .fixedSize(horizontal: false, vertical: true)
            Button("Record Headphone EQ") {
                viewModel.recordHeadphoneEQ(measurementDir: measurementDir,
                                            testSignal: testSignal,
                                            playbackDevice: playbackDevice,
                                            recordingDevice: recordingDevice)
            }
            .disabled(measurementDir.isEmpty || testSignal.isEmpty)
            ScrollView {
                Text(viewModel.log)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding()
    }
}
#endif
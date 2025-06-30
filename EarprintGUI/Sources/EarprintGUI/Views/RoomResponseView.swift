#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct RoomResponseView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    var testSignal: String
    var playbackDevice: String
    var recordingDevice: String

    var body: some View {
        VStack(alignment: .leading) {
            Text("Capture a room response for room correction processing.")
                .fixedSize(horizontal: false, vertical: true)
            Button("Record Room Response") {
                viewModel.recordRoomResponse(measurementDir: measurementDir,
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
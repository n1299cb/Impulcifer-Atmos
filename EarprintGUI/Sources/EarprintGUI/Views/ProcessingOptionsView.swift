#if canImport(SwiftUI)
import SwiftUI
#if canImport(AVFoundation)
import AVFoundation
#endif

struct ProcessingOptionsView: View {
    @Binding var channelBalance: String
    @Binding var targetLevel: String
    @Binding var testSignal: String

#if canImport(AVFoundation)
    @StateObject private var previewer = AudioPreviewer()
    @State private var isPreviewing = false
#endif

    var body: some View {
        Form {
            Picker("Channel Balance", selection: $channelBalance) {
                Text("Off").tag("off")
                Text("Left").tag("left")
                Text("Right").tag("right")
                Text("Average").tag("avg")
                Text("Minimum").tag("min")
                Text("Mids").tag("mids")
                Text("Trend").tag("trend")
            }
            TextField("Target Level", text: $targetLevel)
#if canImport(AVFoundation)
            Button(isPreviewing ? "Stop Preview" : "Start Preview") {
                if isPreviewing {
                    previewer.stop()
                } else if !testSignal.isEmpty {
                    previewer.start(url: URL(fileURLWithPath: testSignal), balance: channelBalance)
                }
                isPreviewing.toggle()
            }
            .disabled(testSignal.isEmpty)
#endif
        }
        .padding()
    }
}
#endif
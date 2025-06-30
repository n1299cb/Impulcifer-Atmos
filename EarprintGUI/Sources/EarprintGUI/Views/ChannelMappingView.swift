#if canImport(SwiftUI)
import SwiftUI

struct ChannelMappingView: View {
    var playbackChannels: Int
    var recordingChannels: Int
    var speakerLabels: [String]
    @Binding var channelMapping: [String: [Int]]
    @Environment(\.dismiss) private var dismiss

    @State private var speakerSelections: [Int]
    @State private var micSelections: [Int]

    init(playbackChannels: Int, recordingChannels: Int, speakerLabels: [String], channelMapping: Binding<[String: [Int]]>) {
        self.playbackChannels = playbackChannels
        self.recordingChannels = recordingChannels
        self.speakerLabels = speakerLabels
        self._channelMapping = channelMapping
        _speakerSelections = State(initialValue: channelMapping.wrappedValue["output_channels"] ?? Array(0..<speakerLabels.count))
        _micSelections = State(initialValue: channelMapping.wrappedValue["input_channels"] ?? [0, 1])
    }

    var body: some View {
        VStack {
            HStack {
                Form {
                    Section(header: Text("Speaker Channels")) {
                        ForEach(speakerLabels.indices, id: \._self) { idx in
                            Picker(speakerLabels[idx], selection: $speakerSelections[idx]) {
                                ForEach(0..<playbackChannels, id: \._self) { ch in
                                    Text("\(ch + 1)").tag(ch)
                                }
                            }
                            .pickerStyle(MenuPickerStyle())
                        }
                    }
                }
                Form {
                    Section(header: Text("Microphone Channels")) {
                        ForEach(0..<2, id: \._self) { idx in
                            Picker(idx == 0 ? "Mic Left" : "Mic Right", selection: $micSelections[idx]) {
                                ForEach(0..<recordingChannels, id: \._self) { ch in
                                    Text("\(ch + 1)").tag(ch)
                                }
                            }
                            .pickerStyle(MenuPickerStyle())
                        }
                    }
                }
            }
            Button("Save") {
                channelMapping["output_channels"] = speakerSelections
                channelMapping["input_channels"] = micSelections
                dismiss()
            }
        }
        .padding()
    }
}
#endif
#include "TrueRoomPlugin.h"
#include "AAX.h"

AAX_CEffectParameters* AAX_CALLBACK TrueRoomPlugin::Create() {
    return new TrueRoomPlugin();
}

TrueRoomPlugin::TrueRoomPlugin() = default;
TrueRoomPlugin::~TrueRoomPlugin() = default;

AAX_Result TrueRoomPlugin::EffectInit() {
    // Allocate plugin parameters here
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::Initialize(double sampleRate, int32_t maxBlockSize) {
    sampleRate_ = sampleRate;
    blockSize_ = static_cast<size_t>(maxBlockSize);
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::ResetFieldData(AAX_CFieldIndex, void* oFieldData) const {
    // Zero buffers between processing calls
    std::memset(oFieldData, 0, sizeof(float));
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::LoadHRIR(const std::string& path) {
    // Load HRIR WAV and prepare RealTimeConvolver
    if (!hrir_.loadFromWav(path))
        return AAX_ERROR_NULL_POINTER;
    convolver_ = std::make_unique<RealTimeConvolver>(hrir_.leftIRs(), hrir_.rightIRs(), blockSize_);
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) {
    if (!convolver_)
        return AAX_ERROR_NULL_POINTER;

    size_t nSpeakers = hrir_.leftIRs().size();
    if (nSpeakers == 0)
        return AAX_ERROR_NULL_POINTER;
    std::vector<std::vector<float>> block(nSpeakers, std::vector<float>(inNumSamples));
    // Use left input for now; a real implementation would map each speaker
    // to its corresponding input channel or an encoded stream.
    for (size_t i = 0; i < nSpeakers; ++i)
        std::memcpy(block[i].data(), inSamples[0], sizeof(float) * inNumSamples);

    std::vector<float> left(inNumSamples), right(inNumSamples);
    convolver_->processBlock(block, left, right);
    std::memcpy(outSamples[0], left.data(), sizeof(float) * inNumSamples);
    std::memcpy(outSamples[1], right.data(), sizeof(float) * inNumSamples);
    return AAX_SUCCESS;

}
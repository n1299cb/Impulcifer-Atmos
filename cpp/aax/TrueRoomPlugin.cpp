#include "TrueRoomPlugin.h"
#include "AAX.h"
#include "HRIR.h" // hypothetical helper for loading HRIR

AAX_CEffectParameters* AAX_CALLBACK TrueRoomPlugin::Create() {
    return new TrueRoomPlugin();
}

TrueRoomPlugin::TrueRoomPlugin() = default;
TrueRoomPlugin::~TrueRoomPlugin() = default;

AAX_Result TrueRoomPlugin::EffectInit() {
    // Allocate plugin parameters here
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::ResetFieldData(AAX_CFieldIndex, void* oFieldData) const {
    // Zero buffers between processing calls
    std::memset(oFieldData, 0, sizeof(float));
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::LoadHRIR(const std::string& path) {
    // Load HRIR WAV and prepare RealTimeConvolver
    HRIR hrir;             // placeholder HRIR class
    if (!hrir.loadFromWav(path))
        return AAX_ERROR_NULL_POINTER;
    convolver_ = std::make_unique<RealTimeConvolver>(hrir.leftIRs(), hrir.rightIRs(), 1024);
    return AAX_SUCCESS;
}

AAX_Result TrueRoomPlugin::ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) {
    if (!convolver_)
        return AAX_ERROR_NULL_POINTER;
    std::vector<std::vector<float>> block(1, std::vector<float>(inNumSamples));
    std::memcpy(block[0].data(), inSamples[0], sizeof(float) * inNumSamples);
    std::vector<float> left(inNumSamples), right(inNumSamples);
    convolver_->processBlock(block, left, right);
    std::memcpy(outSamples[0], left.data(), sizeof(float) * inNumSamples);
    std::memcpy(outSamples[1], right.data(), sizeof(float) * inNumSamples);
    return AAX_SUCCESS;
}
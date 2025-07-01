#ifndef TRUEROOM_PLUGIN_H
#define TRUEROOM_PLUGIN_H

#include "AAX_CEffectParameters.h"
#include "RealTimeConvolver.h"
#include "HRIR.h"
#include <memory>
#include <string>

/**
 * TrueRoomPlugin wraps the RealTimeConvolver in an AAX effect so that
 * Pro Tools can perform binaural rendering in real time. The plugin
 * exposes a minimal interface: users load an HRIR WAV file and audio
 * blocks are processed through the convolver.
 */
class TrueRoomPlugin : public AAX_CEffectParameters {
public:
    TrueRoomPlugin();
    ~TrueRoomPlugin() override;

    static AAX_CEffectParameters* AAX_CALLBACK Create();

    AAX_Result EffectInit() override;
    AAX_Result ResetFieldData(AAX_CFieldIndex inFieldIndex, void* oFieldData) const override;
    AAX_Result ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) override;

    // Called by the host when sample rate or block size changes
    AAX_Result Initialize(double sampleRate, int32_t maxBlockSize);
    
    // Loads HRIRs from a WAV file and prepares the convolver
    AAX_Result LoadHRIR(const std::string& path);

private:
    std::unique_ptr<RealTimeConvolver> convolver_;
    HRIR hrir_;
    double sampleRate_ {48000.0};
    size_t blockSize_ {1024};
};

#endif // TRUEROOM_PLUGIN_H
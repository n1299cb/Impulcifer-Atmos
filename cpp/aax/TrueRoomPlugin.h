#ifndef TRUEROOM_PLUGIN_H
#define TRUEROOM_PLUGIN_H

#include "AAX_CEffectParameters.h"
#include "RealTimeConvolver.h"
#include <memory>
#include <string>

/** Minimal AAX plugin wrapper that uses RealTimeConvolver
 *  for binaural rendering.
 */
class TrueRoomPlugin : public AAX_CEffectParameters {
public:
    TrueRoomPlugin();
    ~TrueRoomPlugin() override;

    static AAX_CEffectParameters* AAX_CALLBACK Create();

    AAX_Result EffectInit() override;
    AAX_Result ResetFieldData(AAX_CFieldIndex inFieldIndex, void* oFieldData) const override;
    AAX_Result ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) override;

    // Loads HRIRs from a WAV file and prepares the convolver
    AAX_Result LoadHRIR(const std::string& path);

private:
    std::unique_ptr<RealTimeConvolver> convolver_;
};

#endif // TRUEROOM_PLUGIN_H
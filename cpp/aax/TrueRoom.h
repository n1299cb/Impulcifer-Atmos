#ifndef TRUEROOM_H
#define TRUEROOM_H

#include "AAX_CEffectParameters.h"
#include "HRIR.h"
#include <fftw3.h>
#include <vector>
#include <memory>
#include <string>
#include <map>

class RealTimeConvolver {
public:
    RealTimeConvolver(const std::vector<std::vector<float>>& leftIRs,
                      const std::vector<std::vector<float>>& rightIRs,
                      size_t maxBlockSize);
    RealTimeConvolver(const std::map<float, std::pair<std::vector<float>, std::vector<float>>>& brirs,
                      size_t maxBlockSize);
    ~RealTimeConvolver();

    void processBlock(const std::vector<std::vector<float>>& input,
                      std::vector<float>& outLeft,
                      std::vector<float>& outRight);
    void setOrientation(float yaw);

private:
    size_t nextPow2(size_t x) const;
    void prepareIRFFT(size_t fftSize);

    size_t maxBlockSize_;
    size_t maxIrLen_;
    size_t fftSize_;
    size_t nSpeakers_;

    std::vector<std::vector<float>> irLeft_;
    std::vector<std::vector<float>> irRight_;
    std::vector<std::vector<fftwf_complex>> irFFTLeft_;
    std::vector<std::vector<fftwf_complex>> irFFTRight_;

    std::vector<float> overlapL_;
    std::vector<float> overlapR_;

    // BRIR support
    bool usingBrir_ {false};
    std::vector<float> brirAngles_;
    std::vector<std::vector<fftwf_complex>> brirFFTLeft_;
    std::vector<std::vector<fftwf_complex>> brirFFTRight_;
    float yaw_ {0.f};
};

/**
 * TrueRoom wraps the RealTimeConvolver in an AAX effect so that
 * Pro Tools can perform binaural rendering in real time. The plugin
 * exposes a minimal interface: users load an HRIR WAV file and audio
 * blocks are processed through the convolver.
 */
class TrueRoom : public AAX_CEffectParameters {
public:
    TrueRoom();
    ~TrueRoom() override;

    static AAX_CEffectParameters* AAX_CALLBACK Create();

    AAX_Result EffectInit() override;
    AAX_Result ResetFieldData(AAX_CFieldIndex inFieldIndex, void* oFieldData) const override;
    AAX_Result ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) override;

    // Called by the host when sample rate or block size changes
    AAX_Result Initialize(double sampleRate, int32_t maxBlockSize);
    
    // Loads HRIRs from a WAV file and prepares the convolver
    AAX_Result LoadHRIR(const std::string& path);

    // Update head orientation in degrees
    AAX_Result SetYaw(float yaw);

private:
    std::unique_ptr<RealTimeConvolver> convolver_;
    HRIR hrir_;
    double sampleRate_ {48000.0};
    size_t blockSize_ {1024};
    float currentYaw_ {0.f};
};

#endif // TRUEROOM_H
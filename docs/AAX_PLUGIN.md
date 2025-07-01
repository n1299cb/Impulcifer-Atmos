# Building the TrueRoom AAX Plugin

This guide outlines how to wrap the real-time convolver in an AAX plugin so that Pro Tools can render binaural audio in real time.

## 1. Set up the AAX SDK

1. Download and unpack the AAX SDK from Avid.
2. Set the `AAX_SDK_ROOT` environment variable to the unpacked folder.
3. Install a C++17 compiler (Visual Studio on Windows, Xcode on macOS).

## 2. Plugin Skeleton

The `cpp/aax` folder contains the plugin sources. `TrueRoom.h` declares the plugin class and `TrueRoom.cpp` implements the wrapper. `HRIR.cpp` provides a small helper for loading multi-channel HRIR WAV files using libsndfile.

```cpp
class TrueRoom : public AAX_CEffectParameters {
    // ...
};
```

`ProcessAudio` copies the incoming block into `RealTimeConvolver` and writes the processed left/right channels back to Pro Tools. `Initialize()` is called by the host to update the sample rate and maximum block size used by the convolver.

## 3. Loading HRIR Files

Call `LoadHRIR()` with the path to an HRIR WAV. It converts the impulses into the format required by `RealTimeConvolver`.

```cpp
TrueRoom plugin;
plugin.LoadHRIR("/path/to/hrir.wav");
```

Make sure the WAV uses the layout expected by `hrir.py` so the loader can map channels correctly.

## 4. Building the Plugin

1. Add the `cpp` folder and AAX SDK headers to your compiler include path.
2. Link against the AAX library, FFTW and libsndfile (used by the HRIR loader).
3. Compile `TrueRoom.cpp` and `HRIR.cpp`.
4. Follow the AAX SDK documentation to generate the `.aaxplugin` bundle.

## 5. Usage

After building, copy the `.aaxplugin` bundle to your Pro Tools plug-ins directory. Insert the effect on a stereo track and load your HRIR file through the plugin's interface to enable binaural rendering.

The updated `TrueRoom` implementation also exposes a `SetYaw()` method so host automation or a head tracker can update the listener orientation. When used with a BRIR set containing multiple yaw angles, the convolver interpolates between the nearest measurements to produce smooth rotation.

This skeleton provides a starting point—extend it with parameters for block size, HRIR selection and any additional controls you need.
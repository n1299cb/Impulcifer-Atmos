# Building the TrueRoom AAX Plugin

This guide outlines how to wrap the real-time convolver in an AAX plugin so that Pro Tools can render binaural audio in real time.

## 1. Set up the AAX SDK

1. Download and unpack the AAX SDK from Avid.
2. Set the `AAX_SDK_ROOT` environment variable to the unpacked folder.
3. Install a C++17 compiler (Visual Studio on Windows, Xcode on macOS).

## 2. Plugin Skeleton

The `cpp/aax` folder contains a minimal starting point. `TrueRoomPlugin.h` declares the plugin class and `TrueRoomPlugin.cpp` implements the wrapper.

```cpp
class TrueRoomPlugin : public AAX_CEffectParameters {
    // ...
};
```

`ProcessAudio` copies the incoming block into `RealTimeConvolver` and writes the processed left/right channels back to Pro Tools.

## 3. Loading HRIR Files

Call `LoadHRIR()` with the path to an HRIR WAV. It converts the impulses into the format required by `RealTimeConvolver`.

```cpp
TrueRoomPlugin plugin;
plugin.LoadHRIR("/path/to/hrir.wav");
```

Make sure the WAV uses the layout expected by `hrir.py` so the loader can map channels correctly.

## 4. Building the Plugin

1. Add the `cpp` folder and AAX SDK headers to your compiler include path.
2. Link against the AAX library and FFTW (used by `RealTimeConvolver`).
3. Compile `TrueRoomPlugin.cpp` along with `RealTimeConvolver.cpp`.
4. Follow the AAX SDK documentation to generate the `.aaxplugin` bundle.

## 5. Usage

After building, copy the `.aaxplugin` bundle to your Pro Tools plug-ins directory. Insert the effect on a stereo track and load your HRIR file through the plugin's interface to enable binaural rendering.

This skeleton provides a starting point—extend it with parameters for block size, HRIR selection and any additional controls you need.
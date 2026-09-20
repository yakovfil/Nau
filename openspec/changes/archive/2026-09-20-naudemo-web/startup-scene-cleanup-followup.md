# Scene cleanup after interrupted startup

Task 2.4's new StopDuringSceneActivationCleansUpBeforeStopped regression fails in
SDK Node Debug: the component activates, startup waits on its activation task,
Stop is requested, then the task is released. The application never reports
Running and reaches Stopped, but destroys the component without invoking
deactivateComponent (observed zero calls, expected one).

The earlier normal/pending-update cases pass on native Windows, SDK Node and
Chrome Debug/Release. They only stop after successful startup. The new case
demonstrates why those checks alone cannot close the initialization cleanup gap.

## Cause

ApplicationImpl::finishStartup assigns m_mainLoop. A Stop request while startup
is pending bypasses finishStartup, leaving that pointer null. ShutdownRequested
therefore substitutes an already-resolved task for shutdownMainLoop. Destruction
of registered services eventually releases the scene objects, without orderly
scene deactivation. MainLoopService's scene-manager pointer is likewise acquired
in initService and can be absent when initialization did not reach that service.

## Applied bounded correction

Before starting game shutdown in ApplicationImpl::pollLifecycle:

```cpp
if (!m_mainLoop)
{
    m_mainLoop = getServiceProvider().find<MainLoopService>();
}
```

In MainLoopService::shutdownMainLoop, inside the existing scene-support guard,
before calling scene shutdown:

```cpp
if (!m_sceneManager)
{
    m_sceneManager = getServiceProvider().find<scene::ISceneManagerInternal>();
}
```

Use the already registered services; do not start or recreate them during cleanup.
Retain the existing asynchronous scene shutdown/polling path and failure reporting.
The minimal profile still has no scene manager. This changes the shared startup
cleanup path for native and browser applications.

The correction is applied. All 19 focused tests passed on native Windows, SDK
Node and Chrome in Debug and Release (demo_scene/run.py). The startup-Stop case
now observes one deactivation and one destruction, with no Running transition.

Regression checks also passed: native minimal lifecycle CTest (Debug), actual
web-minimal-debug success/visibility/repeated Stop, and browser-runtime-debug
stopstartup, deferred initialization failure, pending work and shutdownerror.
The browser sample measured 9.39 updates/second and reported complete cleanup.
Logs: build/demo-native-minimal-build.log, build/demo-minimal-regression-build.log,
build/demo-browser-{stopstartup,deferred,pending,shutdownerror}.json. Full scene
results are maintained in build/demo-scene-evidence; later shared-demo tests add
to this suite. Task 2.4 is complete.

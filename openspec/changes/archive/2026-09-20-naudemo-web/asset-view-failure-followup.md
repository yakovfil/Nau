# Initial asset-view failure settlement

Task 2.3's real asset-manager test loads the recorded cube successfully. Missing
buffers, truncation, malformed JSON, invalid accessor indices and unsupported
stride fail without an abort. A corrupt mesh index reaches the CPU view factory,
which correctly returns a failed Task. The shared AssetViewEntry::getAssetView
then propagates that failure before settling m_assetViewCreationState. Its
destructor aborts because the creation request remains pending. Concurrent
requesters would also remain waiting on that state.

Original reproduction, before the correction (after SDK setup and building the focused project):

```powershell
ctest --test-dir NauEngineLite/build/demo-scene-web-debug --output-on-failure
```

Original evidence: NauEngineLite/build/cpu-assets-test.log, InvalidIndexFails and
the AssetViewEntry destructor stack, executed in SDK Node Debug. The successful
post-fix runs are recorded below.

## Applied correction

In the shared initial AssetViewEntry::getAssetView creation branch, await
fabricateAssetView(container).doTry(). On failure, reject
m_assetViewCreationState with the same error before returning that error to the
first caller. Its existing auto-reset policy permits a later explicit asset
request; the browser application still treats required startup failure as
terminal and requires page reload. Keep the success/cached-view path unchanged.

Concrete replacement for the current single await assignment:

```cpp
auto result = co_await fabricateAssetView(container).doTry();
if (!result)
{
    auto error = result.getError();
    m_assetViewCreationState.reject(error);
    co_return error;
}
assetView = *std::move(result);
```

Verify two callers waiting on one deliberately delayed factory failure both
receive the error, explicit subsequent requests remain possible, and teardown
does not abort. Run the full scene/CPU asset suites on Windows and Chrome,
Debug/Release. Hot-reload updateAssetView behavior is separate from this initial
creation correction; no hot-reload semantics are proposed here.

The user approved this correction with "apply the fix". It is now applied to the
shared initial-view creation path. The new
FactoryFailureSettlesAllWaitersAndAllowsExplicitRetry test starts two requests
against one delayed factory, rejects that operation, checks that both callers
receive the original error object, then verifies two new requests share one
successful retry and teardown completes.

All 16 scene/CPU asset tests pass in Windows, SDK Node and Chrome, Debug/Release.
The corrupt-index and non-finite-position tests now complete without aborting.
Evidence: NauEngineLite/build/demo-scene-evidence/results.json and the adjacent
configure/build/CTest logs. Both browser runs exit zero with no page errors or
abort. Profile source/dependency audits and missing-source diagnostics also pass.

The shared failure-settlement blocker is resolved. Task 2.3 remains unchecked
pending the final input-validation and diagnostic coverage review.

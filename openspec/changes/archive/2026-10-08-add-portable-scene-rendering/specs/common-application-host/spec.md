# Spec Delta

## ADDED Requirements

### Requirement: Shared runtime-service lifecycle polling

The common host SHALL provide a platform-independent optional runtime-service polling contract on the application owner thread. Required service progress SHALL be possible during pending application startup, ordinary execution and eligible cleanup without dispatching premature game updates. Each eligible host lifecycle poll SHALL call each participating live service at most once; browser compatibility forwarding SHALL NOT duplicate calls. Existing browser runtime-service implementations SHALL remain source-compatible. Polling errors SHALL retain their diagnostics, initiate Stop, prevent later ordinary application updates and produce nonzero native completion or terminal browser failure after eligible cleanup. Services and owners SHALL remain alive through accepted work and SHALL NOT be polled after their lifetime ends. Non-rendering applications SHALL NOT acquire rendering dependencies from this contract.

#### Scenario: Startup requires service progress
- **WHEN** an optional runtime service must progress work before application startup can complete on Windows or web
- **THEN** owner-thread polling advances the work while startup remains gated and ordinary application updates do not run early

#### Scenario: A legacy browser service participates
- **WHEN** an existing browser runtime-service implementation is used with the common host
- **THEN** it receives its existing polling callback through compatibility forwarding once per eligible lifecycle poll without implementing a second callback

#### Scenario: Polling fails during execution or cleanup
- **WHEN** a participating runtime service returns a polling error
- **THEN** the host retains the error, stops ordinary updates, continues eligible safe cleanup and reports failure on both platforms without releasing owners used by accepted work

#### Scenario: Service cleanup completes
- **WHEN** a runtime service completes teardown and its owner is released
- **THEN** no subsequent lifecycle poll invokes the released service and the minimal application graph retains its existing rendering exclusions

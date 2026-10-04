# Proposal

## Why

Nau needs a small, portable foundation for a future widget-based UI after retiring Cocos UI. Establishing ownership and basic widget state first allows later capabilities to build on a tested hierarchy contract.

## What Changes

- Introduce a concrete `nau::ui::Widget` with runtime identity, optional debug name, local and effective visibility, and an ordered child hierarchy.
- Parents exclusively own children through `std::unique_ptr<Widget>`; children retain private non-owning parent pointers.
- Provide validated attachment and ownership-returning removal, rejecting invalid hierarchy operations without changing ownership.
- Add focused headless tests and native/browser compile validation for the portable foundation.

## Non-goals

No derived production widgets, layout or geometry, input, drawing, graphics resources, ticking, asset serialization, editor integration, service registration, or legacy UI compatibility.

## Capabilities

### New Capabilities

- `widget-foundation`: Basic widget state, exclusive tree ownership, parent references, and portable module integration.

### Modified Capabilities

None. The Cocos UI retirement remains intact; this is a new implementation with no restored legacy APIs or dependencies.

## Impact

- New implementation and tests under `NauEngineModules/modules/ui/`, plus module build and SDK integration where required.
- New `NauUi` library exposing `nau/ui/widget.h`, independent of graphics, input, ScreenText, and platform windows.
- Standalone NauEngineLite and existing minimal/scene default module selections remain unchanged.
- No new third-party dependencies or application changes.

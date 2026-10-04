# Spec Delta

## ADDED Requirements

### Requirement: Parent-relative widget spatial state

Each widget SHALL expose a local three-dimensional translation, quaternion rotation, and scale using the engine transform type. Translation SHALL locate the widget's pivot relative to its parent's pivot. The local mapping SHALL apply scale, then rotation, then translation. Fresh widgets SHALL have identity local transforms. Attachment, detachment, and rejected hierarchy operations SHALL preserve local spatial state, size, and pivot, as well as existing identity guarantees.

#### Scenario: New widget and local transform edit
- **WHEN** a widget is created and subsequently assigned a valid local transform
- **THEN** its initial transform is identity and the assigned transform becomes observable without a frame update or scene startup

#### Scenario: Subtree changes parent
- **WHEN** a subtree is detached and attached to another parent
- **THEN** every widget retains its local transform, size, and pivot while the subtree's accumulated placement follows the new ancestry

### Requirement: Widget rectangle size and pivot

Each widget SHALL expose an unscaled width and height and a dimensionless two-component pivot. Defaults SHALL be size (0, 0) and pivot (0.5, 0.5). The rectangle SHALL lie in the local XY plane at Z=0 with minimum coordinates equal to negative pivot times size and maximum coordinates equal to (1 minus pivot) times size, component by component. Pivot (0, 0) SHALL denote the minimum-coordinate corner and (1, 1) the maximum-coordinate corner. Finite pivots outside this interval SHALL be supported. Size and pivot edits SHALL NOT change the widget's transform or any descendant's local or accumulated transform.

#### Scenario: Centered rectangle
- **WHEN** size is (200, 100) and pivot is (0.5, 0.5)
- **THEN** its local rectangle spans (-100, -50, 0) to (100, 50, 0)

#### Scenario: External pivot and unchanged children
- **WHEN** a parent with attached children changes its size and sets pivot to (2, -1)
- **THEN** its rectangle uses that external pivot without clamping and all child origins retain their accumulated positions

### Requirement: Immediate accumulated widget matrix

Widgets SHALL expose a matrix mapping their pivot-relative local coordinates into the coordinate space outside the top-level widget. A parentless widget's matrix SHALL equal its local transform matrix. An attached widget's matrix SHALL equal its parent's accumulated matrix multiplied by its own local matrix. Queries SHALL reflect ancestor edits and hierarchy changes immediately and preserve the full affine composition, including shear from rotation combined with nonuniform scale. Size and pivot offsets SHALL NOT enter this hierarchy composition. This coordinate space SHALL NOT imply scene attachment, screen pixels, projection, or a layout system.

#### Scenario: Rotated child under scaled ancestry
- **WHEN** a child has a nontrivial rotation beneath an ancestor with nonuniform scale
- **THEN** its accumulated matrix matches the ordered product of local matrices, including resulting shear, without decomposing the result into translation, rotation, and scale

#### Scenario: Ancestor edits and detached root
- **WHEN** an ancestor transform changes and the subtree is later detached
- **THEN** the next query reflects the ancestor edit before detachment and the detached root's own local matrix afterward

### Requirement: Validated widget spatial updates

Spatial setters SHALL report failure and preserve prior state for non-finite components, negative size components, or a quaternion that fails the engine transform's normalized-rotation validity check. Valid finite zero or negative scale SHALL be accepted; zero size SHALL be accepted. Updates SHALL NOT silently clamp or normalize submitted state. Getters SHALL NOT permit mutation that bypasses validation. These behaviors SHALL hold in Debug, Release, and supported browser builds using the existing portable dependency closure.

#### Scenario: Rejected spatial edit
- **WHEN** a setter receives NaN, infinity, a negative size, or an invalid quaternion
- **THEN** it reports failure and leaves all widget state and hierarchy relationships unchanged

#### Scenario: Degenerate and reflected geometry
- **WHEN** a widget receives zero size or a valid transform containing zero or negative scale
- **THEN** the edit succeeds and forward matrix queries remain available without requiring an inverse

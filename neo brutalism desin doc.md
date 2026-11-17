Yes. **I think this direction is substantially better for BitStream**.

The first reference was soft/neumorphic and premium, but this neo-brutalist system gives BitStream something the previous direction lacked: **a strong visual identity**. More importantly, its rules are explicit enough that an AI coding agent can actually reproduce them consistently instead of vaguely interpreting “make it premium.”

Below is the design philosophy I would hand directly to the AI implementing BitStream. I’m being deliberately prescriptive: these are **rules**, not suggestions.

* * *

BitStream UI — Neo-Brutalist Design System Specification
========================================================

0. Core instruction

-------------------

**Do not interpret “neo-brutalist” as a generic black-and-white brutalist website.**

The target style is a **modern neo-brutalist product interface** with:

* extremely strong visual hierarchy

* thick black outlines

* hard, deliberate geometry

* limited corner rounding

* solid high-saturation accent blocks

* paper-like warm background

* off-white surfaces

* black typography

* strong grid alignment

* deliberately visible interaction states

* small, controlled offset shadows

* unapologetically bold typography

* clear component boundaries

* minimal decorative ornament

* high information clarity

* obvious primary actions

The interface should look **designed and systematic**, not rough, broken, primitive, or intentionally ugly.

The aesthetic is:

> **bold, graphic, tactile, editorial, technical, systematic, high-contrast, slightly rebellious, but still usable as serious software.**

* * *

1. The most important rule: everything belongs to a system
   ==========================================================

Do not individually style components.

Do not make:

* one button with 8px radius

* another with 14px radius

* another with 0px radius

* one shadow with 3px offset

* another with 12px

* arbitrary colors

* arbitrary font sizes

* arbitrary margins

Everything must derive from explicit design tokens.

The UI should feel as though a designer created a **physical design-system specification first and then built the application from it**.

Think:
    DESIGN TOKENS
          ↓
    COMPONENTS
          ↓
    SCREENS
          ↓
    APPLICATION

Not:
    SCREEN
     ↓
    random CSS
     ↓
    more random CSS

* * *

2. Overall aesthetic
   ====================

The application should feel like a cross between:

* a technical instrument

* an editorial poster

* a physical engineering control panel

* a contemporary design-system library

* a carefully printed instruction manual

It should **not** feel like:

* a generic SaaS dashboard

* a glassmorphism app

* an Apple clone

* a gaming UI

* a cyberpunk interface

* a terminal emulator

* a retro computer interface

* a deliberately broken website

* a monochrome corporate admin panel

* * *

3. Visual keywords
   ==================

The implementation should consistently evoke:

**Bold**

**Loud**

**Systematic**

**Useful**

**Graphic**

**Physical**

**High-contrast**

**Structured**

**Editorial**

**Technical**

**Confident**

* * *

4. Background
   =============

The application background should be a **warm paper beige**, not pure white.

Reference philosophy:
    Paper beige
    ≈ #F5F5DC

The exact value can be adjusted, but it must remain:

* warm

* slightly creamy

* visually closer to paper than a web canvas

* light enough for black text

* distinct from pure white surfaces

The background should visually communicate:

> **printed design sheet / technical manual / paper substrate**

rather than:

> browser page.

* * *

5. Surface colors
   =================

Use a very small surface palette.

### Primary background

Warm paper beige.

### Surface

Off-white / near-white.

### Strong contrast surface

Black.

### Accent surfaces

Teal, magenta, yellow, and possibly red where appropriate.

Do not introduce dozens of shades.

The palette should look deliberately constrained.

* * *

6. Core color palette
   =====================

The reference uses approximately these conceptual colors:
    BLACK
    #000000

    WHITE
    #FFFFFF

    PAPER BEIGE
    #F5F5DC

    ACCENT TEAL
    #00C2CB

    ACCENT MAGENTA
    #FF00FF

    ACCENT YELLOW
    #FFD700

You can tune the exact values, but preserve the relationships.

The three primary accents are deliberately **strong and saturated**.

They should not become pastel.

This is one of the biggest differences from the previous soft-mint design.

* * *

7. Accent color philosophy
   ==========================

Teal, magenta, and yellow should function as **solid graphic blocks**.

They are not gradients.

Do not use:
    linear-gradient(...)
    radial-gradient(...)

as the primary visual treatment.

Accent areas should look almost like ink printed onto paper.

* * *

8. Accent hierarchy
   ===================

Do not use all three accents equally everywhere.

Establish hierarchy.

### Teal

Primary brand/action color.

Use for:

* primary buttons

* selected states

* active navigation

* progress

* success where appropriate

* key interactive elements

### Yellow

Secondary attention color.

Use for:

* warnings

* step indicators

* secondary highlights

* selected-but-not-primary states

### Magenta

Special/high-impact state.

Use for:

* destructive actions

* exceptional alerts

* special modes

* steganography-enabled state, potentially

Magenta should feel **special and slightly dangerous**.

Do not make the entire application magenta.

* * *

9. Black is a design color, not just text
   =========================================

Black should be used heavily.

It should function as:

* text

* border

* outline

* structural divider

* button background

* icon color

* table header background

* emphasis surface

* shadow offset

The reference is not afraid of large black shapes.

That confidence should carry into the application.

* * *

10. The primary visual characteristic: thick black strokes
    ==========================================================

This is non-negotiable.

The majority of major UI components should have a **clearly visible black border**.

Typical border:
    2px–3px solid #000000

For major hero components:
    3px

For smaller controls:
    2px

The border should be visually obvious.

Don't use:
    1px rgba(0,0,0,0.08)

That belongs to the previous soft UI system.

Here, boundaries are supposed to be seen.

* * *

11. Borders communicate structure
    =================================

In this system, borders are not subtle separators.

They communicate:

> **This is a distinct object.**

Cards should have visible black outlines.

Buttons should have visible black outlines.

Inputs should have visible black outlines.

Modals should have visible black outlines.

Tabs should have visible black outlines where appropriate.

* * *

12. Avoid border overload
    =========================

However, do not outline absolutely everything.

Large pages can become visually noisy if every tiny label gets a black box.

Use thick borders primarily around:

* interactive objects

* structural containers

* major content blocks

* important state changes

Text itself should generally remain borderless.

* * *

13. Corner radius philosophy
    ============================

**Neo-brutalist geometry should be mostly squared.**

This is extremely important.

Do not apply:
    border-radius: 20px;

to everything.

The reference explicitly calls for:

> **limited radii**

Recommended system:
    0px
    2px
    4px
    6px

Occasionally:
    8px

for special controls.

Default major component radius should probably be:

**4px or 6px.**

Some objects can remain completely square.

* * *

14. No pill-shaped everything
    =============================

Avoid the modern SaaS tendency to make:

* buttons pills

* tabs pills

* chips pills

* search boxes pills

* cards rounded

* modals rounded

* everything an iPhone widget

Neo-brutalism should feel **constructed**, not inflated.

Pills should only be used when the semantic meaning specifically calls for a compact chip/tag.

* * *

15. Typography is the second defining characteristic
    ====================================================

The typography should be **huge, heavy, condensed-looking, and unapologetic**.

The poster uses extremely bold headings.

Typography is not merely content.

It is part of the graphic composition.

* * *

16. Font choice
    ===============

Use a heavy display sans-serif.

Good candidates:

* Anton

* Archivo Black

* Bebas Neue

* Oswald Heavy

* Impact-like alternatives

* Space Grotesk Heavy

* Inter Black, if a less condensed appearance is desired

For a polished app, I would prefer something like:

**Archivo Black / Anton / Space Grotesk Heavy**

for headings.

For body text, use a clean neutral sans-serif such as:

**Inter**

This creates a deliberate distinction between:

> **graphic display typography**

and

> **functional interface typography.**

* * *

17. Typography hierarchy
    ========================

Use a very explicit scale.

Something conceptually like:
    H1
    56–72px

    H2
    40–48px

    H3
    28–36px

    H4
    20–24px

    Body
    16–18px

    Small
    13–14px

    Caption
    11–12px

Do not make everything 14px.

The interface should be visually loud.

* * *

18. Headings should be visually dominant
    ========================================

Headings should often be:

* uppercase or title case where appropriate

* heavy weight

* tight line-height

* dark black

* tightly grouped

Example:

**ENCODE FILES**

should look like a section title.

Not:

> Encode Files

in tiny gray text.

* * *

19. Use uppercase strategically
    ===============================

The reference makes heavy use of uppercase labels.

Use uppercase for:

* section titles

* control categories

* compact labels

* statuses

* navigation where appropriate

Do not force the entire application into uppercase.

For normal descriptive text, sentence case is better.

* * *

20. Letter spacing
    ==================

Headings should generally have **tight or neutral tracking**.

Don't apply huge letter spacing.

Neo-brutalism is bold because of:

* size

* weight

* contrast

* geometry

not because every heading is:
    L E T T E R S P A C E D

* * *

21. Body text
    =============

Body text should remain highly readable.

Use:

* 16–18px on desktop for important descriptions

* 14–16px for ordinary UI labels

* strong contrast

* comfortable line height

Do not let the brutalist style destroy usability.

* * *

22. Labels
    ==========

Labels should be:

* bold

* short

* explicit

* black

Examples:
    RESOLUTION
    FRAME RATE
    OUTPUT FORMAT
    COVER VIDEO
    STEGANOGRAPHY

This is far better than vague labels such as:

> Settings

followed by unexplained controls.

* * *

23. Spacing philosophy
    ======================

The reference uses a strict spacing system.

Use a base scale derived from approximately:
    4
    8
    12
    16
    24
    32
    48
    64
    96

Do not randomly use:
    17px
    19px
    27px
    31px

for no reason.

* * *

24. Large margins are okay
    ==========================

Neo-brutalist doesn't mean cramped.

The poster has strong whitespace between sections.

For the application:

* give major sections breathing room

* separate unrelated content strongly

* use whitespace before reaching for another card

* * *

25. Alignment is sacred
    =======================

The reference explicitly calls out:

> **strict grid alignment**

This should be a major implementation rule.

All major elements should align to a common grid.

For example:
    ┌───────────────────────────────────────────┐
    │ HEADER                                    │
    │                                           │
    │ SECTION TITLE                             │
    │ ───────────────────────────────────────── │
    │ CONTENT                                   │
    │                                           │
    │ SECTION TITLE                             │
    │ ───────────────────────────────────────── │
    │ CONTENT                                   │
    └───────────────────────────────────────────┘

Vertical edges should line up.

Section headings should share the same left edge.

Buttons should align with surrounding content.

Inputs should align.

Don't freestyle positioning.

* * *

26. Use a consistent content width
    ==================================

The application should have a defined maximum content width.

Something like:
    max-width: 1200–1400px

depending on the application.

Do not let content stretch arbitrarily across a huge monitor.

The design should remain poster-like and controlled.

* * *

27. Grid columns
    ================

Complex screens can use a grid such as:
    1 column
    2 columns
    3 columns

but the column boundaries should be deliberate.

For example:
    ┌──────────────────┬────────────────────────┐
    │                  │                        │
    │ INPUT            │ ENCODING               │
    │                  │ SETTINGS               │
    │                  │                        │
    └──────────────────┴────────────────────────┘

Avoid arbitrary masonry layouts.

* * *

28. Divider lines
    =================

The reference uses strong horizontal lines to structure sections.

You should use:
    2px solid black

for major separators.

For example:
    ENCODE FILES
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is one of the easiest ways to reproduce the poster's graphic structure.

* * *

29. Section titles
    ==================

Every major screen section can have:
    SECTION TITLE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The title should be:

* bold

* large

* black

* left aligned

The divider starts near the title or underneath it.

This creates a very editorial system.

* * *

30. Buttons
    ===========

Buttons should look **physical and explicit**.

A button is an object.

Default structure:
    background
    + thick black border
    + slight offset shadow
    + limited radius
    + strong text

* * *

31. Offset shadow philosophy
    ============================

This is a crucial characteristic of the reference.

Instead of soft blur shadows, use **hard or semi-hard offset shadows**.

For example:
    box-shadow:
    4px 4px 0 #000;

or:
    box-shadow:
    3px 3px 0 #000;

This creates the graphic printed-object appearance.

This is one of the biggest differences between the neo-brutalist reference and the first neumorphic reference.

* * *

32. Do not use soft floating shadows everywhere
    ===============================================

Avoid:
    box-shadow:
    0 10px 30px rgba(0,0,0,0.18);

for ordinary components.

The shadow should generally behave like a **graphic offset**.

Hard offset shadows are preferred.

* * *

33. Shadow tokens
    =================

Define a small system:
    SHADOW-0
    none

    SHADOW-1
    2px 2px 0 black

    SHADOW-2
    4px 4px 0 black

    SHADOW-3
    6px 6px 0 black

Use only a few.

Do not create 17 different shadow values.

* * *

34. Shadows should be structural
    ================================

The black offset shadow indicates:

> This object physically sits above the page.

That means the shadow should appear consistently on:

* buttons

* cards

* modals

* important inputs

* major interactive elements

* * *

35. Interaction states should be very obvious
    =============================================

The reference explicitly says:

> **FOCUS ALWAYS VISIBLE.**

This should become a core accessibility rule.

Never remove browser focus outlines without replacing them.

* * *

36. Focus state
    ===============

Focused components should gain a very obvious accent outline.

Possible implementation:
    outline:
    3px solid #FFD700;
    outline-offset:
    3px;

or teal depending on the component.

The focus state should be impossible to miss.

* * *

37. Hover state
    ===============

Hover should be energetic but simple.

Possible behavior:
    default:
    box-shadow 4px 4px 0 #000

    hover:
    box-shadow 6px 6px 0 #000
    transform translate(-2px, -2px)

Or the opposite depending on the physical metaphor.

The change should make the element feel more active.

* * *

38. Pressed state
    =================

On press:
    transform: translate(2px, 2px)
    box-shadow: 1px 1px 0 #000

The button visually moves toward the page.

This is important.

Neo-brutalist interaction should feel **mechanical**.

* * *

39. Disabled state
    ==================

Don't simply lower opacity to 30%.

Instead make the component visibly disabled through:

* gray fill

* muted border

* reduced shadow

* lower contrast

But still preserve the black outlines enough to maintain structural consistency.

* * *

40. Primary button
    ==================

Primary action should typically use:

**Teal fill + black border + black offset shadow + black/dark text.**

Example:
    ┌─────────────────────┐
    │     ENCODE VIDEO    │
    └─────────────────────┘
           ▄▄▄▄▄

The teal block should be visually obvious.

* * *

41. Secondary button
    ====================

Use:

**Off-white fill + black border + black shadow**

This makes it clearly secondary.

* * *

42. Destructive button
    ======================

Use:

**Magenta or strong warm red** depending on context.

The poster uses magenta aggressively for destructive states.

For BitStream:

* delete

* overwrite

* clear

* remove encoded item

could use the destructive accent.

But don't use magenta for normal navigation.

* * *

43. Tertiary buttons
    ====================

Can be:

* text only

* black text

* no background

* no heavy shadow

But keep their typography strong enough to remain visible.

* * *

44. Icon-only buttons
    =====================

Icon buttons should still look like objects.

For example:
    [ + ]
    [ × ]
    [ ⚙ ]
    [ → ]

with:

* thick black border

* small radius

* optional offset shadow

* clear hover state

Do not put a tiny gray icon into a giant blank circle.

* * *

45. Inputs
    ==========

Inputs should look like **outlined physical fields**.

Default:
    ┌────────────────────────────┐
    │  file name...              │
    └────────────────────────────┘

with:

* thick black border

* warm/off-white surface

* small radius

* clear focus state

* * *

46. Error input
    ===============

Error fields should become visually unmistakable.

Possible:

* magenta or red border

* error label beneath

* high contrast

Example:
    ┌────────────────────────────┐
    │                            │
    └────────────────────────────┘
    ERROR: INVALID FILE FORMAT

Don't rely solely on a tiny red icon.

* * *

47. Helper text
    ===============

Helper text should be smaller but still readable.

Example:
    FRAME RATE
    [ 30 FPS ]

    Higher frame rates require more storage.

Body explanation is secondary and should not compete with the label.

* * *

48. Checkboxes
    ==============

Checkboxes should be square.

Do not use giant rounded modern checkbox widgets.

Use:
    □
    ☑

visually represented as actual square controls.

Selected:

* black background with white check

* or accent fill with black/white check

* * *

49. Radio buttons
    =================

Radio controls can remain circular because their semantics are inherently circular.

But they should use the same brutalist treatment:

* black outline

* bold selected state

* high contrast

* * *

50. Toggles
    ===========

Toggles can use black/yellow or black/teal.

For example:
    [ OFF ] [ ON ]

rather than copying a modern floating iOS toggle.

The reference uses a strongly graphic toggle.

* * *

51. Tabs
    ========

Tabs should feel like **physical labels**.

Active tab:

* teal fill

* thick border

* bold type

Inactive tab:

* paper/off-white

* black text

* possibly only bottom border

* * *

52. No subtle invisible active state
    ====================================

Never use:

> slightly darker text

as the only indication that a tab is active.

The active state should be visually undeniable.

* * *

53. Steps / progress navigation
    ===============================

The reference uses numbered steps connected by a line.

This is perfect for BitStream.

You could represent:
    1. FILES
    ───────●────────●────────●───────
           1        2        3

            CONFIGURE

For BitStream:

**1. Select files**

**2. Configure**

**3. Encode**

**4. Verify**

Teal for current/complete.

Yellow for next/attention.

White for future.

* * *

54. Progress bars
    =================

Progress bars should be **rectangular and graphic**.

Not soft capsules.

Example:
    ┌─────────────────────────────────┐
    │███████████████░░░░░░░░░░░░░░░░│
    └─────────────────────────────────┘

Black outline.

Teal fill.

Explicit percentage.

* * *

55. Progress should show real information
    =========================================

For BitStream, show:
    76%

    Encoding frame 1,842 / 2,401

or:
    Embedding payload
    76% complete

Do not fake progress.

The UI design strongly benefits from the underlying engineering being real.

* * *

56. Cards
    =========

Cards should look almost like physical cards pinned to the page.

Use:

* paper/off-white surface

* 2–3px black border

* 4–8px black offset shadow

* limited radius

A card should visibly occupy physical space.

* * *

57. Card hierarchy
    ==================

Not every card should have the same elevation.

Major card:
    6px offset shadow

secondary:
    4px

small:
    2px

This creates depth while staying graphic.

* * *

58. Tables
    ==========

Tables should be extremely structured.

The reference uses:

* black header

* white/cream body

* strong grid lines

* compact typography

* explicit action column

For BitStream history:
    ┌─────────────────────────────────────────────┐
    │ FILE     SIZE     MODE      STATUS     ...  │
    ├─────────────────────────────────────────────┤
    │ archive  4.2 MB   FFV1      ✓ VERIFIED     │
    │ photos   82 MB    STEGO     ✓ VERIFIED     │
    └─────────────────────────────────────────────┘

This fits the aesthetic beautifully.

* * *

59. Table headers
    =================

Table header can be:

**solid black**

with:

**white text**

This is one of the most visually effective elements in the reference.

Use it sparingly.

* * *

60. List items
    ==============

List rows should have clear borders.

A selected list row can use:

* teal

* yellow

* black

* bold indicator

Example:
    [●] project.zip
        4.8 MB

The black outlines keep everything structured.

* * *

61. Badges
    ==========

Badges should be small and graphic.

Examples:
    FFV1
    LOSSLESS
    STEGO
    VERIFIED
    ERROR

Use solid accent fills.

Avoid soft gray pill badges everywhere.

* * *

62. Alerts
    ==========

Alerts should be **strong graphic banners**.

Reference states:

* success → teal/green

* warning → yellow

* error → magenta/red

Each alert should have:

* icon

* bold label

* concise text

* visible border

* maybe offset shadow

* * *

63. Toasts
    ==========

Toasts should not float like translucent glass.

Instead:
    ┌─────────────────────────────────────┐
    │ ✓ ENCODING COMPLETE            ×   │
    │ Video created successfully.         │
    └─────────────────────────────────────┘
           ▄▄▄

Strong border.

Accent fill.

Visible close control.

* * *

64. Modals
    ==========

Modals should look like an actual **physical panel dropped onto the page**.

Structure:
    ┌─────────────────────────────┐
    │ CONFIRM ENCODE              │
    │                             │
    │ This will create a 4.2 GB   │
    │ lossless FFV1 video.        │
    │                             │
    │ [ CANCEL ] [ CONFIRM ]      │
    └─────────────────────────────┘
          ▄▄▄▄▄▄▄

Use:

* large black border

* paper surface

* strong offset shadow

* short title

* explicit actions

* * *

65. Backdrop
    ============

The modal backdrop can darken the page, but avoid making it look like a glassmorphism overlay.

A simple semi-transparent black overlay works.

The modal itself should provide the visual focus.

* * *

66. Empty states
    ================

Empty states should be **graphic and direct**.

Example:
    NO ENCODED VIDEOS

    Nothing has been encoded yet.

    [ CREATE YOUR FIRST VIDEO ]

Include a simple line/icon illustration if useful.

Don't use generic stock illustrations.

* * *

67. Icons
    =========

Icons should be **bold and simple**.

The reference uses very obvious symbols:

* close

* check

* gear

* arrow

* user

* trash

* search

* menu

Use one coherent icon family.

Good options:

**Lucide**, but with appropriate stroke weight.

Or another icon system that supports heavier strokes.

* * *

68. Icons should not become decorative noise
    ============================================

Do not put an icon beside every word just because you can.

Icons should convey:

* action

* state

* object identity

* navigation

not decoration.

* * *

69. Illustration language
    =========================

If BitStream needs illustrations, use:

* thick black outlines

* simple geometric forms

* teal/yellow/magenta blocks

* off-white interiors

* minimal shading

No glossy 3D illustrations.

No realistic imagery unless the image itself is user content.

* * *

70. Data visualization
    ======================

For BitStream-specific graphs, use the same brutalist language.

For example, payload capacity:
    CAPACITY
    ━━━━━━━━━━━━━━━━━━━━

    1080p ┃████████████████████
    720p  ┃██████████████
    480p  ┃████████

Use solid accent blocks.

Avoid:

* gradients

* excessive gridlines

* glass panels

* pastel colors

* * *

71. Technical diagrams
    ======================

This style is fantastic for technical diagrams.

BitStream could show:
    FILES
      │
      ▼
    ZIP PAYLOAD
      │
      ▼
    BITS
      │
      ▼
    VIDEO FRAMES
      │
      ▼
    FFV1
      │
      ▼
    OUTPUT VIDEO

Each stage can be a rectangular black-bordered node.

Use teal for active stages.

* * *

72. The UI should communicate engineering
    =========================================

This is important for your portfolio.

Do not hide the technical sophistication behind a pretty frontend.

Expose useful engineering information:
    Container      FFV1
    Resolution     1920×1080
    Frame rate     30 FPS
    Payload        4.82 MB
    Frames         1,204
    Integrity      VERIFIED
    Mode           STEGANOGRAPHIC

This gives the application technical credibility.

* * *

73. Steganography mode
    ======================

This could be one of the coolest visual states.

Normal mode:
    MODE
    [ NORMAL ]

Steganographic mode:
    MODE
    [ STEGO ]

When activated:

* magenta accent

* clear warning/info

* cover video selection appears

* payload capacity information becomes visible

The UI should **explain the mode**, not just toggle a switch.

* * *

74. Capacity display
    ====================

When selecting a cover video, show:
    COVER VIDEO
    example.mp4

    CAPACITY
    18.4 MB

    PAYLOAD
    12.8 MB

    HEADROOM
    5.6 MB

This can be displayed as a simple brutalist meter.

This would be visually and technically excellent.

* * *

75. Encoding workflow
    =====================

I would structure the main app around a workflow rather than dashboard cards.

Something like:
    1 SELECT
    ────────────────────────────

    Drop files / choose files


    2 CONFIGURE
    ────────────────────────────

    Format
    Resolution
    FPS
    Steganography


    3 ENCODE
    ────────────────────────────

    [ ENCODE VIDEO ]


    4 VERIFY
    ────────────────────────────

    ✓ SHA-256 MATCH

The visual language naturally supports this.

* * *

76. Sidebar philosophy
    ======================

A sidebar is acceptable, but don't make it a giant generic SaaS navigation rail.

Use:
    BITSTREAM

    ENCODE
    DECODE
    HISTORY
    SETTINGS

Very simple.

Potentially with a bold black vertical divider.

* * *

77. Sidebar selected state
    ==========================

Selected:
    ████████████████
      ENCODE
    ████████████████

with teal or yellow.

Inactive:

black text on beige.

Do not use tiny gray text.

* * *

78. Header
    ==========

The header should be simple.

Potentially:
    BITSTREAM                         SETTINGS
    Lossless data as video

Brand name can be extremely bold.

Do not put 15 icons in the header.

* * *

79. Logo treatment
    ==================

The BitStream logo could potentially use a **bold wordmark**.

For example:

**BITSTREAM**

in a heavy display font.

A tiny accent block could sit beside it.

Avoid elaborate gradients or 3D logos.

* * *

80. Decorative language
    =======================

The reference does use decorative labels and little handwritten-looking notes such as:

* "ONE PRIMARY ACTION"

* "KEEP HIT AREA 44PX"

* "FOCUS ALWAYS VISIBLE"

These are useful in the **design system poster**, but do not literally recreate all of these annotations inside the app.

Instead, translate their philosophy into behavior.

For example:

> 44px minimum hit target

becomes an implementation rule.

* * *

81. Hit targets
    ===============

Interactive controls should have approximately:

**44px minimum touch/click target**

where practical.

Especially:

* icon buttons

* close buttons

* navigation

* compact controls

Don't make the brutalist interface physically tiny.

* * *

82. One primary action
    ======================

This is one of the strongest principles in the reference.

Every important screen should have:

> **ONE obvious primary action.**

For BitStream's encode screen:

**ENCODE VIDEO**

should be the strongest button.

Not:

* Encode

* Save

* Export

* Apply

* Start

* Confirm

all competing visually.

* * *

83. Secondary actions
    =====================

Secondary actions should be visibly less important.

For example:
    [ ENCODE VIDEO ]

    [ SAVE PRESET ]     CANCEL

The primary action gets the teal block.

* * *

84. Don't make every button colorful
    ====================================

Accent colors indicate hierarchy.

If:

* Encode = teal

* Save = yellow

* Browse = magenta

* Cancel = gray

* Reset = blue

the hierarchy collapses.

Use color sparingly.

* * *

85. Danger semantics
    ====================

Use magenta/red only where danger deserves it.

For example:

**Delete encoded video**

could be magenta.

Ordinary:

**Remove file from queue**

might remain white/black.

* * *

86. Accessibility remains mandatory
    ===================================

Brutalism does **not** justify poor accessibility.

Maintain:

* strong text contrast

* visible focus

* clear labels

* keyboard navigation

* appropriate hit sizes

* semantic controls

* non-color state indicators

The poster's emphasis on focus is particularly good.

* * *

87. Keyboard interaction
    ========================

Every major UI action should be keyboard-accessible.

Focus should visibly move through:
    Teal/yellow outline
    +
    black border
    +
    clear active state

Never disable default accessibility behavior simply to make the UI look cleaner.

* * *

88. Motion should be mechanical
    ===============================

Animations should not be soft and floaty.

Think:

> click → shift → snap

rather than:

> float → blur → fade → bounce

Transitions should generally be:

**100–200ms**

and purposeful.

* * *

89. Hover animation
    ===================

A component might move:
    -2px / -2px

and increase its offset shadow.

This makes it feel like a printed object being lifted.

* * *

90. Press animation
    ===================

On click:
    translate(2px, 2px)

and reduce shadow.

This makes the interface feel **physically actuated**.

* * *

91. No excessive blur
    =====================

Avoid backdrop blur as a major visual technique.

If blur is used at all, it should be incidental rather than defining.

The style relies primarily on:

**flat surfaces + black outlines + offset shadows + color blocks.**

* * *

92. No glassmorphism
    ====================

Explicitly tell the implementation AI:

> Do not use glassmorphism.

No:
    rgba(255,255,255,.3)
    backdrop-filter: blur(...)
    frosted panels

as the primary design vocabulary.

That would immediately pull the interface away from the reference.

* * *

93. No soft gradients
    =====================

Avoid gradient backgrounds.

Avoid gradient buttons.

Avoid gradient cards.

Accent colors should appear as **solid blocks**.

* * *

94. No excessive rounded cards
    ==============================

This is worth repeating because many UI generators default to this.

Do not produce:
    ╭────────────────╮
    │                │
    │       CARD     │
    │                │
    ╰────────────────╯

with giant 24px rounded corners.

Instead:
    ┌──────────────────┐
    │                  │
    │       CARD       │
    │                  │
    └──────────────────┘
        █████████

Square or lightly rounded.

Heavy border.

Offset shadow.

* * *

95. No generic dashboard metrics
    ================================

Don't add:
    4.82 MB
    1,204
    98%
    24 videos

as giant KPI cards unless those metrics genuinely help the user.

The app is a file-processing tool, not an analytics dashboard.

* * *

96. Screen hierarchy for BitStream
    ==================================

I would define the product screens roughly like this:

### Encode

Primary workflow.

### Decode

Reverse workflow.

### History

Previous operations.

### Settings

Configuration.

Everything else should support those.

* * *

97. Encode screen visual priority
    =================================

Priority:
    1. FILE SELECTION
    2. ENCODE ACTION
    3. CONFIGURATION
    4. PROGRESS
    5. OUTPUT DETAILS
    6. ADVANCED INFORMATION

Don't reverse this.

* * *

98. Decode screen visual priority
    =================================
    
    1. VIDEO SELECTION
    2. DECODE ACTION
    3. DESTINATION
    4. INTEGRITY RESULT
    5. RECOVERED FILES

* * *

99. History visual priority
    ===========================
    
    1. RECENT OPERATIONS
    2. STATUS
    3. FILE / VIDEO INFORMATION
    4. OPEN / REVEAL ACTION

* * *

100. Settings visual priority
     =============================

Group settings:
    ENCODING
    STEGANOGRAPHY
    OUTPUT
    INTERFACE
    ADVANCED

Do not throw everything into one giant settings panel.

* * *

101. Responsive behavior
     ========================

On a wide window:
    two-column layout where appropriate

On a narrow window:
    single-column
    stack controls
    preserve hierarchy

Do not squash the interface.

* * *

102. Mobile/touch considerations
     ================================

If the UI might eventually run on touch:

* minimum 44px hit targets

* don't use tiny icon controls

* give controls enough spacing

* keep focus indicators usable

Neo-brutalism can work beautifully on touch because its interaction states are highly visible.

* * *

103. Code architecture should reflect the design system
     =======================================================

The AI should create reusable tokens.

For example conceptually:
    colors
    typography
    spacing
    radii
    borders
    shadows
    transitions

Then components consume those tokens.

Don't hardcode colors all over the codebase.

* * *

104. Suggested design tokens
     ============================

A conceptual system:
    COLOR_BACKGROUND
    COLOR_SURFACE
    COLOR_BLACK
    COLOR_WHITE
    COLOR_TEAL
    COLOR_MAGENTA
    COLOR_YELLOW
    COLOR_ERROR

    BORDER_THIN
    BORDER_STANDARD
    BORDER_HEAVY

    RADIUS_NONE
    RADIUS_SMALL
    RADIUS_MEDIUM

    SHADOW_NONE
    SHADOW_SM
    SHADOW_MD
    SHADOW_LG

    SPACE_1
    SPACE_2
    SPACE_3
    SPACE_4
    SPACE_6
    SPACE_8
    SPACE_12
    SPACE_16

The actual naming is up to the implementation.

The principle is mandatory.

* * *

105. Component naming
     =====================

Components should reflect product concepts:
    FileDropZone
    FileQueue
    EncodingSettings
    CodecSelector
    ResolutionSelector
    FrameRateSelector
    SteganographyPanel
    CoverVideoPicker
    EncodingProgress
    VerificationResult
    EncodingHistory

This is much better than:
    Card1
    Box2
    Panel3
    Thing4

* * *

106. Component behavior should be deterministic
     ===============================================

A brutalist visual system can become chaotic if states aren't standardized.

Every interactive component should define:
    default
    hover
    focus
    active/pressed
    disabled
    error
    success (where applicable)

The AI should not invent state behavior independently for each component.

* * *

107. File queue
     ===============

The file queue is a particularly important component.

Each row should show:
    ICON
    FILENAME
    SIZE
    TYPE
    STATUS
    REMOVE

Visual structure:
    ┌──────────────────────────────────────────────┐
    │ ◼ project.zip     ZIP    4.82 MB    ✓   ×   │
    ├──────────────────────────────────────────────┤
    │ ◼ photo.jpg       JPG    2.13 MB    ✓   ×   │
    └──────────────────────────────────────────────┘

Strong grid.

Clear typography.

Minimal decoration.

* * *

108. Encoding settings
     ======================

The setting blocks should look like technical specifications.

For example:
    RESOLUTION

    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ 480P     │ │ 720P     │ │ 1080P    │
    └──────────┘ └──────────┘ └──────────┘
                             ↑
                           TEAL

Selected state should be bold and obvious.

* * *

109. Steganography panel
     ========================

Potential layout:
    STEGANOGRAPHY

    [ OFF ] [ ON ]

    Embed the payload inside the pixel LSBs
    of a cover video.

    COVER VIDEO
    [ Choose video ]

    CAPACITY
    18.4 MB

    PAYLOAD
    12.8 MB

    HEADROOM
    5.6 MB

This is both visually strong and technically informative.

* * *

110. Verification component
     ===========================

After processing, show:
    VERIFICATION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✓ SHA-256 MATCH

    Original
    4C3...

    Recovered
    4C3...

    DATA INTEGRITY
    VERIFIED

The “VERIFIED” state can use teal.

This would fit the design perfectly.

* * *

111. Error philosophy
     =====================

Errors should be:

**direct, specific, actionable.**

Instead of:

> Something went wrong.

Say:

> **Cover video capacity exceeded.**
> 
> Payload: 82.4 MB  
> Capacity: 64.1 MB
> 
> Choose a larger video or reduce the payload.

This is both good UX and good technical presentation.

* * *

112. Empty state philosophy
     ===========================

Empty states should tell the user:

1. what is missing

2. why it matters

3. what to do next

Example:
    NO FILES SELECTED

    Add one or more files to begin encoding.

    [ ADD FILES ]

* * *

113. Status terminology
     =======================

Use a consistent vocabulary.

For example:
    READY
    QUEUED
    ENCODING
    WRITING
    VERIFYING
    COMPLETE
    FAILED
    CANCELLED

Don't alternate between:

* done

* finished

* successful

* complete

* completed

* ready

for the same state.

* * *

114. Design voice
     =================

Text should also match the visual philosophy.

Use **short, direct, confident language**.

Good:

> **SELECT FILES**

> **CHOOSE OUTPUT**

> **ENCODE VIDEO**

> **VERIFY RESULT**

Avoid overly conversational UI copy:

> "Let's get started! Choose some files below and we'll take care of the rest!"

The design is more assertive than that.

* * *

115. Microcopy
     ==============

Examples:

**ENCODE**

> Convert the selected payload into a lossless FFV1 video.

**STEGANOGRAPHY**

> Embed payload bits into a cover video's pixel channels.

**VERIFICATION**

> Compare original and recovered SHA-256 hashes.

This makes the app feel technically serious.

* * *

116. Decorative typography
     ==========================

You can occasionally use giant display text as a visual anchor.

For example:
    ENCODE

in 64–96px.

But only when it reinforces hierarchy.

Don't put giant words everywhere.

* * *

117. Visual rhythm
     ==================

A screen should alternate between:

**large graphic heading**

↓

**structured content**

↓

**accent block**

↓

**content**

↓

**large spacing**

This creates the same rhythm as the reference poster.

* * *

118. The app should feel almost printable
     =========================================

This is a useful mental test.

Imagine printing a screenshot of the application on beige paper.

Would it still look coherent?

If yes, you're probably close.

If the design depends on:

* glow

* blur

* gradients

* transparency

* animation

then you're drifting away from the intended style.

* * *

119. Physicality without skeuomorphism
     ======================================

Don't add fake screws, knobs, bolts, or literal hardware graphics.

The physicality comes from:

* borders

* shadows

* offsets

* geometric construction

* interaction movement

This is **neo-brutalist**, not skeuomorphic.

* * *

120. Important distinction: loud does not mean chaotic
     ======================================================

The design can be visually loud while remaining highly organized.

That means:

**strong colors**

but:

**few colors**

**large headings**

but:

**strict hierarchy**

**thick borders**

but:

**consistent borders**

**bold components**

but:

**clear spacing**

This tension is what makes the reference work.

* * *

121. The central aesthetic formula
     ==================================

The entire design can basically be thought of as:
    PAPER BEIGE
    +
    BLACK
    +
    THICK OUTLINES
    +
    HUGE TYPOGRAPHY
    +
    LIMITED RADIUS
    +
    OFFSET SHADOWS
    +
    SOLID ACCENT BLOCKS
    +
    STRICT GRID
    +
    HIGH CONTRAST
    +
    VISIBLE STATES
    +
    MINIMAL DECORATION

That is the core formula.

* * *

122. Things the AI must explicitly NOT do
     =========================================

I would literally include this section in the implementation prompt.

### Do not:

* use glassmorphism

* use frosted cards

* use excessive blur

* use gradients as the primary visual treatment

* use pastel UI colors

* use giant rounded cards

* use pill-shaped buttons by default

* use soft drop shadows everywhere

* use subtle gray borders as the main structure

* use generic dashboard layouts

* use emoji as icons

* use random icon sets

* use futuristic/cyberpunk typography

* use neon glow

* make every element colorful

* make every section a card

* hide focus states

* create tiny click targets

* create arbitrary spacing values

* create arbitrary radii

* create arbitrary shadows

* introduce unnecessary decorative elements

* sacrifice usability for visual novelty

* * *

123. Things the AI MUST do
     ==========================

### Must:

* use a warm paper-beige background

* use black as a major structural color

* use thick black borders

* use strong offset shadows

* use limited corner radii

* use large heavy typography

* maintain a strict spacing grid

* maintain strict alignment

* use teal, yellow and magenta strategically

* keep contrast extremely high

* make focus states obvious

* provide strong hover/pressed states

* preserve accessibility

* maintain reusable design tokens

* use consistent iconography

* make primary actions visually dominant

* expose important technical information

* preserve clear workflow hierarchy

* favor solid fills over gradients

* favor graphic composition over decorative effects

* keep the visual system consistent across every screen

* * *

124. The most important BitStream-specific principle
     ====================================================

**The neo-brutalist design should make the technical nature of BitStream more obvious, not hide it.**

The UI should make someone think:

> “This is a serious experimental piece of software.”

rather than:

> “This is a pretty file uploader.”

That's why the technical metadata, encoding stages, payload capacity, codec information, frame counts, verification results, and steganographic mode should all have a visible place in the interface.

* * *

125. The ideal final personality of BitStream
     =============================================

Imagine someone opening it.

They see:

**BITSTREAM**

**LOSSLESS DATA → VIDEO**

A bold black-bordered drop zone.

Teal **ADD FILES**.

A clean file queue.

A huge **ENCODE VIDEO** action.

Heavy headings.

Black outlines.

Yellow warnings.

Magenta destructive states.

A mechanical progress bar.

A strong:

**✓ DATA INTEGRITY VERIFIED**

at the end.

The whole thing feels like a **precision tool designed by someone who cared about both engineering and visual systems**.

That's exactly where I would take BitStream.

* * *

The prompt I would actually give your coding AI
-----------------------------------------------

You can essentially prepend this to the rest of the BitStream implementation instructions:

> **Redesign the entire BitStream application using a disciplined neo-brutalist product design system inspired by the supplied reference design-system poster. Do not copy the poster literally and do not turn the application into a generic brutalist webpage. Reproduce its visual grammar: warm paper-beige background, off-white surfaces, dominant black typography and structural outlines, 2–3px black borders, hard offset shadows such as 2px–6px solid black offsets, extremely limited corner radii, oversized heavy display typography, strict grid alignment, deliberate spacing tokens, solid saturated accent blocks using teal/yellow/magenta, high contrast, visible focus states, obvious hover/pressed/disabled states, strong primary-action hierarchy, graphic section dividers, structured lists and tables, and minimal decoration. The interface should feel tactile, physical, editorial, technical, bold, systematic, and highly usable. It must not use glassmorphism, soft neumorphism, pastel colors, excessive blur, gradient-heavy surfaces, giant rounded cards, pill-shaped everything, cyberpunk styling, neon glow, random shadows, random spacing, or generic SaaS dashboard patterns. Treat the design as a formal design system: define reusable color, typography, spacing, border, radius, shadow, icon, and interaction tokens, then build all screens and components from those tokens. Every interactive component must have consistent default, hover, focus, pressed, disabled, and relevant error/success states. Focus indicators must always remain visible and obvious. Use one primary action per major screen. Preserve strong accessibility and minimum comfortable hit areas. Use bold, consistent iconography rather than emoji. The visual system should communicate BitStream's actual technical purpose: file selection → payload preparation → encoding → optional LSB steganographic embedding → FFV1 video generation → verification. Expose useful technical information such as codec, resolution, FPS, payload size, frame count, capacity, mode, and integrity verification in the UI rather than hiding the engineering behind decorative UI. The result should look like a deliberately designed precision utility rather than a prototype dashboard.**

That last paragraph is the part I'd consider **non-negotiable** for BitStream: the style shouldn't just sit _on top_ of the project. It should make the project's underlying engineering legible.

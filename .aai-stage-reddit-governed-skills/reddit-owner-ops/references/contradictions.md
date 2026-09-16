# Contradiction classes

Each class blocks ship unless Krass overrides it in operator state.

| ID | Class | Typical miss |
| --- | --- | --- |
| C1 | Sticky exemption vs engine | Title-regex missing or ID list stale |
| C2 | Public copy leak | Floor in `comment:`, header, or saved reply |
| C3 | Packet vs engine codes | 1a/1e text does not match the firing rule |
| C4 | Dual engine | Safety Filter and AutoMod tell two stories |
| C5 | Saved reply vs live rule | Reply says a check does not exist |
| C6 | Gate skip | Draft written as if the wiki paste already happened |
| C7 | Roster fiction | Permission bits assigned without a live source |

Record open classes in operator state. Close them only with a current-source
fix or an explicit Krass override.

# Offline Stop and Restart Evidence Cases

These synthetic traces address two questions. Did any ordinary motion command reach the drive after the stop request? What evidence establishes that the moving mechanism stopped? Evaluate those questions separately. A drive dispatch here means a new application motion target. Drive commands needed to execute the stop itself are outside that count.

For this fixture, all events use one clock. The initial owner has generation 7. A stop invalidates it, a reset clears the latch, and an explicit new start grants generation 8. The fixture uses an independent position sensor with a declared standstill detector. Its times and displacements illustrate evidence handling and carry no acceptance limits.

| Case | Recorded events in chronological order | Expected review finding |
| --- | --- | --- |
| Physical outcome observed | Hazard at 0 ms, detection at 12 ms, stop request at 16 ms, drive ACK at 21 ms, standstill detector asserts at 76 ms and remains asserted through 180 ms. A linear axis moves monotonically from 100 to 118 mm between onset and standstill. | Detection delay 12 ms, request-to-standstill 60 ms, onset-to-standstill 76 ms, travel 18 mm. Report sensor resolution and detector dwell if comparing with a limit. |
| Feedback lost | Same hazard, detection, request, and ACK. Independent position feedback ends at 22 ms, before standstill is established. | Request receipt confirmed. Stopping time and distance remain unknown. |
| Old reply after new start | Stop, reset, new start with generation 8, delayed policy reply from generation 7, drive accepts that reply. | Fail command authorization. Re-arming cannot authorize a previous generation. The eventual physical effect requires a separate observation. |
| Reset starts motion | Stop, confirmed standstill, emergency-stop release and reset, buffered trajectory resumes before a new start. | Fail restart verification even if the application log shows an empty queue. Trace pending work in the controller and drive. |
| Deliberate recovery | Stop, confirmed standstill, initiating hazard cleared, reset, no motion, explicit new start, a fresh generation-8 target is dispatched and generation 7 is rejected. | The trace supports the specified restart sequence. Any stopping-distance claim still needs measurements under the declared operating conditions. |

When using actual traces, retain the initiating signal, independent motion feedback, clock relationship, and configuration alongside the result. If the clocks cannot be aligned, report intervals measured within each clock domain and leave cross-domain timing unresolved.

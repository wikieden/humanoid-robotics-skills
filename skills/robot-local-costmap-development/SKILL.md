---
name: robot-local-costmap-development
description: Develop a rolling obstacle map or traversability layer from depth and lidar. Use for ray integration, occupancy decay, height-aware projection, and publishing a consistent costmap to a planner.
metadata:
  title: Local Occupancy and Traversability Map Development
---

# Local Occupancy and Traversability Map Development

Start with a scene where projection changes the answer. A doorway and a low overhang can have identical floor outlines. Specify the clearance and support observations a consumer needs, its unknown-space policy, and its maximum usable map age. A 2D grid suffices for a planar scan within a declared height band. Store vertical evidence in columns or sparse voxels when overhead clearance, steps or missing floor can change the route.

## Implement a map update

1. Transform each ray origin and endpoint into a continuous local frame at acquisition time. Remove self returns using the robot configuration at that time. Use floor division for voxel keys, including coordinates below zero. Keep keys fixed in the local frame and crop to the rolling window, or shift a circular buffer by whole cells and invalidate newly exposed cells.
2. Traverse cells from the sensor origin to a measured surface. Apply miss evidence to the traversed cells and hit evidence to the endpoint. Leave space beyond the first opaque return unobserved. For a reliable range-limit observation, clear only to its documented limit. A missing depth pixel, absent scan, or failed transform supplies no clearing ray.
3. Store bounded log odds and the last observation time. For inverse-model probability `p` and prior `p0`, add `logit(p) − logit(p0)` to the previous score and clamp it. Deduplicate repeated delivery of a source frame. For dense overlapping rays, specify how conflicting hit and miss evidence in one scan is aggregated. Use measurement age to decay confidence toward unknown. A timer tick carries no new measurement.
4. For a traversability layer, estimate ground height and support in neighboring columns. Grow a connected region from observed support under the robot, checking step height, slope and vertical body clearance. Mark unseen floor as unknown. A biped can use this layer to select a corridor, while its foothold planner still needs contact area, reachable step transitions, and swing clearance.
5. Publish the map data with its frame, origin, cell size, observation interval and revision taken from the same snapshot. Give an asynchronous traversability result the revision of its input. Keep the measured occupancy distinct from planner costs such as footprint inflation so footprint changes do not require reintegrating sensor data.

## Minimal regression for a disappearing obstacle

This Python example uses one grid row, positive-going rays and synthetic log-odds increments. It tests the difference between a lost frame and later measurements that see through the former obstacle position.

```python
scores = {}
seen = set()


def observe(frame_id, hit):
    if hit is None or frame_id in seen:
        return
    seen.add(frame_id)
    for cell in range(hit):
        scores[cell] = max(-4, scores.get(cell, 0) - 1)
    scores[hit] = min(4, scores.get(hit, 0) + 2)


observe(1, 2)
assert scores == {0: -1, 1: -1, 2: 2}  # Cell 3 is occluded.
observe(1, 2)
observe(2, None)
assert scores[2] == 2 and 3 not in scores
for frame_id in (3, 4, 5):
    observe(frame_id, 4)
assert scores[2] < 0 and scores[4] > 0 and 5 not in scores
```

**Deliverable.** Return the sensor model, grid representation, clearing and expiry rules, and planner-facing contract. Replay a stationary obstacle across a window shift, an obstacle removed under direct observation, and a sensor dropout. For each, report false clearances, time to mark or clear, unknown coverage in the path, and observation-to-publication latency. When profiling ray integration, vary return count and resolution independently. For a probabilistic 3D occupancy baseline, see [OctoMap](https://octomap.github.io/).

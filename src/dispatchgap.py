"""Exact document-date reachability with a minimum inter-document handoff gap.

No inference of delivery, reading, forwarding, or shared message content is made.
An output bit at target v denotes an admissible route ending with a document
dated in the window, not a delivery completed by the end of the window.
"""
from collections import defaultdict, deque
from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class Contact:
    day: int
    author: str
    recipient: str
    document: str


def static_masks(contacts, nodes):
    index = {n: i for i, n in enumerate(nodes)}
    adjacency = defaultdict(set)
    for e in contacts:
        adjacency[e.author].add(e.recipient)
    masks = [0] * len(nodes)
    for source in nodes:
        seen, todo = {source}, deque([source])
        while todo:
            for target in adjacency[todo.popleft()]:
                if target not in seen:
                    seen.add(target)
                    todo.append(target)
        bit = 1 << index[source]
        for target in seen:
            masks[index[target]] |= bit
    return masks


def temporal_masks(contacts, nodes, gap):
    """Return one bitmask of admissible origins per destination.

    All origins are available before the first dated contact. A contact at t
    can carry an origin available to its author at t. Its recipient becomes
    available as an intermediate vertex at t+gap. Final legs are counted at t.
    For gap=0 each day's directed contacts are closed to a fixed point.
    """
    if not isinstance(gap, int) or gap < 0:
        raise ValueError("gap must be a nonnegative integer")
    index = {n: i for i, n in enumerate(nodes)}
    ready = [1 << i for i in range(len(nodes))]
    reached = ready.copy()
    grouped = defaultdict(list)
    for e in contacts:
        grouped[e.day].append((index[e.author], index[e.recipient]))
    pending = []
    serial = 0
    for day, edges in sorted(grouped.items()):
        while pending and pending[0][0] <= day:
            _, _, target, mask = heapq.heappop(pending)
            ready[target] |= mask
        if gap == 0:
            changed = True
            while changed:
                changed = False
                for author, recipient in edges:
                    new = ready[recipient] | ready[author]
                    if new != ready[recipient]:
                        ready[recipient] = new
                        changed = True
            for _, recipient in edges:
                reached[recipient] |= ready[recipient]
        else:
            for author, recipient in edges:
                mask = ready[author]
                reached[recipient] |= mask
                serial += 1
                heapq.heappush(pending, (day + gap, serial, recipient, mask))
    return reached


def pair_count(masks):
    return sum(mask.bit_count() - 1 for mask in masks)


def route(contacts, source, target, gap):
    """Return a document-level route witness or None (source != target)."""
    if source == target:
        return ()
    grouped = defaultdict(list)
    for e in contacts:
        grouped[e.day].append(e)
    # Earliest availability dominates with unlimited waiting and lower gaps.
    available = {source: (-10**20, ())}
    for day, edges in sorted(grouped.items()):
        changed = True
        while changed:
            changed = False
            for e in edges:
                state = available.get(e.author)
                if state is None or state[0] > day:
                    continue
                path = state[1] + (e,)
                if e.recipient == target:
                    return path
                when = day + gap
                previous = available.get(e.recipient)
                if previous is None or when < previous[0]:
                    available[e.recipient] = (when, path)
                    changed = gap == 0
    return None


def critical_gap(contacts, source, target):
    """Largest integer gap for an indirect-only route; None if unreachable.

    A direct contact has unbounded gap under the terminal-leg convention;
    it is reported as 'direct' rather than a fabricated finite threshold.
    """
    if any(e.author == source and e.recipient == target for e in contacts):
        return "direct"
    if route(contacts, source, target, 0) is None:
        return None
    span = max(e.day for e in contacts) - min(e.day for e in contacts)
    lo, hi = 0, span + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if route(contacts, source, target, mid) is None:
            hi = mid
        else:
            lo = mid
    return lo


def oracle(contacts, source, gap):
    """Independent finite state graph search over (vertex, availability)."""
    todo = deque([(source, -10**20)])
    seen = set(todo)
    endpoints = {source}
    while todo:
        author, ready = todo.popleft()
        for e in contacts:
            if e.author != author or e.day < ready:
                continue
            endpoints.add(e.recipient)
            state = (e.recipient, e.day + gap)
            if state not in seen:
                seen.add(state)
                todo.append(state)
    return endpoints

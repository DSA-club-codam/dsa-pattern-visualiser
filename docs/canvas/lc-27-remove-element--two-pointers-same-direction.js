/* Generated from problems/lc-27-remove-element/two-pointers-same-direction/canvas.js */
VIZ.canvas.register("lc-27-remove-element/two-pointers-same-direction", /* LC 27 · two pointers, same direction (copy forward).
   Reads step.state = { arr, slow, fast } and step.roles = { pos: "current" | "current removed" | "new" }.
   Values are copied, not swapped, so cells keep their position (no ids).
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.nums, { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, n = s.arr.length, slow = s.slow;
    const last = step.phase === "return";
    // fast = n after the loop; null before it starts and on the last step
    const read = last ? n : s.fast === null ? 0 : s.fast; // [slow, read) = free slots
    const cls = {};
    s.arr.forEach((v, pos) => {
      const c = [];
      if (pos < slow) c.push("done");
      else if (pos < read) c.push("out"); // old value, will be overwritten or ignored
      const role = step.roles[pos];
      if (role) c.push(role);
      cls[pos] = c.join(" ");
    });
    const bands = [];
    if (slow > 0) bands.push({ kind: "best", from: 0, to: slow - 1, label: "kept" });
    if (read > slow) bands.push({ kind: "gap", from: slow, to: read - 1, label: last ? "ignored" : "free" });
    const inside = (i) => (i === null || i >= n ? null : i);
    ctx.row.update({
      arr: s.arr,
      cls,
      bands,
      pointers: [
        { role: "back", label: "slow", at: last ? null : Math.min(slow, n - 1), dim: slow >= n },
        { role: "front", label: "fast", at: last ? null : inside(s.fast) },
      ],
    });
  },
}));

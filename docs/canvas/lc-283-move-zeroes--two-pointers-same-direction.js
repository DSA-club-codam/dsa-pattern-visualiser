/* Generated from problems/lc-283-move-zeroes/two-pointers-same-direction/canvas.js */
VIZ.canvas.register("lc-283-move-zeroes/two-pointers-same-direction", /* LC 283 · two pointers, same direction.
   Reads step.state = { arr, ids, slow, fast } and step.roles = { pos: "current" | "swap" }.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.nums, { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, n = s.arr.length, slow = s.slow, fast = s.fast;
    const last = step.phase === "return";
    const swapping = step.phase === "swap" && slow !== fast;
    // [0, slow) is placed; [slow, fast) holds zeros (at the end: [slow, n))
    const gapEnd = last ? n : fast === null ? slow : fast;
    const g0 = swapping ? slow + 1 : slow; // during a swap, slot slow already holds the non-zero
    const cls = {};
    s.arr.forEach((v, pos) => {
      const c = [];
      if (v === 0) c.push("zero");
      if (v !== 0 && pos < slow) c.push("done");
      const role = step.roles[pos];
      if (role) c.push(role);
      cls[pos] = c.join(" ");
    });
    const bands = [];
    if (slow > 0) bands.push({ kind: "best", from: 0, to: slow - 1, label: swapping ? "" : "placed" });
    if (gapEnd > g0) bands.push({ kind: "gap", from: g0, to: gapEnd - 1, label: swapping ? "" : "zeros" });
    ctx.row.update({
      arr: s.arr,
      ids: s.ids,
      cls,
      bands,
      arc: swapping ? { from: slow, to: fast, label: "swap" } : null,
      pointers: [
        { role: "back", label: "slow", at: Math.min(slow, n - 1), dim: slow >= n },
        { role: "front", label: "fast", at: fast },
      ],
    });
  },
}));

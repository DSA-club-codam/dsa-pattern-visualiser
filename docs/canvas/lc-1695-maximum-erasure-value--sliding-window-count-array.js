/* Generated from problems/lc-1695-maximum-erasure-value/sliding-window-count-array/canvas.js */
VIZ.canvas.register("lc-1695-maximum-erasure-value/sliding-window-count-array", /* LC 1695 · sliding window + counting array.
   Reads step.state = { arr, left, right, window, total, rows, dup, largest, bestWindow }
   and step.roles = { pos: "current" | "conflict" | "removed" }.
   Draws only with VIZ.ArrayRow and VIZ.countMap — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.nums, { roles: ["back", "front"], bar: true });
    ctx.mapPanel = ctx.extraPanel();
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, left = s.left, right = s.right;
    const cls = {}, tags = {};
    s.arr.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && i < left) c.push("out");
      if (step.phase === "return" && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1]) c.push("best");
      if (role === "current") c.push("current");
      if (role === "conflict") { c.push("conflict"); tags[i] = "×2"; }
      if (s.dup !== null && v === s.dup && role !== "conflict" && right !== null && i >= left && i <= right) c.push("dup");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    ctx.row.update({
      arr: s.arr,
      cls,
      tags,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · total ${s.total}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · largest ${s.largest}` }
        : null,
    });
    VIZ.countMap(ctx.mapPanel, s.rows, 1, "count <small>(value → times in window, at most 1)</small>");
  },
}));

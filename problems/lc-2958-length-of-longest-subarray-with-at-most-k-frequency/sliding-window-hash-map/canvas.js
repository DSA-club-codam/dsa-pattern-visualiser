/* LC 2958 · sliding window + hash map.
   Reads step.state = { arr, k, left, right, window, rows, over, length, longest, bestWindow }
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
      if (role === "conflict") { c.push("conflict"); tags[i] = ">k"; }
      if (s.over !== null && v === s.over && role !== "conflict" && right !== null && i >= left && i <= right) c.push("dup");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    ctx.row.update({
      arr: s.arr,
      cls,
      tags,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}]` + (s.length !== null ? ` · length ${s.length}` : "") }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · longest ${s.longest}` }
        : null,
    });
    VIZ.countMap(ctx.mapPanel, s.rows, s.k, `count <small>(value → times in window, limit k = ${s.k})</small>`);
  },
})

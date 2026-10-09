/* LC 344 · two pointers, towards each other, swapping.
   Reads step.state = { arr, ids, left, right, done } and step.roles = { pos: "swap" }.
   Spaces are shown as ␣ so they are visible. Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    const shown = (ch) => (ch === " " ? "␣" : ch);
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.s.map(shown), { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, n = s.arr.length, left = s.left, right = s.right;
    const shown = (ch) => (ch === " " ? "␣" : ch);
    const swapping = step.phase === "swap";
    const cls = {};
    s.arr.forEach((ch, pos) => {
      const c = [];
      // final: outside [left, right], or everything once the loop has ended
      if (s.done || pos < left || pos > right) c.push("done");
      const role = step.roles[pos];
      if (role) c.push(role);
      cls[pos] = c.join(" ");
    });
    const bands = !s.done && left < right ? [{ kind: "window", from: left, to: right, label: swapping ? "" : "not reversed" }] : [];
    const inside = (i) => (i < 0 || i >= n ? null : i);
    ctx.row.update({
      arr: s.arr.map(shown),
      ids: s.ids,
      cls,
      bands,
      arc: swapping ? { from: left, to: right, label: "swap" } : null,
      pointers: [
        { role: "back", label: "left", at: inside(left) },
        { role: "front", label: "right", at: inside(right) },
      ],
    });
  },
})

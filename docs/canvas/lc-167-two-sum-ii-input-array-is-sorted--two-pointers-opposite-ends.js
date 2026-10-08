/* Generated from problems/lc-167-two-sum-ii-input-array-is-sorted/two-pointers-opposite-ends/canvas.js */
VIZ.canvas.register("lc-167-two-sum-ii-input-array-is-sorted/two-pointers-opposite-ends", /* LC 167 · two pointers, towards each other.
   Reads step.state = { arr, left, right, found }.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.numbers, { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, left = s.left, right = s.right;
    const cls = {};
    s.arr.forEach((v, pos) => {
      if (pos < left || pos > right) cls[pos] = "out"; // dropped for good
      else if (s.found && (pos === left || pos === right)) cls[pos] = "best";
    });
    ctx.row.update({
      arr: s.arr,
      cls,
      bands: [{ kind: "window", from: left, to: right, label: s.found ? "" : "still possible" }],
      pointers: [
        { role: "back", label: "left", at: left },
        { role: "front", label: "right", at: right },
      ],
    });
  },
}));

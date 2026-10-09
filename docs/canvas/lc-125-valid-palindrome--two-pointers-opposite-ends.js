/* Generated from problems/lc-125-valid-palindrome/two-pointers-opposite-ends/canvas.js */
VIZ.canvas.register("lc-125-valid-palindrome/two-pointers-opposite-ends", /* LC 125 · two pointers, towards each other, on a string.
   Reads step.state = { arr, left, right, matched, done } and step.roles = { pos: "conflict" }.
   Spaces are shown as ␣ so they are visible. Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    const shown = (ch) => (ch === " " ? "␣" : ch);
    ctx.row = new VIZ.ArrayRow(ctx.canvas, [...ctx.example.args.s].map(shown), { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, n = s.arr.length, left = s.left, right = s.right;
    const shown = (ch) => (ch === " " ? "␣" : ch);
    const matched = new Set(s.matched);
    const alnum = (ch) => /[A-Za-z0-9]/.test(ch);
    const cls = {}, tags = {};
    s.arr.forEach((ch, pos) => {
      const c = [];
      if (matched.has(pos)) c.push("done");
      else if (!alnum(ch) && (pos < left || pos > right)) c.push("out"); // skipped
      const role = step.roles[pos];
      if (role) {
        c.push(role);
        if (role === "conflict") tags[pos] = "≠";
      }
      cls[pos] = c.join(" ");
    });
    const bands = left <= right && !s.done ? [{ kind: "window", from: left, to: right, label: "not checked" }] : [];
    const inside = (i) => (i < 0 || i >= n ? null : i);
    ctx.row.update({
      arr: s.arr.map(shown),
      cls,
      tags,
      bands,
      pointers: [
        { role: "back", label: "left", at: inside(left) },
        { role: "front", label: "right", at: inside(right) },
      ],
    });
  },
}));

/* Generated from problems/lc-88-merge-sorted-array/two-pointers-merge-from-end/canvas.js */
VIZ.canvas.register("lc-88-merge-sorted-array/two-pointers-merge-from-end", /* LC 88 · two pointers, merging from the end.
   Reads step.state = { arr1, arr2, m, p1, p2, write, placed, r1, r2 }:
   slots >= placed are final; r1 / r2 = { pos: "current" | "new" } per row.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    const a = ctx.example.args;
    ctx.canvas.innerHTML = "";
    const host = (title) => {
      ctx.canvas.insertAdjacentHTML("beforeend", `<h3>${title}</h3>`);
      const d = VIZ.el("div");
      ctx.canvas.append(d);
      return d;
    };
    const h1 = host(`nums1 <small>(m = ${a.m}, length ${a.nums1.length})</small>`);
    const h2 = host(`nums2 <small>(n = ${a.n})</small>`);
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums1, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.nums2, { roles: ["front"] });
  },

  render(step, ctx) {
    const s = step.state, n1 = s.arr1.length;
    const cls1 = {}, cls2 = {};
    s.arr1.forEach((v, pos) => {
      const c = [];
      const free = pos > s.p1 && pos < s.placed;
      if (pos >= s.placed) c.push("done");
      else if (free && pos >= s.m) c.push("zero"); // placeholder, never written yet
      else if (free) c.push("out"); // old copy of a value that moved right
      if (s.r1[pos]) c.push(s.r1[pos]);
      cls1[pos] = c.join(" ");
    });
    s.arr2.forEach((v, pos) => {
      const c = [];
      if (pos > s.p2) c.push("out");
      if (s.r2[pos]) c.push(s.r2[pos]);
      cls2[pos] = c.join(" ");
    });
    const bands = [];
    if (s.placed <= n1 - 1) bands.push({ kind: "best", from: s.placed, to: n1 - 1, label: "placed" });
    const freeTo = Math.min(s.write, s.placed - 1);
    if (freeTo > s.p1) bands.push({ kind: "gap", from: s.p1 + 1, to: freeTo, label: "free" });
    const finished = step.phase === "return";
    ctx.row1.update({
      arr: s.arr1,
      cls: cls1,
      bands,
      pointers: [
        { role: "back", label: "write", at: finished || s.write < 0 ? null : s.write },
        { role: "front", label: "p1", at: finished || s.p1 < 0 ? null : s.p1 },
      ],
    });
    ctx.row2.update({
      arr: s.arr2,
      cls: cls2,
      pointers: [{ role: "front", label: "p2", at: finished || s.p2 < 0 ? null : s.p2 }],
    });
  },
}));
